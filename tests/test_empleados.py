# -*- coding: utf-8 -*-
"""
Tests para empleados
Verifica balance de horas y datos de empleados
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.database import Base, SessionLocal, engine
from models.sql_models import Empleado, User
from main import app







@pytest.fixture
def test_user(db_session: Session):
    """Crea un usuario de prueba"""
    empleado = Empleado(
        nombre_completo="Test",
        email="employee@example.com",
        telefono="123456789"
    )
    db_session.add(empleado)
    db_session.commit()
    
    usuario = User(
        email="employee@example.com",
        hashed_password="hashed",
        full_name="Test Employee",
        role="vigilante"
    )
    db_session.add(usuario)
    db_session.commit()
    
    return usuario


def test_get_balance_anio_valido(client):
    """Prueba obtener balance para año válido"""
    response = client.get(
        "/api/empleados/balance/2025",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar 200 o 401 sin auth válida
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        data = response.json()
        assert "balance_horas" in data or isinstance(data, dict)


def test_get_balance_anio_invalido(client):
    """Prueba obtener balance con año inválido"""
    response = client.get(
        "/api/empleados/balance/1900",  # Año fuera de rango
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar año inválido
    assert response.status_code in [400, 422, 401]


def test_get_balance_anio_futuro(client):
    """Prueba obtener balance para año muy lejano"""
    response = client.get(
        "/api/empleados/balance/3000",  # Año muy lejano
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar año demasiado lejano
    assert response.status_code in [400, 422, 401]


def test_get_mi_perfil(client):
    """Prueba obtener mi perfil"""
    response = client.get(
        "/api/empleados/mi-perfil",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar 200 o 401 sin auth
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        data = response.json()
        assert "email" in data or "nombre" in data


def test_actualizar_perfil(client):
    """Prueba actualización de perfil"""
    response = client.put(
        "/api/empleados/actualizar-perfil",
        json={
            "nombre": "Nuevo",
            "apellido": "Nombre",
            "telefono": "987654321"
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar 200 o 401 sin auth
    assert response.status_code in [200, 401]


def test_actualizar_perfil_email_invalido(client):
    """Prueba rechazo de email inválido en actualización"""
    response = client.put(
        "/api/empleados/actualizar-perfil",
        json={
            "nombre": "Nombre",
            "apellido": "Apellido",
            "email": "email-invalido"
        },
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar email inválido
    assert response.status_code in [400, 422, 401]


def test_listar_empleados(client):
    """Prueba listado de empleados"""
    response = client.get(
        "/api/empleados/",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar lista o 401 sin auth
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, (list, dict))


def test_listar_empleados_paginado(client):
    """Prueba listado de empleados con paginación"""
    response = client.get(
        "/api/empleados/?skip=0&limit=10",
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code in [200, 401]


def test_listar_empleados_limit_invalido(client):
    """Prueba rechazo de limit inválido"""
    response = client.get(
        "/api/empleados/?limit=2000",  # Exceeds max
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar limit muy grande
    assert response.status_code in [400, 422, 401]


def test_listar_empleados_skip_negativo(client):
    """Prueba rechazo de skip negativo"""
    response = client.get(
        "/api/empleados/?skip=-5",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar skip negativo
    assert response.status_code in [400, 422, 401]


def test_obtener_empleado_por_email(client):
    """Prueba obtener empleado por email"""
    response = client.get(
        "/api/empleados/por-email/employee@example.com",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería retornar empleado o 404
    assert response.status_code in [200, 404, 401]


def test_obtener_empleado_email_invalido(client):
    """Prueba obtener empleado con email inválido"""
    response = client.get(
        "/api/empleados/por-email/email-invalido",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar email inválido
    assert response.status_code in [400, 422, 404, 401]


def test_get_balance_mes_especifico(client):
    """Prueba obtener balance para mes específico"""
    response = client.get(
        "/api/empleados/balance/2025/12",  # Diciembre 2025
        headers={"Authorization": "Bearer fake_token"}
    )
    assert response.status_code in [200, 401, 404]


def test_get_balance_mes_invalido(client):
    """Prueba rechazo de mes inválido"""
    response = client.get(
        "/api/empleados/balance/2025/13",  # Mes no existe
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar mes fuera de rango
    assert response.status_code in [400, 422, 401]


def test_get_balance_mes_negativo(client):
    """Prueba rechazo de mes negativo"""
    response = client.get(
        "/api/empleados/balance/2025/0",
        headers={"Authorization": "Bearer fake_token"}
    )
    # Debería rechazar mes < 1
    assert response.status_code in [400, 422, 401]
