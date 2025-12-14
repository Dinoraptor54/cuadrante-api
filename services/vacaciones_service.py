# -*- coding: utf-8 -*-
"""
Servicio de vacaciones
Lógica de negocio para gestión de solicitudes de vacaciones
"""

from sqlalchemy.orm import Session
from models import sql_models
from datetime import datetime

def create_solicitud(
    db: Session, 
    solicitante_id: int, 
    fecha_inicio: str, 
    fecha_fin: str, 
    motivo: str = None
) -> sql_models.Vacacion:
    """Crea una nueva solicitud de vacaciones"""
    nueva_vacacion = sql_models.Vacacion(
        solicitante_id=solicitante_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        motivo=motivo,
        estado="pendiente",
        fecha_solicitud=datetime.utcnow()
    )
    db.add(nueva_vacacion)
    db.commit()
    db.refresh(nueva_vacacion)
    return nueva_vacacion

def get_mis_solicitudes(db: Session, user_id: int):
    """Obtiene todas las solicitudes de un usuario"""
    return db.query(sql_models.Vacacion).filter(
        sql_models.Vacacion.solicitante_id == user_id
    ).order_by(sql_models.Vacacion.fecha_solicitud.desc()).all()

def get_solicitud_by_id(db: Session, vacacion_id: int):
    """Obtiene una solicitud por ID"""
    return db.query(sql_models.Vacacion).filter(
        sql_models.Vacacion.id == vacacion_id
    ).first()

def update_estado(db: Session, vacacion: sql_models.Vacacion, nuevo_estado: str):
    """Actualiza el estado de una solicitud"""
    vacacion.estado = nuevo_estado
    db.commit()
    db.refresh(vacacion)
    return vacacion
