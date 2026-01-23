from sqlalchemy.orm import Session
from models import sql_models
from typing import Dict, Any

def get_horas_turno(codigo: str) -> float:
    """
    Devuelve las horas estimadas para un código de turno.
    TODO: Esto debería venir de la base de datos o configuración.
    """
    mapping = {
        "N": 12.0, # Noche: segun turnos.json son 12h (con 8h nocturnas)
        "D": 12.0, # Dia: 12h
        "V": 5.0,  # Vacaciones: segun turnos.json cuentan como 5h
        "L": 0.0,  # Libre
        "B": 0.0,  # Baja
        "F": 0.0,  # Formacion
        "R": 5.0   # Rotativo/Mixto (segun turnos.json 5h trab + 5h noct = 10? No, 'trabajadas': 5. Asumiremos 5h de trabajo efectivo por ahora, aunque R suele ser complejo)
    }
    # Nota: M y T no aparecen en turnos.json, se asumen 0 o se eliminan.
    return mapping.get(codigo, 0.0)

def get_horas_nocturnas(codigo: str) -> float:
    """
    Devuelve las horas nocturnas para un código de turno.
    Según turnos.json, solo el turno N tiene horas nocturnas (8h).
    """
    mapping = {
        "N": 8.0,  # Turno noche: 8 horas nocturnas (de 19:00 a 07:00)
        "D": 0.0,  # Turno día: sin horas nocturnas
        "V": 0.0,  # Vacaciones
        "L": 0.0,  # Libre
        "B": 0.0,  # Baja
        "F": 0.0,  # Formación
        "R": 0.0   # Rotativo
    }
    return mapping.get(codigo, 0.0)

def calcular_balance_anual(db: Session, empleado_id: int, anio: int) -> Dict[str, Any]:
    """
    Calcula el balance de horas para un empleado en un año específico.
    """
    # 1. Obtener turnos del año
    turnos = db.query(sql_models.Turno).filter(
        sql_models.Turno.empleado_id == empleado_id,
        sql_models.Turno.anio == anio
    ).all()
    
    total_horas = 0.0
    dias_trabajados = 0
    dias_vacaciones = 0
    dias_baja = 0
    
    # 2. Iterar y sumar
    for t in turnos:
        codigo = t.codigo_turno
        
        # Sumar horas (básico)
        horas = get_horas_turno(codigo)
        total_horas += horas
        
        if horas > 0:
            dias_trabajados += 1
            
        if codigo == "V":
            dias_vacaciones += 1
        elif codigo == "B":
            dias_baja += 1
            
    # 3. Calcular esperadas (Simplificado: 1768 horas anuales convenio aprox)
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
