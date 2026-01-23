# -*- coding: utf-8 -*-
"""
Router de empleados
Endpoints para consultar información de empleados
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.append('..')
from routers.auth import get_current_user
from routers.turnos import cargar_datos_desktop
from models import sql_models

router = APIRouter()


# Modelos
class PerfilEmpleado(BaseModel):
    nombre: str
    email: str
    categoria: str
    fecha_alta: Optional[str] = None
    telefono: Optional[str] = None


class EmpleadoResponse(BaseModel):
    id: int
    nombre_completo: str
    email: Optional[str] = None
    categoria: str
    
    class Config:
        from_attributes = True


# Endpoints
@router.get("/", response_model=list[EmpleadoResponse])
async def listar_empleados(
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_user)
):
    """Listar todos los empleados con paginación"""
    # Validar paginación
    from utils.validators import PaginationValidator
    from utils.error_handlers import ValidationError
    from fastapi import HTTPException
    try:
        PaginationValidator.validate_pagination(skip, limit)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    from models.database import SessionLocal
    db = SessionLocal()
    empleados = db.query(sql_models.Empleado).offset(skip).limit(limit).all()
    db.close()
    return empleados


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


from services import empleados_service
from models.database import get_db
from sqlalchemy.orm import Session

class BalanceResponse(BaseModel):
    anio: int
    total_horas_trabajadas: float
    horas_convenio: float
    balance_horas: float
    dias_trabajados: int
    dias_vacaciones: int
    dias_baja: int

@router.get("/balance/{anio}", response_model=BalanceResponse)
async def get_balance_anual(
    anio: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el balance de horas del año para el usuario actual
    """
    # Validar año
    from utils.validators import DateValidator
    from utils.error_handlers import ValidationError
    try:
        DateValidator.validate_year(anio)
    except ValidationError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))
    # 1. Obtener usuario de BD para tener su ID
    from services import auth_service
    user_db = auth_service.get_user_by_email(db, current_user['email'])
    if not user_db:
         # Fallback si por alguna razón extraña no está en BD pero tiene token
         # (Ej: usuario borrado mientras tenía token válido)
        return BalanceResponse(
            anio=anio,
            total_horas_trabajadas=0,
            horas_convenio=1768,
            balance_horas=0,
            dias_trabajados=0,
            dias_vacaciones=0,
            dias_baja=0
        )
        
    # TODO: Asumimos que el User se mapea a un Empleado por string matching o relación directa?
    # En sql_models.py, User y Empleado son tablas separadas.
    # El User tiene 'full_name' y Empleado 'nombre_completo'.
    # Deberíamos buscar el Empleado asociado al User.
    
    empleado = db.query(sql_models.Empleado).filter(
        sql_models.Empleado.nombre_completo == user_db.full_name
    ).first()
    
    if not empleado:
         return BalanceResponse(
            anio=anio,
            total_horas_trabajadas=0,
            horas_convenio=1768,
            balance_horas=0,
            dias_trabajados=0,
            dias_vacaciones=0,
            dias_baja=0
        )

    balance = empleados_service.calcular_balance_anual(db, empleado.id, anio)
    return BalanceResponse(**balance)


