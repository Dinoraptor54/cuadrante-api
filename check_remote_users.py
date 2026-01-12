from sqlalchemy import create_engine, text
import os

# URL Confirmada (AWS-1)
DATABASE_URL = "postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"

def check_users():
    try:
        engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 10})
        with engine.connect() as conn:
            # Verificar si la tabla users existe
            result = conn.execute(text("SELECT to_regclass('public.users')"))
            if not result.scalar():
                print("❌ La tabla 'users' NO existe. La base de datos está vacía.")
                return

            # Listar usuarios
            result = conn.execute(text("SELECT email, role, is_active FROM users"))
            users = result.fetchall()
            
            if not users:
                print("⚠️  La tabla 'users' existe pero está VACÍA.")
                print("   Necesitas poblar la base de datos.")
            else:
                print(f"✅ Se encontraron {len(users)} usuarios:")
                for u in users:
                    print(f"   - Email: {u[0]} | Rol: {u[1]} | Activo: {u[2]}")

    except Exception as e:
        print(f"❌ Error al conectar: {e}")

if __name__ == "__main__":
    check_users()
