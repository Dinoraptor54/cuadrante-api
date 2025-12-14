# -*- coding: utf-8 -*-
"""
API REST para Cuadrante de Vigilantes
Permite acceso móvil a turnos, permutas y datos de empleados
"""

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

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


@app.get("/schedule/{year}/{month}")
async def get_schedule(year: int, month: int):
    """
    Obtiene el cuadrante de turnos para un mes específico
    Retorna todos los turnos para todos los empleados
    """
    from models.database import SessionLocal
    from models.sql_models import Turno, Empleado
    
    db = SessionLocal()
    try:
        # Obtener todos los turnos del mes
        turnos = db.query(Turno).filter(
            Turno.anio == year,
            Turno.mes == month
        ).all()
        
        # Organizar por empleado
        cuadrante = {}
        for turno in turnos:
            empleado = db.query(Empleado).filter(Empleado.id == turno.empleado_id).first()
            if empleado:
                if empleado.nombre_completo not in cuadrante:
                    cuadrante[empleado.nombre_completo] = {}
                cuadrante[empleado.nombre_completo][turno.dia] = turno.codigo_turno
        
        return {
            "anio": year,
            "mes": month,
            "cuadrante": cuadrante
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
