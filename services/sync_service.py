# -*- coding: utf-8 -*-
"""
Servicio de Sincronización
Lógica de negocio para la sincronización de datos con el desktop.
"""

from sqlalchemy.orm import Session
from typing import Dict, Any

from models import sql_models

def sync_data(db: Session, data: Dict[str, Any]):
    """
    Sincroniza los datos del desktop con la base de datos.
    """
    try:
        # 1. Sincronizar Empleados
        for nombre, emp_data in data['empleados'].items():
            db_emp = db.query(sql_models.Empleado).filter(sql_models.Empleado.nombre_completo == nombre).first()
            if not db_emp:
                db_emp = sql_models.Empleado(
                    nombre_completo=nombre,
                    email=emp_data.get("email"),
                    telefono=emp_data.get("telefono"),
                    dni=emp_data.get("dni"),
                    fecha_alta=emp_data.get("fecha_alta")
                )
                db.add(db_emp)
            else:
                db_emp.email = emp_data.get("email")
                db_emp.telefono = emp_data.get("telefono")
        
        db.flush()

        # 2. Sincronizar Turnos
        for anio_str, meses_data in data['cuadrantes'].items():
            anio = int(anio_str)
            for mes_str, vigilantes_list in meses_data.items():
                mes = int(mes_str)
                
                for vig_data in vigilantes_list:
                    nombre = vig_data["nombre"]
                    turnos_dict = vig_data.get("turnos", {})
                    
                    empleado = db.query(sql_models.Empleado).filter(sql_models.Empleado.nombre_completo == nombre).first()
                    if not empleado:
                        continue
                    
                    db.query(sql_models.Turno).filter(
                        sql_models.Turno.empleado_id == empleado.id,
                        sql_models.Turno.anio == anio,
                        sql_models.Turno.mes == mes
                    ).delete()
                    
                    for dia_str, codigo in turnos_dict.items():
                        nuevo_turno = sql_models.Turno(
                            empleado_id=empleado.id,
                            anio=anio,
                            mes=mes,
                            dia=int(dia_str),
                            codigo_turno=codigo
                        )
                        db.add(nuevo_turno)

        # 3. Sincronizar Configuración de Turnos
        for codigo, config_data in data['config_turnos'].items():
            db_config = db.query(sql_models.ConfiguracionTurno).filter(sql_models.ConfiguracionTurno.codigo == codigo).first()
            if not db_config:
                db_config = sql_models.ConfiguracionTurno(
                    codigo=codigo,
                    descripcion=config_data.get('leyenda'),
                    horario=config_data.get('horario'),
                    color=config_data.get('color')
                )
                db.add(db_config)
            else:
                db_config.descripcion = config_data.get('leyenda')
                db_config.horario = config_data.get('horario')
                db_config.color = config_data.get('color')

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
