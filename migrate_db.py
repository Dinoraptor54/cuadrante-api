# -*- coding: utf-8 -*-
"""
Script de migración para añadir columnas de horas a la base de datos en producción.
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def migrate():
    # Obtener la URL de la base de datos (priorizar la de producción si estamos en modo despliegue)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ Error: No se encontró DATABASE_URL en el entorno.")
        return

    # Corrección para postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    print(f"🚀 Iniciando migración en: {database_url[:50]}...")
    engine = create_engine(database_url)

    queries = [
        # Columnas para la tabla 'turnos'
        "ALTER TABLE turnos ADD COLUMN IF NOT EXISTS horas_trabajadas FLOAT DEFAULT 0.0;",
        "ALTER TABLE turnos ADD COLUMN IF NOT EXISTS horas_nocturnas FLOAT DEFAULT 0.0;",
        "ALTER TABLE turnos ADD COLUMN IF NOT EXISTS horas_festivas FLOAT DEFAULT 0.0;",
        "ALTER TABLE turnos ADD COLUMN IF NOT EXISTS es_festivo BOOLEAN DEFAULT FALSE;",
        
        # Columnas para la tabla 'config_turnos'
        "ALTER TABLE config_turnos ADD COLUMN IF NOT EXISTS horas_total FLOAT DEFAULT 0.0;",
        "ALTER TABLE config_turnos ADD COLUMN IF NOT EXISTS horas_nocturnas FLOAT DEFAULT 0.0;"
    ]

    with engine.connect() as conn:
        for query in queries:
            try:
                conn.execute(text(query))
                conn.commit()
                print(f"✅ Ejecutado: {query[:50]}...")
            except Exception as e:
                print(f"⚠️  Aviso en query: {str(e)}")

    print("🎉 Migración completada exitosamente.")

if __name__ == "__main__":
    migrate()
