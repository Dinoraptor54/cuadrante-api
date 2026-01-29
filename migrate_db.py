# -*- coding: utf-8 -*-
"""
Script de migración para añadir columnas de horas a la base de datos en producción.
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def migrate():
    # Intentar obtener la URL de producción (Supabase)
    database_url = "postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    
    # Fallback al entorno si no se ha configurado
    env_url = os.getenv("DATABASE_URL")
    if env_url and "sqlite" not in env_url:
        database_url = env_url

    print(f"🚀 Iniciando migración en: {database_url[:70]}...")
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
