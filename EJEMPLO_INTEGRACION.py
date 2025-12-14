# -*- coding: utf-8 -*-
"""
Ejemplo de uso de validadores, logging y error handling
Muestra cómo integrar todas las mejoras en un router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from models.database import get_db
from routers.auth import get_current_user

# Importar utilidades
from utils.validators import (
    DateValidator,
    EmailValidator,
    PaginationValidator
)
from utils.logging_config import (
    log_info,
    log_error,
    log_acceso_recurso
)

router = APIRouter()


# EJEMPLO 1: Validar parámetros de ruta
@router.get("/ejemplo/balance/{anio}")
async def ejemplo_validar_anio(
    anio: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Ejemplo: Validar que el año sea válido
    """
    try:
        # Validar año
        validated_year = DateValidator.validate_year(anio)

        # Log de acceso
        log_acceso_recurso(
            current_user.get("email"),
            f"/balance/{validated_year}",
            "GET",
            exitoso=True
        )

        log_info(f"Balance solicitado para año {validated_year}")

        return {"anio": validated_year, "balance": 100}

    except Exception as exc:
        log_error("Error en balance", error=exc)
        raise HTTPException(status_code=400, detail=str(exc))


# EJEMPLO 2: Validar email y fecha
@router.post("/ejemplo/permuta")
async def ejemplo_validar_permuta(
    fecha_origen: str,
    fecha_destino: str,
    email_destino: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Ejemplo: Validar emails y fechas de permuta
    """
    try:
        # Validar email
        validated_email = EmailValidator.validate_email(email_destino)

        # Validar fechas
        from utils.validators import PermutaValidator
        fecha_origen_obj, fecha_destino_obj, email = (
            PermutaValidator.validate_permuta_request(
                fecha_origen,
                fecha_destino,
                email_destino
            )
        )

        log_info(
            f"Permuta validada: {fecha_origen_obj} -> {fecha_destino_obj}"
        )

        return {
            "status": "válido",
            "fecha_origen": fecha_origen_obj,
            "fecha_destino": fecha_destino_obj,
            "email": email
        }

    except Exception as exc:
        log_error("Error en validación de permuta", error=exc)
        raise


# EJEMPLO 3: Validar paginación
@router.get("/ejemplo/empleados")
async def ejemplo_listar_empleados(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ejemplo: Validar parámetros de paginación
    """
    try:
        # Validar paginación
        skip, limit = PaginationValidator.validate_pagination(skip, limit)

        log_info(
            f"Listando empleados: skip={skip}, limit={limit}"
        )

        # Aquí iría la lógica de BD
        return {
            "skip": skip,
            "limit": limit,
            "empleados": []
        }

    except Exception as exc:
        log_error("Error en listado de empleados", error=exc)
        raise


# EJEMPLO 4: Validación personalizada
@router.put("/ejemplo/perfil")
async def ejemplo_actualizar_perfil(
    nombre: str,
    apellido: str,
    email: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Ejemplo: Validación personalizada con múltiples campos
    """
    try:
        # Validar email
        email = EmailValidator.validate_email(email)

        # Validar que los campos no estén vacíos
        if not nombre or not nombre.strip():
            raise ValueError("Nombre no puede estar vacío")

        if not apellido or not apellido.strip():
            raise ValueError("Apellido no puede estar vacío")

        log_info(
            f"Perfil actualizado para {email}: "
            f"{nombre} {apellido}"
        )

        return {
            "status": "actualizado",
            "email": email,
            "nombre": nombre,
            "apellido": apellido
        }

    except ValueError as exc:
        log_error("Validación fallida", error=exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        log_error("Error en actualización de perfil", error=exc)
        raise


# EJEMPLO 5: Manejador de excepciones personalizado
@router.get("/ejemplo/riesgoso")
async def ejemplo_manejo_errores(
    current_user: dict = Depends(get_current_user)
):
    """
    Ejemplo: Cómo los errores se manejan automáticamente
    """
    try:
        # Simular un error
        resultado = 10 / 0  # ZeroDivisionError

        return {"resultado": resultado}

    except ZeroDivisionError as exc:
        # Los errores se loguean automáticamente
        log_error("Error de división por cero", error=exc)
        raise HTTPException(
            status_code=400,
            detail="No se puede dividir entre cero"
        )
    except Exception as exc:
        # Cualquier otro error se maneja globalmente
        log_error("Error inesperado", error=exc)
        raise


# DOCSTRING: Patrones de Uso
"""
PATRONES DE USO DE VALIDADORES

1. VALIDAR FECHAS:
   anio = DateValidator.validate_year(anio)
   mes = DateValidator.validate_month(mes)
   dia = DateValidator.validate_day(dia, mes, anio)
   fecha = DateValidator.validate_date_string("2025-12-08")

2. VALIDAR EMAILS:
   email = EmailValidator.validate_email("user@example.com")

3. VALIDAR TURNOS:
   codigo = TurnoValidator.validate_turno_code("M")
   horario = TurnoValidator.validate_horario("08:00-16:00")

4. VALIDAR PERMUTAS:
   f_origen, f_destino, email = (
       PermutaValidator.validate_permuta_request(...)
   )

5. VALIDAR PAGINACIÓN:
   skip, limit = PaginationValidator.validate_pagination(skip, limit)

6. VALIDAR CONTRASEÑA:
   pwd = PasswordValidator.validate_password_strength(password)

7. LOGGING DE EVENTOS:
   log_info("Mensaje")
   log_warning("Advertencia")
   log_error("Error", error=exception)
   log_login("user@ex.com", success=True)
   log_permuta_creada("u1@ex.com", "u2@ex.com", "2025-12-01", "2025-12-02")
   log_acceso_recurso("user@ex.com", "/api/turnos", "GET", True)

8. MANEJO DE ERRORES:
   try:
       # Tu código
   except ValidationError as exc:
       # Errores de validación personalizados
       log_error("Error de validación", error=exc)
       raise HTTPException(status_code=422, detail=str(exc))
   except Exception as exc:
       # Cualquier otro error
       log_error("Error inesperado", error=exc)
       raise

INSTRUCCIONES:
1. Importar validadores necesarios
2. Llamar validador al inicio del endpoint
3. Lograr el evento importante
4. Manejar excepciones adecuadamente
5. El manejador global captará cualquier error no manejado
"""