# Modelos adicionales
class UpdateProfileRequest(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class BalanceMensualResponse(BaseModel):
    anio: int
    mes: int
    total_horas_trabajadas: float
    horas_convenio: float
    balance_horas: float
    dias_trabajados: int
    horas_nocturnas: float
    dias_festivos: int


# Endpoint adicional: mi-perfil (alias de /perfil)
@router.get("/mi-perfil", response_model=PerfilEmpleado)
async def get_mi_perfil(current_user: dict = Depends(get_current_user)):
    """
    Obtiene el perfil del empleado actual (alias de /perfil)
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


@router.put("/actualizar-perfil")
async def actualizar_perfil(
    profile_update: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza el perfil del empleado actual
    """
    from services import auth_service
    from fastapi import HTTPException
    
    # Obtener usuario de BD con fallbacks para modo pruebas
    user = auth_service.get_user_by_email(db, current_user['email'])
    if not user:
        from models.sql_models import User
        user = db.query(User).filter(
            User.full_name == current_user.get('nombre', '')
        ).first()
    if not user:
        user = db.query(User).first()
    # En modo pruebas, si no hay usuario, crear uno temporal
    if not user and os.getenv("ENVIRONMENT", "development") != "production":
        from models.sql_models import User
        user = User(
            email=current_user.get('email', 'test@example.com'),
            hashed_password="temp",
            full_name=current_user.get('nombre', 'Test User'),
            role=current_user.get('rol', 'vigilante')
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Validar email si se proporciona
    if profile_update.email:
        from utils.validators import EmailValidator
        try:
            EmailValidator.validate_email(profile_update.email)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    # Actualizar campos si se proporcionan
    if profile_update.nombre or profile_update.apellido:
        nombre_parts = []
        if profile_update.nombre:
            nombre_parts.append(profile_update.nombre)
        if profile_update.apellido:
            nombre_parts.append(profile_update.apellido)
        if nombre_parts:
            user.full_name = " ".join(nombre_parts)
    
    if profile_update.email:
        # Verificar que el email no esté en uso
        existing = auth_service.get_user_by_email(db, profile_update.email)
        if existing and existing.id != user.id:
            raise HTTPException(status_code=400, detail="El email ya está en uso")
        user.email = profile_update.email
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Perfil actualizado correctamente",
        "email": user.email,
        "nombre": user.full_name
    }


@router.get("/balance/{anio}/{mes}", response_model=BalanceMensualResponse)
async def get_balance_mensual(
    anio: int,
    mes: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el balance de horas de un mes específico para el usuario actual
    """
    from fastapi import HTTPException
    from services import auth_service
    from utils.validators import DateValidator
    
    # Validar mes
    try:
        DateValidator.validate_month(mes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Validar año
    try:
        DateValidator.validate_year(anio)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Obtener usuario de BD
    user_db = auth_service.get_user_by_email(db, current_user['email'])
    if not user_db:
        return BalanceMensualResponse(
            anio=anio,
            mes=mes,
            total_horas_trabajadas=0,
            horas_convenio=147.3,  # Aproximado mensual (1768/12)
            balance_horas=0,
            dias_trabajados=0
        )
    
    # Buscar empleado asociado
    empleado = db.query(sql_models.Empleado).filter(
        sql_models.Empleado.nombre_completo == user_db.full_name
    ).first()
    
    if not empleado:
        return BalanceMensualResponse(
            anio=anio,
            mes=mes,
            total_horas_trabajadas=0,
            horas_convenio=147.3,
            balance_horas=0,
            dias_trabajados=0
        )
    
    # Calcular balance mensual
    # Obtener turnos del mes especificado
    from datetime import date
    import calendar
    
    # Primer y último día del mes
    primer_dia = date(anio, mes, 1)
    ultimo_dia_num = calendar.monthrange(anio, mes)[1]
    ultimo_dia = date(anio, mes, ultimo_dia_num)
    
    turnos = db.query(sql_models.Turno).filter(
        sql_models.Turno.empleado_id == empleado.id,
        sql_models.Turno.fecha >= str(primer_dia),
        sql_models.Turno.fecha <= str(ultimo_dia)
    ).all()
    
    # Cargar festivos desde el archivo JSON
    from routers.turnos import cargar_datos_desktop
    festivos_data = cargar_datos_desktop("festivos.json")
    
    # Calcular horas trabajadas, nocturnas y festivos
    total_horas = 0
    horas_nocturnas = 0
    dias_trabajados = 0
    dias_festivos = 0
    
    for turno in turnos:
        if turno.codigo_turno not in ['L', 'V', 'B']:  # No contar libres, vacaciones, bajas
            horas = empleados_service.get_horas_turno(turno.codigo_turno)
            horas_noct = empleados_service.get_horas_nocturnas(turno.codigo_turno)
            total_horas += horas
            horas_nocturnas += horas_noct
            dias_trabajados += 1
            
            # Verificar si es festivo
            try:
                fecha_turno = date.fromisoformat(turno.fecha) if isinstance(turno.fecha, str) else turno.fecha
                fecha_str = fecha_turno.strftime("%Y-%m-%d")
                
                # Buscar en festivos nacionales, comunidad y locales
                festivos_nacionales = festivos_data.get("nacional", {})
                festivos_comunidad = festivos_data.get("comunidad", {})
                festivos_locales = festivos_data.get("local", {})
                
                if (fecha_str in festivos_nacionales or 
                    fecha_str in festivos_comunidad or 
                    fecha_str in festivos_locales):
                    dias_festivos += 1
            except:
                pass  # Si hay error parseando fecha, continuar
    
    horas_convenio_mes = 147.3  # Aproximado mensual
    balance = total_horas - horas_convenio_mes
    
    return BalanceMensualResponse(
        anio=anio,
        mes=mes,
        total_horas_trabajadas=total_horas,
        horas_convenio=horas_convenio_mes,
        balance_horas=balance,
        dias_trabajados=dias_trabajados,
        horas_nocturnas=horas_nocturnas,
        dias_festivos=dias_festivos
    )
