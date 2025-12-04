from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
import json

from models.database import get_db, engine
from models import sql_models
from routers.auth import get_current_user

# Crear tablas si no existen
sql_models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Modelos Pydantic para recibir datos
class SyncData(BaseModel):
    empleados: Dict[str, Any]
    cuadrantes: Dict[str, Any] # Estructura anidada anio -> mes -> lista vigilantes
    config_turnos: Dict[str, Any]

@router.post("/full")
async def sync_full_data(
    data: SyncData,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Sincronización completa: Recibe los JSONs del desktop y actualiza la BD.
    Solo permitido para coordinadores.
    """
    if current_user["rol"] != "coordinador":
        raise HTTPException(status_code=403, detail="No autorizado para sincronizar")

    try:
        # 1. Sincronizar Empleados
        # Primero obtenemos los existentes para no duplicar o para actualizar
        for nombre, emp_data in data.empleados.items():
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
                # Actualizar campos
                db_emp.email = emp_data.get("email")
                db_emp.telefono = emp_data.get("telefono")
                # ... otros campos
        
        db.flush() # Para obtener IDs de nuevos empleados

        # 2. Sincronizar Turnos
        # Estrategia simple: Borrar turnos del año/mes recibidos y re-insertar
        # Ojo: Esto es destructivo para el historial si no se envía todo.
        # Asumimos que el desktop es la fuente de verdad.
        
        # Iterar sobre los datos recibidos
        for anio_str, meses_data in data.cuadrantes.items():
            anio = int(anio_str)
            for mes_str, vigilantes_list in meses_data.items():
                mes = int(mes_str)
                
                # Para cada vigilante en este mes
                for vig_data in vigilantes_list:
                    nombre = vig_data["nombre"]
                    turnos_dict = vig_data.get("turnos", {})
                    
                    # Buscar empleado
                    empleado = db.query(sql_models.Empleado).filter(sql_models.Empleado.nombre_completo == nombre).first()
                    if not empleado:
                        continue # O crearlo on-the-fly
                    
                    # Borrar turnos existentes de este empleado en este mes/año
                    db.query(sql_models.Turno).filter(
                        sql_models.Turno.empleado_id == empleado.id,
                        sql_models.Turno.anio == anio,
                        sql_models.Turno.mes == mes
                    ).delete()
                    
                    # Insertar nuevos turnos
                    for dia_str, codigo in turnos_dict.items():
                        nuevo_turno = sql_models.Turno(
                            empleado_id=empleado.id,
                            anio=anio,
                            mes=mes,
                            dia=int(dia_str),
                            codigo_turno=codigo
                        )
                        db.add(nuevo_turno)

        db.commit()
        return {"status": "success", "message": "Sincronización completada"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en sincronización: {str(e)}")
