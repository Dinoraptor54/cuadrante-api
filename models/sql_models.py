from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="vigilante")  # coordinador, vigilante
    is_active = Column(Boolean, default=True)

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    dni = Column(String, nullable=True)
    fecha_alta = Column(String, nullable=True)
    categoria = Column(String, default="Vigilante")
    
    # Relación con turnos
    turnos = relationship("Turno", back_populates="empleado")

class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    anio = Column(Integer)
    mes = Column(Integer)
    dia = Column(Integer)
    codigo_turno = Column(String) # N, D, L, etc.
    
    empleado = relationship("Empleado", back_populates="turnos")

class ConfiguracionTurno(Base):
    __tablename__ = "config_turnos"
    
    codigo = Column(String, primary_key=True)
    descripcion = Column(String)
    horario = Column(String) # 19:00-07:00
    color = Column(String)
