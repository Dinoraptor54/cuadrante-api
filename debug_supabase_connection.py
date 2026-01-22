import psycopg2
import sys
from urllib.parse import quote_plus

# Credentials
PROJECT_ID = "wmnnbkkiskfvbxdgxcby"
PASSWORD_RAW = "Dinor@ptor55."
PASSWORD_ENCODED = quote_plus(PASSWORD_RAW)

# Combinations to test
hosts = [
    "aws-0-eu-central-1.pooler.supabase.com",
    "aws-1-eu-central-1.pooler.supabase.com",
    f"db.{PROJECT_ID}.supabase.co"
]
ports = [5432, 6543]
users = [
    f"postgres.{PROJECT_ID}",
    "postgres"
]

def test_connection(name, dsn):
    print(f"Testing {name}...")
    try:
        conn = psycopg2.connect(dsn, connect_timeout=5)
        conn.close()
        msg = f"✅ SUCCESS: {name}"
        print(msg)
        with open("debug_connection_output.txt", "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        return True
    except Exception as e:
        msg = f"❌ FAILED: {name} - {str(e).strip()}"
        print(msg)
        with open("debug_connection_output.txt", "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        return False

with open("debug_connection_output.txt", "w", encoding="utf-8") as f:
    f.write("--- Starting Connection Diagnostics ---\n")
print(f"Project ID: {PROJECT_ID}")
print(f"Password encoded: {PASSWORD_ENCODED}")

success = False
working_dsn = ""

for host in hosts:
    for port in ports:
        for user in users:
            # Skip invalid combinations (direct URL usually doesn't need project ID in user, but pooler DOES)
            
            # Construct DSN
            # Note: For psycopg2, we can pass parameters or a DSN string. 
            # DSN string format: postgresql://user:password@host:port/dbname
            
            # Test with encoded password in URL
            dsn = f"postgresql://{user}:{PASSWORD_ENCODED}@{host}:{port}/postgres"
            test_name = f"Host={host}, Port={port}, User={user}"
            
            if test_connection(test_name, dsn):
                success = True
                working_dsn = dsn
                break
        if success: break
    if success: break

if success:
    print("\n--- ✅ FOUND WORKING CONFIGURATION ---")
    print(f"DSN: {working_dsn}")
else:
    print("\n--- ❌ ALL COMBINATIONS FAILED ---")
    print("Please verify the Project ID and Password are correct.")
