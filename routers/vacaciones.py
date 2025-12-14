# -*- coding: utf-8 -*-
"""
Router de vacaciones
Endpoints para solicitar y gestionar vacaciones
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from models.database import get_db
from models import sql_models
from services import vacaciones_service, auth_service, notification_service
from routers.auth import get_current_user
from utils.validators import DateValidator

router = APIRouter()

# Modelos Pydantic
class SolicitudVacacion(BaseModel):
    fecha_inicio: str  # YYYY-MM-DD
    fecha_fin: str  # YYYY-MM-DD
    motivo: Optional[str] = None

class VacacionResponse(BaseModel):
    id: int
    fecha_inicio: str
    fecha_fin: str
    estado: str
    fecha_solicitud: datetime
    motivo: Optional[str] = None

    class Config:
        from_attributes = True

# Endpoints
@router.post("/solicitar", response_model=VacacionResponse)
async def solicitar_vacaciones(
    solicitud: SolicitudVacacion,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Solicita un periodo de vacaciones"""
    # Validar fechas
    try:
        DateValidator.validate_date_string(solicitud.fecha_inicio)
        DateValidator.validate_date_string(solicitud.fecha_fin)
        
        # Validar que inicio < fin
        start = datetime.strptime(solicitud.fecha_inicio, "%Y-%m-%d")
        end = datetime.strptime(solicitud.fecha_fin, "%Y-%m-%d")
        if start > end:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Obtener usuario
    user = auth_service.get_user_by_email(db, current_user['email'])
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Crear solicitud
    nueva_vacacion = vacaciones_service.create_solicitud(
        db,
        solicitante_id=user.id,
        fecha_inicio=solicitud.fecha_inicio,
        fecha_fin=solicitud.fecha_fin,
        motivo=solicitud.motivo
    )
    
    # Notificar creación
    notification_service.notify_vacacion_created(
        user.email,
        solicitud.fecha_inicio,
        solicitud.fecha_fin
    )

    return nueva_vacacion

@router.get("/mis-solicitudes", response_model=List[VacacionResponse])
async def get_mis_solicitudes(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene el historial de solicitudes del usuario"""
    user = auth_service.get_user_by_email(db, current_user['email'])
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return vacaciones_service.get_mis_solicitudes(db, user.id)
