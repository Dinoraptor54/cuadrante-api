from models.database import SessionLocal
from models.sql_models import Empleado, User
from services.auth_service import get_password_hash

db = SessionLocal()

# 1. Limpiar usuarios anteriores (test)
db.query(User).delete()
db.commit()
print("🗑️  Usuarios anteriores eliminados.")

# 2. Buscar un empleado real
empleado = db.query(Empleado).first()

if empleado:
    print(f"👤 Empleado encontrado: {empleado.nombre_completo}")
    
    # Crear usuario para este empleado
    # Usamos su email si tiene, sino uno generado
    email = empleado.email if empleado.email else f"user{empleado.id}@cuadrante.com"
    
    user = User(
        email=email,
        hashed_password=get_password_hash("1234"),
        full_name=empleado.nombre_completo,
        role="vigilante"
    )
    db.add(user)
    db.commit()
    
    print(f"\n✅ Usuario creado exitosamente:")
    print(f"   Email: {email}")
    print(f"   Contraseña: 1234")
else:
    print("❌ No se encontraron empleados en la BD.")

db.close()
