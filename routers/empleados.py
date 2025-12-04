# -*- coding: utf-8 -*-
"""
Router de empleados
Endpoints para consultar información de empleados
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import sys

sys.path.append('..')
from routers.auth import get_current_user
from routers.turnos import cargar_datos_desktop

router = APIRouter()


# Modelos
class PerfilEmpleado(BaseModel):
    nombre: str
    email: str
    categoria: str
    fecha_alta: Optional[str] = None
    telefono: Optional[str] = None


# Endpoints
@router.get("/perfil", response_model=PerfilEmpleado)
async def get_perfil(current_user: dict = Depends(get_current_user)):
    """
    Obtiene el perfil del empleado actual
    """
    empleados = cargar_datos_desktop("empleados.json")
    nombre = current_user.get("nombre")
    
    empleado_data = empleados.get(nombre, {})
    
    return PerfilEmpleado(
        nombre=nombre,
        email=empleado_data.get("email", current_user.get("email")),
        categoria=empleado_data.get("categoria", "Vigilante de Seguridad"),
        fecha_alta=empleado_data.get("fecha_alta"),
        telefono=empleado_data.get("telefono")
    )


@router.get("/balance/{anio}")
async def get_balance_anual(
    anio: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene el balance de horas del año
    """
    # TODO: Calcular balance desde cuadrantes
    return {
        "anio": anio,
        "total_horas": 0,
        "horas_extra": 0,
        "dias_ausencia": 0
    }
