# -*- coding: utf-8 -*-
print("🚀 INICIANDO MAIN.PY - CARGANDO MÓDULOS...")

"""
API REST para Cuadrante de Vigilantes
Permite acceso móvil a turnos, permutas y datos de empleados
"""

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Cargar variables de entorno
load_dotenv()

# Importar configuración
from config import settings, validate_settings, print_settings
from utils.logging_config import AppLogger, log_info

# Validar configuración
if not validate_settings():
    print("❌ Configuración inválida. Abortar.")
    exit(1)

# Inicializar logging
AppLogger.initialize(
    log_dir=settings.LOG_DIR,
    log_level=settings.LOG_LEVEL,
    environment=settings.ENVIRONMENT
)

# Mostrar configuración
print_settings()

log_info(f"Iniciando API - Ambiente: {settings.ENVIRONMENT}")

# Importar routers (después de logging)
from routers import auth, turnos, permutas, empleados, sync, vacaciones

# --- MIGRACIÓN AUTOMÁTICA DE BASE DE DATOS ---
def run_auto_migrations():
    from sqlalchemy import text, inspect
    from models.database import engine
    from utils.logging_config import log_info
    
    log_info("Ejecutando migraciones automáticas...")
    
    inspector = inspect(engine)
    
    # Definición de columnas por tabla
    migrations = {
        "turnos": [
            ("horas_trabajadas", "FLOAT DEFAULT 0.0"),
            ("horas_nocturnas", "FLOAT DEFAULT 0.0"),
            ("horas_festivas", "FLOAT DEFAULT 0.0"),
            ("es_festivo", "BOOLEAN DEFAULT FALSE")
        ],
        "config_turnos": [
            ("horas_total", "FLOAT DEFAULT 0.0"),
            ("horas_nocturnas", "FLOAT DEFAULT 0.0")
        ]
    }
    
    with engine.connect() as conn:
        for table_name, columns in migrations.items():
            # Obtener columnas existentes
            existing_columns = [c["name"] for c in inspector.get_columns(table_name)]
            
            for col_name, col_type in columns:
                if col_name not in existing_columns:
                    try:
                        log_info(f"Añadiendo columna {col_name} a la tabla {table_name}...")
                        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type};"))
                        conn.commit()
                        log_info(f"Columna {col_name} añadida con éxito.")
                    except Exception as e:
                        log_info(f"Error al añadir columna {col_name}: {e}")
                else:
                    # debug - log_info(f"La columna {col_name} ya existe en {table_name}.")
                    pass
                    
    log_info("Migraciones finalizadas.")

# Ejecutar antes de crear la APP
run_auto_migrations()

# Crear app FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description="API REST para gestión de turnos y cuadrantes de vigilantes",
    version=settings.API_VERSION
)

# Configurar manejadores de error (antes de middlewares)
from utils.error_handlers import setup_error_handlers
setup_error_handlers(app)

# Configurar CORS con dominios permitidos
allowed_origins = settings.get_allowed_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



log_info(f"CORS configurado con {len(allowed_origins)} origen(es)")

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(turnos.router, prefix="/api/turnos", tags=["Turnos"])
app.include_router(
    permutas.router, prefix="/api/permutas", tags=["Permutas"]
)
app.include_router(
    empleados.router, prefix="/api/empleados", tags=["Empleados"]
)
app.include_router(
    sync.router, prefix="/api/sync", tags=["Sincronización"]
)
app.include_router(
    vacaciones.router, prefix="/api/vacaciones", tags=["Vacaciones"]
)


@app.get("/api/")
async def root():
    """Endpoint raíz - información de la API"""
    return {
        "message": "API Cuadrante Vigilantes",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }


@app.get("/api/schedule/{year}/{month}")
async def get_schedule(
    year: int, 
    month: int,
    current_user: dict = Depends(auth.get_current_user)
):
    """
    Obtiene el cuadrante de turnos para un mes específico
    Retorna los turnos solo para el usuario autenticado
    """
    from models.database import SessionLocal
    from models.sql_models import Turno, Empleado
    
    db = SessionLocal()
    try:
        # Obtener el empleado asociado al usuario actual
        nombre_usuario = current_user.get("nombre")
        empleado = db.query(Empleado).filter(Empleado.nombre_completo == nombre_usuario).first()
        
        if not empleado:
            return {"anio": year, "mes": month, "shifts": {}}

        # Obtener turnos del mes para este empleado
        turnos = db.query(Turno).filter(
            Turno.empleado_id == empleado.id,
            Turno.anio == year,
            Turno.mes == month
        ).all()
        
        # Formatear como diccionario día -> objeto detallado
        shifts = {
            str(t.dia): {
                "codigo": t.codigo_turno,
                "t": t.horas_trabajadas,
                "n": t.horas_nocturnas,
                "f": t.horas_festivas,
                "es_festivo": t.es_festivo
            } 
            for t in turnos
        }
        
        return {
            "anio": year,
            "mes": month,
            "shifts": shifts
        }
    finally:
        db.close()


@app.get("/api/schedule/{year}/{month}/empleado/{empleado_id}")
async def get_schedule_by_employee(
    year: int, 
    month: int,
    empleado_id: int,
    current_user: dict = Depends(auth.get_current_user)
):
    """
    Obtiene el cuadrante de turnos para un empleado específico
    Solo permitido para coordinadores
    """
    from models.database import SessionLocal
    from models.sql_models import Turno, Empleado
    from fastapi import HTTPException
    
    # Verificar que el usuario sea coordinador o que sea el propio empleado
    if current_user.get("rol") != "coordinador":
        db_perm = SessionLocal()
        try:
            from sqlalchemy import func
            nombre_usuario = current_user.get("nombre")
            email_usuario = current_user.get("email")
            
            # Buscar el ID del empleado del usuario actual (insensible a mayúsculas/espacios)
            user_empleado = db_perm.query(Empleado).filter(
                func.lower(func.trim(Empleado.nombre_completo)) == func.lower(func.trim(nombre_usuario))
            ).first()
            
            # Fallback por email si el nombre no coincide exactamente
            if not user_empleado and email_usuario:
                user_empleado = db_perm.query(Empleado).filter(
                    func.lower(func.trim(Empleado.email)) == func.lower(func.trim(email_usuario))
                ).first()

            if not user_empleado or user_empleado.id != empleado_id:
                raise HTTPException(status_code=403, detail="No autorizado para ver este cuadrante (identidad no confirmada)")
        finally:
            db_perm.close()
    
    db = SessionLocal()
    try:
        # Verificar que el empleado existe
        empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
        if not empleado:
            return {"anio": year, "mes": month, "shifts": {}}

        # Obtener turnos del mes para este empleado
        turnos = db.query(Turno).filter(
            Turno.empleado_id == empleado_id,
            Turno.anio == year,
            Turno.mes == month
        ).all()
        
        # Formatear como diccionario día -> objeto detallado
        shifts = {
            str(t.dia): {
                "codigo": t.codigo_turno,
                "t": t.horas_trabajadas,
                "n": t.horas_nocturnas,
                "f": t.horas_festivas,
                "es_festivo": t.es_festivo
            } 
            for t in turnos
        }
        
        return {
            "anio": year,
            "mes": month,
            "empleado_id": empleado_id,
            "empleado_nombre": empleado.nombre_completo,
            "shifts": shifts
        }
    finally:
        db.close()


@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {"status": "healthy"}





# Servir archivos estáticos (PWA) al final para no capturar rutas de API
if os.path.exists("static"):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    # Ejecutar servidor de desarrollo
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload en desarrollo
    )
