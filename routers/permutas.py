# -*- coding: utf-8 -*-
"""
Router de permutas
Endpoints para solicitar y gestionar cambios de turno
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys

sys.path.append('..')
from routers.auth import get_current_user

router = APIRouter()


# Modelos
class SolicitudPermuta(BaseModel):
    dia_origen: int
    dia_destino: int
    vigilante_destino: str
    motivo: Optional[str] = None


class Permuta(BaseModel):
    id: int
    solicitante: str
    vigilante_destino: str
    dia_origen: int
    dia_destino: int
    estado: str  # pending, accepted, rejected
    fecha_solicitud: datetime
    motivo: Optional[str] = None


# Endpoints
@router.post("/solicitar")
async def solicitar_permuta(
    solicitud: SolicitudPermuta,
    current_user: dict = Depends(get_current_user)
):
    """
    Solicita una permuta de turno
    """
    # TODO: Guardar en base de datos
    return {
        "message": "Permuta solicitada correctamente",
        "permuta_id": 1,
        "status": "pending"
    }


@router.get("/mis-solicitudes", response_model=List[Permuta])
async def get_mis_solicitudes(current_user: dict = Depends(get_current_user)):
    """
    Obtiene las permutas solicitadas por el usuario
    """
    # TODO: Consultar base de datos
    return []


@router.get("/pendientes", response_model=List[Permuta])
async def get_permutas_pendientes(current_user: dict = Depends(get_current_user)):
    """
    Obtiene permutas pendientes que involucran al usuario
    """
    # TODO: Consultar base de datos
    return []


@router.put("/{permuta_id}/aceptar")
async def aceptar_permuta(
    permuta_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Acepta una permuta pendiente
    """
    # TODO: Actualizar en base de datos
    return {"message": "Permuta aceptada", "permuta_id": permuta_id}


@router.put("/{permuta_id}/rechazar")
async def rechazar_permuta(
    permuta_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Rechaza una permuta pendiente
    """
    # TODO: Actualizar en base de datos
    return {"message": "Permuta rechazada", "permuta_id": permuta_id}
