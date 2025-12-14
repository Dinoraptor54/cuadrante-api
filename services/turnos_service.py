# -*- coding: utf-8 -*-
"""
Servicio de Turnos
Lógica de negocio para operaciones relacionadas con turnos.
"""

from sqlalchemy.orm import Session
from datetime import date, timedelta
import json
import os
from typing import List, Dict

from models.sql_models import Empleado, Turno as TurnoDB, ConfiguracionTurno
from routers.turnos import ProximoTurno


def cargar_datos_desktop(archivo: str) -> dict:
    """Carga datos desde los JSON del proyecto desktop"""
    desktop_path = os.getenv("DESKTOP_DATA_PATH", "../../proyecto_modulo_cuadrante/datos_cuadrante")
    ruta_completa = os.path.join(desktop_path, archivo)
    
    try:
        with open(ruta_completa, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_proximos_turnos_empleado(db: Session, empleado_id: int, dias: int) -> List[ProximoTurno]:
    """
    Obtiene los próximos turnos de un empleado desde la base de datos.
    """
    hoy = date.today()
    
    # Cargar festivos
    festivos_data = cargar_datos_desktop("festivos.json")
    festivos_nacionales = festivos_data.get("nacional", {})
    festivos_comunidad = festivos_data.get("comunidad", {})
    festivos_locales = festivos_data.get("local", {})

    turnos_db = db.query(TurnoDB).filter(
        TurnoDB.empleado_id == empleado_id,
        TurnoDB.anio >= hoy.year,
    ).all()
    
    turnos_config = {t.codigo: t for t in db.query(ConfiguracionTurno).all()}

    proximos_turnos = []
    for i in range(dias + 1):
        fecha_actual = hoy + timedelta(days=i)
        
        # Comprobar si es festivo
        fecha_str = fecha_actual.strftime("%m-%d")
        es_festivo = (
            fecha_str in festivos_nacionales or
            fecha_str in festivos_comunidad or
            fecha_str in festivos_locales
        )
        
        turno_en_fecha = next((t for t in turnos_db if t.anio == fecha_actual.year and t.mes == fecha_actual.month and t.dia == fecha_actual.day), None)

        if turno_en_fecha:
            config_turno = turnos_config.get(turno_en_fecha.codigo_turno)
            if config_turno:
                # Usar el modelo Pydantic directamente para construir el objeto
                proximos_turnos.append(ProximoTurno(
                    fecha=fecha_actual,
                    codigo_turno=turno_en_fecha.codigo_turno,
                    descripcion=config_turno.descripcion,
                    horario=config_turno.horario,
                    es_festivo=es_festivo
                ))

    return sorted(proximos_turnos, key=lambda t: t.fecha)
