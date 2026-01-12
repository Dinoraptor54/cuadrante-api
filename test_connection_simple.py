import psycopg2
import sys

# URL que el usuario proporcionó
url = "postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor@ptor55.@aws-1-eu-central-1.pooler.supabase.com:6543/postgres"

print(f"Probando conexión a Supabase...")
print(f"URL: {url[:60]}...")
print()

try:
    # Parsear la URL manualmente
    parts = url.replace("postgresql://", "").split("@")
    user_pass = parts[0].split(":")
    host_port_db = parts[1].split("/")
    host_port = host_port_db[0].split(":")
    
    user = user_pass[0]
    password = user_pass[1]
    host = host_port[0]
    port = host_port[1]
    database = host_port_db[1]
    
    print(f"📋 Parámetros de conexión:")
    print(f"   Usuario: {user}")
    print(f"   Host: {host}")
    print(f"   Puerto: {port}")
    print(f"   Base de datos: {database}")
    print()
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        connect_timeout=10
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    
    print(f"✅ ¡CONEXIÓN EXITOSA!")
    print(f"   PostgreSQL: {version[:80]}")
    print()
    print(f"🎯 USA ESTA URL EN RENDER:")
    print(url)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN:")
    print(f"   {type(e).__name__}: {str(e)}")
    print()
    print("🔍 Posibles causas:")
    print("   1. Contraseña incorrecta")
    print("   2. Proyecto de Supabase en pausa o eliminado")
    print("   3. Firewall bloqueando la conexión")
    print("   4. Project ID incorrecto")
    sys.exit(1)
