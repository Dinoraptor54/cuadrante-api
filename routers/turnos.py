# -*- coding: utf-8 -*-
"""
Router de turnos
Endpoints para consultar turnos de vigilantes
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date
import json
import os
import sys

# Importar autenticación
sys.path.append('..')
from routers.auth import get_current_user

router = APIRouter()


# Modelos
class Turno(BaseModel):
    dia: int
    codigo: str
    horario: str
    es_festivo: bool = False


class CalendarioMes(BaseModel):
    anio: int
    mes: int
    vigilante: str
    turnos: List[Turno]
    total_horas: float


# Funciones auxiliares
def cargar_datos_desktop(archivo: str) -> dict:
    """Carga datos desde los JSON del proyecto desktop"""
    desktop_path = os.getenv("DESKTOP_DATA_PATH", "../../proyecto_modulo_cuadrante/datos_cuadrante")
    ruta_completa = os.path.join(desktop_path, archivo)
    
    try:
        with open(ruta_completa, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Endpoints
@router.get("/mis-turnos/{anio}/{mes}", response_model=CalendarioMes)
async def get_mis_turnos(
    anio: int,
    mes: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene los turnos del usuario actual para un mes específico
    """
    # Cargar datos
    cuadrantes = cargar_datos_desktop("cuadrantes.json")
    turnos_config = cargar_datos_desktop("turnos.json")
    
    # Buscar turnos del vigilante
    nombre_vigilante = current_user.get("nombre")
    turnos_mes = cuadrantes.get(str(anio), {}).get(str(mes), [])
    
    vigilante_data = next(
        (v for v in turnos_mes if v["nombre"] == nombre_vigilante),
        None
    )
    
    if not vigilante_data:
        return CalendarioMes(
            anio=anio,
            mes=mes,
            vigilante=nombre_vigilante,
            turnos=[],
            total_horas=0
        )
    
    # Construir lista de turnos
    turnos_lista = []
    total_horas = 0
    
    for dia_str, codigo_turno in vigilante_data.get("turnos", {}).items():
        turno_info = turnos_config.get(codigo_turno.upper(), {})
        horas = turno_info.get("trabajadas", 0)
        
        turnos_lista.append(Turno(
            dia=int(dia_str),
            codigo=codigo_turno.upper(),
            horario=turno_info.get("leyenda", ""),
            es_festivo=False  # TODO: Verificar contra festivos
        ))
        
        total_horas += horas
    
    # Ordenar por día
    turnos_lista.sort(key=lambda x: x.dia)
    
    return CalendarioMes(
        anio=anio,
        mes=mes,
        vigilante=nombre_vigilante,
        turnos=turnos_lista,
        total_horas=total_horas
    )


@router.get("/calendario/{anio}/{mes}")
async def get_calendario_completo(
    anio: int,
    mes: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene el calendario completo del mes (solo coordinadores)
    """
    if current_user.get("rol") != "coordinador":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    cuadrantes = cargar_datos_desktop("cuadrantes.json")
    turnos_mes = cuadrantes.get(str(anio), {}).get(str(mes), [])
    
    return {
        "anio": anio,
        "mes": mes,
        "vigilantes": turnos_mes
    }


@router.get("/proximos-turnos")
async def get_proximos_turnos(
    dias: int = 7,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene los próximos turnos del vigilante
    """
    # TODO: Implementar lógica para obtener próximos N días
    return {
        "message": "Próximos turnos",
        "dias": dias,
        "turnos": []
    }
