# -*- coding: utf-8 -*-
"""
Tests para vacaciones
Verifica solicitud y listado de vacaciones
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date, timedelta

from models.database import Base, SessionLocal, engine, get_db
from models.sql_models import Empleado, User, Vacacion
from main import app
from routers.auth import get_current_user

# Override auth dependency
async def mock_get_current_user():
    return {"email": "user1@example.com", "nombre": "Usuario Uno", "rol": "vigilante"}

app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

@pytest.fixture
def db_session():
    """Crea una sesión de BD de prueba"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Override get_db to use this session
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
    
    # Remove override
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_user(db_session: Session):
    """Crea un usuario de prueba"""
    usuario = User(
        email="user1@example.com",
        hashed_password="hashed",
        full_name="Usuario Uno",
        role="vigilante"
    )
    db_session.add(usuario)
    db_session.commit()
    return usuario

def test_solicitar_vacaciones_exitosas(test_user):
    """Prueba solicitud de vacaciones exitosa"""
    mañana = (date.today() + timedelta(days=1)).isoformat()
    pasado_mañana = (date.today() + timedelta(days=5)).isoformat()
    
    response = client.post(
        "/api/vacaciones/solicitar",
        json={
            "fecha_inicio": mañana,
            "fecha_fin": pasado_mañana,
            "motivo": "Vacaciones de verano"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fecha_inicio"] == mañana
    assert data["fecha_fin"] == pasado_mañana
    assert data["estado"] == "pendiente"

def test_solicitar_vacaciones_fechas_invalidas(test_user):
    """Prueba rechazo cuando inicio > fin"""
    mañana = (date.today() + timedelta(days=1)).isoformat()
    ayer = (date.today() - timedelta(days=1)).isoformat()
    
    response = client.post(
        "/api/vacaciones/solicitar",
        json={
            "fecha_inicio": mañana,
            "fecha_fin": ayer,
            "motivo": "Fechas mal"
        }
    )
    assert response.status_code == 400

def test_solicitar_vacaciones_formato_invalido(test_user):
    """Prueba rechazo de formato de fecha inválido"""
    response = client.post(
        "/api/vacaciones/solicitar",
        json={
            "fecha_inicio": "2025/01/01",
            "fecha_fin": "2025/01/05",
            "motivo": "Formato mal"
        }
    )
    assert response.status_code == 422

def test_listar_mis_solicitudes(test_user, db_session):
    """Prueba listado de solicitudes"""
    # Crear una solicitud previa
    vacacion = Vacacion(
        solicitante_id=test_user.id,
        fecha_inicio="2025-08-01",
        fecha_fin="2025-08-15",
        estado="pendiente"
    )
    db_session.add(vacacion)
    db_session.commit()
    
    response = client.get("/api/vacaciones/mis-solicitudes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["fecha_inicio"] == "2025-08-01"
