from models.database import SessionLocal
from models.sql_models import Empleado, User

db = SessionLocal()
empleados = db.query(Empleado).all()

print(f"Total Empleados: {len(empleados)}")
for emp in empleados[:5]:
    print(f"- {emp.nombre_completo} (Email: {emp.email})")

users = db.query(User).all()
print(f"\nTotal Usuarios: {len(users)}")
for u in users:
    print(f"- {u.email} (Rol: {u.role})")

db.close()
