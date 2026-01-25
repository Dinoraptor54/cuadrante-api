# -*- coding: utf-8 -*-
"""
Servicio de Sincronización
Lógica de negocio para la sincronización de datos con el desktop.
"""

from sqlalchemy.orm import Session
from typing import Dict, Any

from models import sql_models
from utils.security import get_password_hash

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
            
            # 1.1 Sincronizar Usuarios y Contraseñas
            email = emp_data.get("email")
            web_password = emp_data.get("web_password")
            
            if email and web_password:
                db_user = db.query(sql_models.User).filter(sql_models.User.email == email).first()
                hashed_pw = get_password_hash(web_password)
                
                if not db_user:
                    db_user = sql_models.User(
                        email=email,
                        hashed_password=hashed_pw,
                        full_name=nombre,
                        role="vigilante",
                        is_active=True
                    )
                    db.add(db_user)
                else:
                    db_user.hashed_password = hashed_pw
                    db_user.full_name = nombre # Asegurar nombre sincronizado 
        
        db.flush()

        # 2. Sincronizar Turnos (Optimizado)
        # Pre-cargar empleados para evitar miles de SELECT
        all_emps = {e.nombre_completo: e.id for e in db.query(sql_models.Empleado).all()}
        
        for anio_str, meses_data in data['cuadrantes'].items():
            anio = int(float(anio_str))
            for mes_str, vigilantes_list in meses_data.items():
                if not mes_str.replace('.', '').isdigit():
                    continue
                mes = int(float(mes_str))
                
                for vig_data in vigilantes_list:
                    nombre = vig_data["nombre"]
                    emp_id = all_emps.get(nombre)
                    if not emp_id: continue
                    
                    # Eliminar antiguos del mes de un plumazo
                    db.query(sql_models.Turno).filter(
                        sql_models.Turno.empleado_id == emp_id,
                        sql_models.Turno.anio == anio,
                        sql_models.Turno.mes == mes
                    ).delete(synchronize_session=False)
                    
                    turnos_objs = []
                    for dia_str, t_info in vig_data.get("turnos", {}).items():
                        if isinstance(t_info, dict):
                            codigo, h_t, h_n, h_f, es_f = t_info.get("codigo", ""), float(t_info.get("t", 0)), float(t_info.get("n", 0)), float(t_info.get("f", 0)), bool(t_info.get("festivo", False))
                        else:
                            codigo, h_t, h_n, h_f, es_f = t_info, 0.0, 0.0, 0.0, False

                        turnos_objs.append(sql_models.Turno(
                            empleado_id=emp_id, anio=anio, mes=mes, 
                            dia=int(float(dia_str)), codigo_turno=codigo,
                            horas_trabajadas=h_t, horas_nocturnas=h_n, 
                            horas_festivas=h_f, es_festivo=es_f
                        ))
                    
                    if turnos_objs:
                        db.bulk_save_objects(turnos_objs)

        # 3. Sincronizar Configuración de Turnos
        for codigo, config_data in data['config_turnos'].items():
            db_config = db.query(sql_models.ConfiguracionTurno).filter(sql_models.ConfiguracionTurno.codigo == codigo).first()
            if not db_config:
                db_config = sql_models.ConfiguracionTurno(
                    codigo=codigo,
                    descripcion=config_data.get('leyenda'),
                    horario=config_data.get('horario') or config_data.get('leyenda'),
                    color=config_data.get('color_fondo') or config_data.get('color'),
                    horas_total=float(config_data.get('trabajadas', 0)),
                    horas_nocturnas=float(config_data.get('nocturnas', 0))
                )
                db.add(db_config)
            else:
                db_config.descripcion = config_data.get('leyenda')
                db_config.horario = config_data.get('horario') or config_data.get('leyenda')
                db_config.color = config_data.get('color_fondo') or config_data.get('color')
                db_config.horas_total = float(config_data.get('trabajadas', 0))
                db_config.horas_nocturnas = float(config_data.get('nocturnas', 0))

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
