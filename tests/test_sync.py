# -*- coding: utf-8 -*-
from models.sql_models import Empleado, Turno, ConfiguracionTurno

# --- Datos de prueba ---
TEST_COORDINADOR = {
    "email": "coord.test@example.com",
    "password": "testpassword",
    "full_name": "Coordinador Test",
    "role": "coordinador"
}

SYNC_DATA = {
    "empleados": {
        "Empleado Sync 1": {
            "email": "sync1@example.com",
            "telefono": "600111222",
            "dni": "11111111A",
            "fecha_alta": "2024-01-01"
        }
    },
    "cuadrantes": {
        "2025": {
            "12": [
                {
                    "nombre": "Empleado Sync 1",
                    "turnos": {
                        "6": "N",
                        "7": "L"
                    }
                }
            ]
        }
    },
    "config_turnos": {
        "N": {
            "leyenda": "Noche",
            "horario": "19:00-07:00",
            "color": "#0000FF"
        },
        "L": {
            "leyenda": "Libre",
            "horario": "00:00-00:00",
            "color": "#FFFFFF"
        }
    }
}

# --- Tests ---
def test_sync_unauthenticated(client):
    """Verifica que el endpoint de sync requiere autenticación de coordinador."""
    response = client.post("/api/sync/full", json=SYNC_DATA)
    assert response.status_code == 401 # Unauthorized

def test_sync_not_a_coordinator(client, db_session):
    """Verifica que un usuario no coordinador no puede sincronizar."""
    # 1. Crear usuario no coordinador
    from services.auth_service import create_user
    from tests.test_turnos import TEST_USER
    create_user(db_session, TEST_USER)
    
    # 2. Loguearse como no coordinador
    login_response = client.post(
        "/api/auth/login",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Intentar sincronizar
    response = client.post("/api/sync/full", json=SYNC_DATA, headers=headers)
    assert response.status_code == 403 # Forbidden

def test_full_sync_success(client, db_session):
    """
    Prueba una sincronización completa exitosa:
    - Crea empleados nuevos.
    - Crea turnos nuevos.
    - Crea configuración de turnos nueva.
    """
    # 1. Crear usuario coordinador y loguearse
    from services.auth_service import create_user
    create_user(db_session, TEST_COORDINADOR)
    
    login_response = client.post(
        "/api/auth/login",
        data={"username": TEST_COORDINADOR["email"], "password": TEST_COORDINADOR["password"]}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Enviar datos de sincronización
    response = client.post("/api/sync/full", json=SYNC_DATA, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Sincronización completada"}

    # 3. Verificar que los datos se han escrito en la BD
    # Verificar empleado
    empleado = db_session.query(Empleado).filter(Empleado.nombre_completo == "Empleado Sync 1").first()
    assert empleado is not None
    assert empleado.email == "sync1@example.com"
    
    # Verificar turnos
    turnos = db_session.query(Turno).filter(Turno.empleado_id == empleado.id).all()
    assert len(turnos) == 2
    
    turno_noche = db_session.query(Turno).filter(Turno.dia == 6).first()
    assert turno_noche is not None
    assert turno_noche.codigo_turno == "N"
    
    turno_libre = db_session.query(Turno).filter(Turno.dia == 7).first()
    assert turno_libre is not None
    assert turno_libre.codigo_turno == "L"
    
    # Verificar config de turnos
    config_n = db_session.query(ConfiguracionTurno).filter(ConfiguracionTurno.codigo == "N").first()
    assert config_n is not None
    assert config_n.descripcion == "Noche"
