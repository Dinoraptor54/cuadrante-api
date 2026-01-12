# -*- coding: utf-8 -*-
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models.database import Base, get_db

# --- Configuración de la base de datos de prueba ---
# --- Configuración de la base de datos de prueba ---
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Sobrescribir la dependencia de la base de datos ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# --- Fixtures de Pytest ---
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Se ejecuta una vez por sesión de prueba para crear y destruir la BD."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Proporciona una sesión de BD limpia para cada función de prueba."""
    db = TestingSessionLocal()
    # Limpiar tablas antes de cada prueba
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Crea un TestClient con la sesión de BD de prueba para cada test."""
    def override_get_db_for_client():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db_for_client
    with TestClient(app) as c:
        yield c
    # Restaurar la dependencia original
    app.dependency_overrides[get_db] = get_db
