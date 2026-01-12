# -*- coding: utf-8 -*-
"""
Script de inicialización de base de datos
Crea todas las tablas y datos iniciales necesarios
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Cargar variables de entorno
load_dotenv()

# Importar modelos
from models.database import Base, SessionLocal
from models.sql_models import Empleado, User
from services.auth_service import get_password_hash


def init_db():
    """Inicializa la base de datos"""
    
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./cuadrante.db"
    )
    
    print(f"📊 Conectando a: {database_url[:50]}...")
    
    # Crear engine
    engine = create_engine(database_url)
    
    try:
        # Probar conexión
        with engine.connect() as _:
            print("✅ Conexión exitosa a la BD")
    except OperationalError as e:
        print(f"❌ Error al conectar a BD: {e}")
        return False
    
    # Crear tablas
    try:
        print("🔨 Creando tablas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return False
    
    # Crear usuario administrador inicial
    try:
        print("👤 Creando usuario administrador inicial...")
        db = SessionLocal()
        
        # Verificar si ya existe
        admin_usuario = db.query(User).filter(
            User.email == "admin@example.com"
        ).first()
        
        if admin_usuario:
            print("ℹ️ Usuario admin ya existe")
        else:
            # Crear usuario admin (sin empleado necesariamente)
            admin_usuario = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrador Sistema",
                role="coordinador"
            )
            db.add(admin_usuario)
            db.commit()
            db.add(admin_usuario)
            db.commit()
            print("✅ Usuario admin creado: admin@example.com / admin123")
            print("   ⚠️  CAMBIAR CONTRASEÑA EN PRODUCCIÓN")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error al crear usuario admin: {e}")
        return False
    
    return True


def reset_db():
    """Reinicia la base de datos (desarrollo solo)"""
    
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./cuadrante.db"
    )
    
    # No permitir reset en producción
    if "postgresql://" in database_url and \
       os.getenv("ENVIRONMENT") == "production":
        print("❌ No se puede resetear BD en producción")
        return False
    
    print("⚠️  Reiniciando base de datos...")
    
    # Crear engine
    engine = create_engine(database_url)
    
    try:
        # Eliminar todas las tablas
        Base.metadata.drop_all(bind=engine)
        print("🗑️  Tablas eliminadas")
        
        # Recrear tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas recreadas")
        
        return True
    except Exception as e:
        print(f"❌ Error al resetear BD: {e}")
        return False


def check_db_health():
    """Verifica la salud de la BD"""
    
    try:
        db = SessionLocal()
        
        # Test query
        result = db.query(Empleado).first()
        
        print("✅ BD saludable")
        print(f"   Empleados en BD: {db.query(Empleado).count()}")
        print(f"   Usuarios en BD: {db.query(User).count()}")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Error en salud de BD: {e}")
        return False


if __name__ == "__main__":
    # Configurar encoding para Windows
    import sys
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == "init":
            print("Inicializando BD...")
            success = init_db()
            sys.exit(0 if success else 1)
        
        elif comando == "reset":
            print("Reseteando BD...")
            success = reset_db()
            if success:
                success = init_db()
            sys.exit(0 if success else 1)
        
        elif comando == "health":
            print("Verificando salud de BD...")
            success = check_db_health()
            sys.exit(0 if success else 1)
        
        else:
            print(f"Comando desconocido: {comando}")
            print("Comandos disponibles: init, reset, health")
            sys.exit(1)
    
    else:
        print("Inicializando BD (por defecto)...")
        success = init_db()
        if success:
            print("\nVerificando salud...")
            check_db_health()
        sys.exit(0 if success else 1)
