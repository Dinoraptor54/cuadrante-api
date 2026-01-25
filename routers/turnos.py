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

from sqlalchemy.orm import Session
from models.database import get_db
from models.sql_models import Empleado, Turno as TurnoDB, ConfiguracionTurno
from datetime import date, timedelta

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

class ProximoTurno(BaseModel):
    fecha: date
    codigo_turno: str
    descripcion: str
    horario: str
    es_festivo: bool

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
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los turnos del usuario actual para un mes específico
    """
    # 1. Intentar cargar desde DB primero (fuente de verdad sincronizada)
    nombre_vigilante = current_user.get("nombre")
    
    # Obtener configuración de turnos desde DB
    from services import empleados_service
    config_horas = empleados_service.get_horas_config(db)
    # También necesitamos la leyenda y color que están en ConfiguracionTurno
    configs_db = {c.codigo: c for c in db.query(ConfiguracionTurno).all()}
    
    # Buscar turnos del vigilante en DB
    empleado = db.query(Empleado).filter(Empleado.nombre_completo == nombre_vigilante).first()
    
    if empleado:
        turnos_db = db.query(TurnoDB).filter(
            TurnoDB.empleado_id == empleado.id,
            TurnoDB.anio == anio,
            TurnoDB.mes == mes
        ).all()
        
        if turnos_db:
            turnos_lista = []
            total_horas = 0
            for t in turnos_db:
                conf = configs_db.get(t.codigo_turno)
                
                turnos_lista.append(Turno(
                    dia=t.dia,
                    codigo=t.codigo_turno,
                    horario=conf.descripcion if conf else "",
                    es_festivo=t.es_festivo
                ))
                total_horas += t.horas_trabajadas
            
            turnos_lista.sort(key=lambda x: x.dia)
            return CalendarioMes(
                anio=anio,
                mes=mes,
                vigilante=nombre_vigilante,
                turnos=turnos_lista,
                total_horas=total_horas
            )

    # 2. Fallback a JSON (solo para desarrollo local si no hay DB)
    cuadrantes = cargar_datos_desktop("cuadrantes.json")
    turnos_config = cargar_datos_desktop("turnos.json")
    
    turnos_mes = cuadrantes.get(str(anio), {}).get(str(mes), [])
    vigilante_data = next((v for v in turnos_mes if v["nombre"] == nombre_vigilante), None)
    
    if not vigilante_data:
        return CalendarioMes(anio=anio, mes=mes, vigilante=nombre_vigilante, turnos=[], total_horas=0)
    
    turnos_lista = []
    total_horas = 0
    for dia_str, codigo_turno in vigilante_data.get("turnos", {}).items():
        turno_info = turnos_config.get(codigo_turno.upper(), {})
        horas = turno_info.get("trabajadas", 0)
        turnos_lista.append(Turno(
            dia=int(dia_str),
            codigo=codigo_turno.upper(),
            horario=turno_info.get("leyenda", ""),
            es_festivo=False
        ))
        total_horas += horas
    
    turnos_lista.sort(key=lambda x: x.dia)
    return CalendarioMes(anio=anio, mes=mes, vigilante=nombre_vigilante, turnos=turnos_lista, total_horas=total_horas)


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


from services import turnos_service
from models.sql_models import Empleado

@router.get("/proximos-turnos", response_model=List[ProximoTurno])
async def get_proximos_turnos(
    dias: int = 7,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los próximos turnos del vigilante desde la base de datos.
    """
    nombre_usuario = current_user.get("nombre")
    empleado = db.query(Empleado).filter(Empleado.nombre_completo == nombre_usuario).first()

    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    proximos_turnos = turnos_service.get_proximos_turnos_empleado(db, empleado.id, dias)
    
    return proximos_turnos
