from models.database import SessionLocal
from models.sql_models import Empleado

db = SessionLocal()
count = db.query(Empleado).count()
print(f"Total Empleados: {count}")
db.close()
