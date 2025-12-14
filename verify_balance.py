import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import sql_models, database
from utils import security
from main import app

# Database setup
DATABASE_URL = database.SQLALCHEMY_DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
client = TestClient(app)

def init_db():
    print("[*] Asegurando esquema de base de datos...")
    sql_models.Base.metadata.create_all(bind=engine)

def cleanup_test_data(db):
    print("[*] Limpiando datos de prueba anteriores...")
    # Clean up potentially conflicting data
    user = db.query(sql_models.User).filter(sql_models.User.email == "balance@test.com").first()
    if user:
        db.delete(user)
    
    emp = db.query(sql_models.Empleado).filter(sql_models.Empleado.nombre_completo == "Usuario Balance").first()
    if emp:
        # Delete associated shifts first
        db.query(sql_models.Turno).filter(sql_models.Turno.empleado_id == emp.id).delete()
        db.delete(emp)
    
    db.commit()

def crear_datos_prueba():
    db = SessionLocal()
    cleanup_test_data(db)
    
    print("[*] Creando datos de prueba...")
    
    # 1. Create User
    user = sql_models.User(
        email="balance@test.com",
        hashed_password=security.get_password_hash("pass123"),
        full_name="Usuario Balance",
        role="vigilante",
        is_active=True
    )
    db.add(user)
    
    # 2. Create Empleado (linked by name)
    empleado = sql_models.Empleado(
        nombre_completo="Usuario Balance",
        email="balance@test.com",
        categoria="Vigilante"
    )
    db.add(empleado)
    db.commit()
    db.refresh(empleado)
    
    # 3. Create Shifts for 2024
    # N=12, N=12, D=12, V=5 -> Total 41h
    turnos = [
        sql_models.Turno(empleado_id=empleado.id, anio=2024, mes=1, dia=1, codigo_turno="N"),
        sql_models.Turno(empleado_id=empleado.id, anio=2024, mes=1, dia=2, codigo_turno="N"),
        sql_models.Turno(empleado_id=empleado.id, anio=2024, mes=1, dia=3, codigo_turno="D"),
        sql_models.Turno(empleado_id=empleado.id, anio=2024, mes=1, dia=4, codigo_turno="V"),
    ]
    db.add_all(turnos)
    db.commit()
    db.close()

def get_token():
    resp = client.post("/api/auth/login", data={"username": "balance@test.com", "password": "pass123"})
    if resp.status_code == 200:
        return resp.json()["access_token"]
    print(f"[ERROR] Login fallido: {resp.text}")
    return None

def verify_balance():
    init_db()
    crear_datos_prueba()
    
    token = get_token()
    if not token:
        return
        
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n[1] Consultando balance 2024...")
    resp = client.get("/api/empleados/balance/2024", headers=headers)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"  [OK] Respuesta recibida: {data}")
        
        expected_hours = 41.0
        if data["total_horas_trabajadas"] == expected_hours:
            print("  [OK] Cálculo de horas correcto (41h).")
        else:
            print(f"  [ERROR] Horas incorrectas. Esperado {expected_hours}, Recibido {data['total_horas_trabajadas']}")
            
        if data["dias_trabajados"] == 4:
             print("  [OK] Días trabajados correctos (4).")
        else:
             print(f"  [ERROR] Días trabajados incorrectos. Esperado 4, Recibido {data['dias_trabajados']}")
             
    else:
        print(f"  [ERROR] Error en request: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    verify_balance()
