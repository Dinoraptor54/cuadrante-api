# -*- coding: utf-8 -*-
from datetime import date
from models.sql_models import Empleado, Turno, ConfiguracionTurno

# --- Datos de prueba ---
TEST_USER = {
    "email": "turnos.test@example.com",
    "password": "testpassword",
    "full_name": "Test User",
    "role": "vigilante"
}
TEST_EMPLEADO = {
    "nombre_completo": "Test User",
    "email": "turnos.test@example.com"
}

# --- Tests ---
def test_get_proximos_turnos_unauthenticated(client):
    """Verifica que el endpoint requiere autenticación."""
    response = client.get("/api/turnos/proximos-turnos")
    assert response.status_code == 401 # Unauthorized

def test_get_proximos_turnos_success(client, db_session):
    """Prueba el flujo completo: crear usuario, loguearse y pedir próximos turnos."""
    # 1. Crear usuario y empleado de prueba
    from services.auth_service import create_user
    create_user(db_session, TEST_USER)
    empleado_db = Empleado(**TEST_EMPLEADO)
    db_session.add(empleado_db)
    db_session.commit()
    db_session.refresh(empleado_db)

    # 2. Crear turnos de prueba para el empleado
    hoy = date.today()
    turno_manana = Turno(empleado_id=empleado_db.id, anio=hoy.year, mes=hoy.month, dia=hoy.day, codigo_turno="M")
    db_session.add(turno_manana)
    
    config_m = ConfiguracionTurno(codigo="M", descripcion="Mañana", horario="07:00-19:00", color="#FFFFFF")
    db_session.add(config_m)
    db_session.commit()

    # 3. Iniciar sesión para obtener el token
    login_response = client.post(
        "/api/auth/login",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Llamar al endpoint de próximos turnos
    response = client.get("/api/turnos/proximos-turnos?dias=1", headers=headers)
    
    # 5. Verificar la respuesta
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    
    turno_recibido = data[0]
    assert turno_recibido["fecha"] == hoy.isoformat()
    assert turno_recibido["codigo_turno"] == "M"
    assert turno_recibido["descripcion"] == "Mañana"

