# Test de Conexión a Supabase (Diagnóstico Profundo)

import os
from sqlalchemy import create_engine, text

# Contraseña URL-encoded
PWD = "Dinor%40ptor55."
PROJECT_ID = "wmnnbkkiskfvbxdgxcby"

urls_to_test = [
    {
        "name": "Pooler AWS-0 (Port 5432)",
        "url": f"postgresql://postgres.{PROJECT_ID}:{PWD}@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"
    },
    {
        "name": "Pooler AWS-0 (Port 6543)",
        "url": f"postgresql://postgres.{PROJECT_ID}:{PWD}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    },
    {
        "name": "Pooler AWS-1 (Port 5432)",
        "url": f"postgresql://postgres.{PROJECT_ID}:{PWD}@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"
    },
    {
        "name": "Pooler AWS-1 (Port 6543)",
        "url": f"postgresql://postgres.{PROJECT_ID}:{PWD}@aws-1-eu-central-1.pooler.supabase.com:6543/postgres"
    },
    {
        "name": "Direct Connection (IPv6)",
        "url": f"postgresql://postgres.{PROJECT_ID}:{PWD}@db.{PROJECT_ID}.supabase.co:5432/postgres"
    }
]

print("Iniciando diagnostico detallado de conexion...\n")

for item in urls_to_test:
    print(f"Probando: {item['name']}")
    print(f"   URL: {item['url'][:60]}...")
    
    try:
        engine = create_engine(item['url'], pool_pre_ping=True, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"   [EXITO] Conectado correctamente.")
            print(f"   Version: {version[:40]}...")
    except Exception as e:
        error_msg = str(e)
        if "Tenant or user not found" in error_msg:
            print(f"   [ERROR CRITICO] Tenant/User not found (Host incorrecto para este proyecto)")
        elif "Network is unreachable" in error_msg:
             print(f"   [ERROR DE RED] Network unreachable (Problema de IPv6)")
        else:
             print(f"   [ERROR] {error_msg.split('[')[0][:100]}")
    print("-" * 50)
