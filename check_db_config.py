from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.sql_models import ConfiguracionTurno

db = SessionLocal()
configs = db.query(ConfiguracionTurno).all()
for c in configs:
    print(f"Codigo: {c.codigo}, Horario: {c.horario}, Desc: {c.descripcion}")
db.close()
