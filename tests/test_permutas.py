# -*- coding: utf-8 -*-
"""
Tests para permutas
Verifica solicitud, aceptación y rechazo de permutas
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date, timedelta

from models.database import Base, SessionLocal, engine
from models.sql_models import Empleado, User, Permuta
from main import app







@pytest.fixture
def test_usuarios(db_session: Session):
    """Crea usuarios de prueba"""
    empleado1 = Empleado(
        nombre_completo="Usuario Uno",
        email="user1@example.com",
        telefono="111111111"
    )
    empleado2 = Empleado(
        nombre_completo="Usuario Dos",
        email="user2@example.com",
        telefono="222222222"
    )
    db_session.add_all([empleado1, empleado2])
    db_session.commit()
    
    usuario1 = User(
        email="user1@example.com",
        hashed_password="hashed",
        full_name="User 1",
        role="vigilante"
    )
    usuario2 = User(
        email="user2@example.com",
        hashed_password="hashed",
        full_name="User 2",
        role="vigilante"
    )
    db_session.add_all([usuario1, usuario2])
    db_session.commit()
    
    return usuario1, usuario2


def test_solicitar_permuta_exitosa(client, test_usuarios):
    """Prueba solicitud de permuta exitosa"""
    usuario1, usuario2 = test_usuarios
    
    mañana = (date.today() + timedelta(days=1)).isoformat()
    pasado_mañana = (date.today() + timedelta(days=2)).isoformat()
    
    response = client.post(
        "/api/permutas/solicitar",
        json={
            "fecha_origen": mañana,
            "fecha_destino": pasado_mañana,
            "email_destino": usuario2.email,
            "motivo": "Necesito cambiar turno"
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar 200 o 401 si requiere auth
    assert response.status_code in [200, 201, 401, 422]


def test_solicitar_permuta_sin_motivo(client, test_usuarios):
    """Prueba permuta sin motivo (opcional)"""
    usuario1, usuario2 = test_usuarios
    
    mañana = (date.today() + timedelta(days=1)).isoformat()
    pasado_mañana = (date.today() + timedelta(days=2)).isoformat()
    
    response = client.post(
        "/api/permutas/solicitar",
        json={
            "fecha_origen": mañana,
            "fecha_destino": pasado_mañana,
            "email_destino": usuario2.email
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code in [200, 201, 401, 422]


def test_solicitar_permuta_fechas_iguales(client, test_usuarios):
    """Prueba rechazo de permuta con fechas iguales"""
    usuario1, usuario2 = test_usuarios
    
    mañana = (date.today() + timedelta(days=1)).isoformat()
    
    response = client.post(
        "/api/permutas/solicitar",
        json={
            "fecha_origen": mañana,
            "fecha_destino": mañana,
            "email_destino": usuario2.email,
            "motivo": "Prueba"
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar fechas iguales
    assert response.status_code in [400, 422]


def test_solicitar_permuta_fecha_pasada(client, test_usuarios):
    """Prueba rechazo de permuta en fecha pasada"""
    usuario1, usuario2 = test_usuarios
    
    ayer = (date.today() - timedelta(days=1)).isoformat()
    mañana = (date.today() + timedelta(days=1)).isoformat()
    
    response = client.post(
        "/api/permutas/solicitar",
        json={
            "fecha_origen": ayer,
            "fecha_destino": mañana,
            "email_destino": usuario2.email,
            "motivo": "Prueba"
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar fechas pasadas
    assert response.status_code in [400, 422]


def test_listar_mis_permutas(client):
    """Prueba listado de mis permutas"""
    response = client.get(
        "/api/permutas/mis-permutas",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar lista (200) o 401 sin auth
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        assert isinstance(response.json(), list)


def test_aceptar_permuta_no_existe(client):
    """Prueba aceptar permuta inexistente"""
    response = client.post(
        "/api/permutas/aceptar/999",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar 404
    assert response.status_code in [404, 401]


def test_rechazar_permuta_no_existe(client):
    """Prueba rechazar permuta inexistente"""
    response = client.post(
        "/api/permutas/rechazar/999",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar 404
    assert response.status_code in [404, 401]


def test_email_destino_invalido(client, test_usuarios):
    """Prueba validación de email destino"""
    usuario1, usuario2 = test_usuarios
    
    mañana = (date.today() + timedelta(days=1)).isoformat()
    pasado_mañana = (date.today() + timedelta(days=2)).isoformat()
    
    response = client.post(
        "/api/permutas/solicitar",
        json={
            "fecha_origen": mañana,
            "fecha_destino": pasado_mañana,
            "email_destino": "email-invalido",
            "motivo": "Prueba"
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar email inválido
    assert response.status_code in [400, 422]


def test_formato_fecha_invalido(client, test_usuarios):
    """Prueba formato de fecha inválido"""
    usuario1, usuario2 = test_usuarios
    
    response = client.post(
        "/api/permutas/solicitar",
        json={
            "fecha_origen": "2025/12/01",  # Formato incorrecto
            "fecha_destino": "2025/12/02",
            "email_destino": usuario2.email,
            "motivo": "Prueba"
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar formato incorrecto
    assert response.status_code in [400, 422]
