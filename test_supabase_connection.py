# Test de Conexión a Supabase

import os
from sqlalchemy import create_engine, text

# Diferentes URLs para probar
urls_to_test = [
    # Transaction Pooler (puerto 6543)
    "postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor@ptor55.@aws-1-eu-central-1.pooler.supabase.com:6543/postgres",
    
    # Session Pooler (puerto 5432)
    "postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor@ptor55.@aws-1-eu-central-1.pooler.supabase.com:5432/postgres",
    
    # Conexión directa
    "postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor@ptor55.@db.wmnnbkkiskfvbxdgxcby.supabase.co:5432/postgres",
]

print("🔍 Probando conexiones a Supabase...\n")

for i, url in enumerate(urls_to_test, 1):
    print(f"Prueba {i}:")
    print(f"URL: {url[:50]}...")
    
    try:
        engine = create_engine(url, pool_pre_ping=True, echo=False)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ ÉXITO - Conectado a PostgreSQL")
            print(f"   Versión: {version[:50]}...")
            print(f"\n🎯 USA ESTA URL EN RENDER:\n{url}\n")
            break
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:100]}")
        print()
else:
    print("\n⚠️ Ninguna URL funcionó. Verifica:")
    print("1. Que el proyecto de Supabase esté activo")
    print("2. Que la contraseña sea correcta")
    print("3. Que el project ID sea 'wmnnbkkiskfvbxdgxcby'")
