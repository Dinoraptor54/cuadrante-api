from sqlalchemy.orm import Session
from models import sql_models
from datetime import datetime
from typing import List, Optional

def create_permuta(
    db: Session, 
    solicitante_id: int, 
    receptor_id: int, 
    fecha_origen: str, 
    fecha_destino: str, 
    motivo: str = None
) -> sql_models.Permuta:
    """Crea una nueva solicitud de permuta"""
    permuta = sql_models.Permuta(
        solicitante_id=solicitante_id,
        receptor_id=receptor_id,
        fecha_origen=fecha_origen,
        fecha_destino=fecha_destino,
        motivo=motivo,
        estado="pendiente",
        fecha_solicitud=datetime.utcnow()
    )
    db.add(permuta)
    db.commit()
    db.refresh(permuta)
    return permuta

def get_permutas_by_user(db: Session, user_id: int) -> List[sql_models.Permuta]:
    """Obtiene permutas donde el usuario es solicitante o receptor"""
    return db.query(sql_models.Permuta).filter(
        (sql_models.Permuta.solicitante_id == user_id) | 
        (sql_models.Permuta.receptor_id == user_id)
    ).all()

def get_permutas_pendientes(db: Session, user_id: int) -> List[sql_models.Permuta]:
    """Obtiene permutas pendientes recibidas por el usuario"""
    return db.query(sql_models.Permuta).filter(
        sql_models.Permuta.receptor_id == user_id,
        sql_models.Permuta.estado == "pendiente"
    ).all()

def get_permuta_by_id(db: Session, permuta_id: int) -> Optional[sql_models.Permuta]:
    """Busca permuta por ID"""
    return db.query(sql_models.Permuta).filter(sql_models.Permuta.id == permuta_id).first()

def update_permuta_status(db: Session, permuta: sql_models.Permuta, nuevo_estado: str):
    """Actualiza el estado de una permuta"""
    permuta.estado = nuevo_estado
    db.commit()
    db.refresh(permuta)
    return permuta

def get_all_permutas(db: Session) -> List[sql_models.Permuta]:
    """Obtiene todas las permutas (para modo administrador)"""
    return db.query(sql_models.Permuta).order_by(sql_models.Permuta.fecha_solicitud.desc()).all()
