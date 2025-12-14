import sys
import os

# Add the parent directory to sys.path to resolve 'main' and other modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import sql_models, database
from utils import security
from main import app  # Import your FastAPI app

# Configuración DB para asegurar tablas
DATABASE_URL = database.SQLALCHEMY_DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

def init_db():
    print("[*] Asegurando esquema de base de datos...")
    sql_models.Base.metadata.create_all(bind=engine)

def crear_usuarios_test():
    db = SessionLocal()
    
    users = [
        {"email": "user1@test.com", "pass": "pass1", "name": "Usuario Uno"},
        {"email": "user2@test.com", "pass": "pass2", "name": "Usuario Dos"}
    ]
    
    for u in users:
        existing = db.query(sql_models.User).filter(sql_models.User.email == u["email"]).first()
        if not existing:
            print(f"[*] Creando usuario test: {u['email']}")
            new_user = sql_models.User(
                email=u["email"],
                hashed_password=security.get_password_hash(u["pass"]),
                full_name=u["name"],
                role="vigilante",
                is_active=True
            )
            db.add(new_user)
    
    db.commit()
    db.close()

def get_token(email, password):
    resp = client.post("/api/auth/login", data={"username": email, "password": password})
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None

def verify_permutas():
    # 1. Setup
    init_db()
    crear_usuarios_test()
    
    token1 = get_token("user1@test.com", "pass1")
    token2 = get_token("user2@test.com", "pass2")
    
    if not token1 or not token2:
        print("  [ERROR] Error: No se pudieron obtener tokens para los usuarios de prueba.")
        return

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # 2. User 1 solicita permuta a User 2
    print("\n[1] Solicitando permuta (User1 -> User2)...")
    payload = {
        "fecha_origen": "2023-12-01",
        "fecha_destino": "2023-12-02",
        "email_destino": "user2@test.com",
        "motivo": "Cambio por asunto personal"
    }
    
    resp = client.post("/api/permutas/solicitar", json=payload, headers=headers1)
    if resp.status_code == 200:
        data = resp.json()
        permuta_id = data["id"]
        print(f"  [OK] Permuta creada ID: {permuta_id}")
    else:
        print(f"  [ERROR] Error al crear permuta: {resp.text}")
        return

    # 3. User 2 verifica sus solicitudes pendientes
    print("\n[2] User 2 revisando pendientes...")
    resp = client.get("/api/permutas/pendientes", headers=headers2)
    pendientes = resp.json()
    
    found = False
    for p in pendientes:
        if p["id"] == permuta_id:
            found = True
            print(f"  [OK] Solicitud encontrada en pendientes de User 2: {p}")
            break
            
    if not found:
        print("  [ERROR] La solicitud no aparece en pendientes del receptor.")
        return

    # 4. User 2 acepta la permuta
    print("\n[3] User 2 aceptando permuta...")
    resp = client.put(f"/api/permutas/{permuta_id}/aceptar", headers=headers2)
    
    if resp.status_code == 200:
        data = resp.json()
        if data["estado"] == "aceptada":
            print(f"  [OK] Permuta aceptada correctamente. Estado: {data['estado']}")
        else:
            print(f"  [WARN] Aviso: Estado inesperado: {data['estado']}")
    else:
        print(f"  [ERROR] Error al aceptar permuta: {resp.text}")

    # 5. Verificar estado final
    print("\n[4] Verificando estado final (User 1)...")
    resp = client.get("/api/permutas/mis-solicitudes", headers=headers1)
    mis_solicitudes = resp.json()
    
    for p in mis_solicitudes:
        if p["id"] == permuta_id:
            print(f"Estado final visto por User 1: {p['estado']}")
            if p["estado"] == "aceptada":
                print("  [OK] Flujo completo de permuta EXITOSO.")
            else:
                print("  [ERROR] El estado final no es 'aceptada'.")

if __name__ == "__main__":
    verify_permutas()
