from sqlalchemy.orm import Session
from models import sql_models
from typing import Dict, Any

def get_horas_config(db: Session) -> Dict[str, Dict[str, float]]:
    """
    Obtiene la configuración de horas de todos los turnos desde la base de datos.
    """
    configs = db.query(sql_models.ConfiguracionTurno).all()
    return {c.codigo: {"total": c.horas_total, "nocturnas": c.horas_nocturnas} for c in configs}

def get_horas_turno(codigo: str, config_mapping: Dict[str, Dict[str, float]] = None) -> float:
    """
    Devuelve las horas estimadas para un código de turno.
    Utiliza el mapeo proporcionado (de la BD) o valores por defecto si no existe.
    """
    if config_mapping and codigo in config_mapping:
        return config_mapping[codigo]["total"]
    
    # Fallback por compatibilidad o códigos no configurados
    mapping = {
        "N": 12.0, "D": 12.0, "V": 0.0, "L": 0.0, "B": 0.0, "F": 0.0, "R": 5.0
    }
    return mapping.get(codigo, 0.0)

def get_horas_nocturnas(codigo: str, config_mapping: Dict[str, Dict[str, float]] = None) -> float:
    """
    Devuelve las horas nocturnas para un código de turno.
    """
    if config_mapping and codigo in config_mapping:
        return config_mapping[codigo]["nocturnas"]
        
    mapping = {
        "N": 8.0, "D": 0.0, "V": 0.0, "L": 0.0, "B": 0.0, "F": 0.0, "R": 0.0
    }
    return mapping.get(codigo, 0.0)

def calcular_balance_anual(db: Session, empleado_id: int, anio: int) -> Dict[str, Any]:
    """
    Calcula el balance de horas para un empleado en un año específico.
    Utiliza los campos pre-calculados por el escritorio.
    """
    # 1. Obtener turnos del año
    turnos = db.query(sql_models.Turno).filter(
        sql_models.Turno.empleado_id == empleado_id,
        sql_models.Turno.anio == anio
    ).all()
    
    total_horas = sum(t.horas_trabajadas for t in turnos)
    dias_trabajados = sum(1 for t in turnos if t.horas_trabajadas > 0)
    dias_vacaciones = sum(1 for t in turnos if t.codigo_turno == "V")
    dias_baja = sum(1 for t in turnos if t.codigo_turno == "B")
    
    # 3. Calcular esperadas (1768 horas anuales convenio)
    horas_convenio = 1768.0
    balance = total_horas - horas_convenio
    
    return {
        "anio": anio,
        "total_horas_trabajadas": total_horas,
        "horas_convenio": horas_convenio,
        "balance_horas": balance,
        "dias_trabajados": dias_trabajados,
        "dias_vacaciones": dias_vacaciones,
        "dias_baja": dias_baja
    }
