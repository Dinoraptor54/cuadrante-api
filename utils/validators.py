# -*- coding: utf-8 -*-
"""
Módulo de validaciones
Proporciona validadores robustos para entrada de datos
"""

from datetime import datetime, date
from typing import Optional
from fastapi import HTTPException, status
import re


class ValidationError(HTTPException):
    """Excepción personalizada para errores de validación"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class DateValidator:
    """Validador para fechas"""
    
    @staticmethod
    def validate_year(year: int) -> int:
        """Valida que el año sea válido"""
        current_year = datetime.now().year
        if year < 2000 or year > current_year + 5:
            raise ValidationError(
                f"Año inválido: {year}. Debe estar entre 2000 y {current_year + 5}"
            )
        return year
    
    @staticmethod
    def validate_month(month: int) -> int:
        """Valida que el mes sea válido (1-12)"""
        if month < 1 or month > 12:
            raise ValidationError(
                f"Mes inválido: {month}. Debe estar entre 1 y 12"
            )
        return month
    
    @staticmethod
    def validate_day(day: int, month: int, year: int) -> int:
        """Valida que el día sea válido para el mes y año dados"""
        try:
            date(year, month, day)
        except ValueError:
            raise ValidationError(
                f"Día inválido: {day} para {month}/{year}"
            )
        return day
    
    @staticmethod
    def validate_date_string(date_str: str, format: str = "%Y-%m-%d") -> date:
        """Valida una cadena de fecha en formato YYYY-MM-DD"""
        try:
            return datetime.strptime(date_str, format).date()
        except ValueError:
            raise ValidationError(
                f"Formato de fecha inválido: {date_str}. Use {format}"
            )
    
    @staticmethod
    def validate_date_in_past(date_obj: date, allow_today: bool = True) -> date:
        """Valida que una fecha no esté en el pasado"""
        today = date.today()
        if allow_today:
            if date_obj < today:
                raise ValidationError(
                    f"La fecha no puede estar en el pasado: {date_obj}"
                )
        else:
            if date_obj <= today:
                raise ValidationError(
                    f"La fecha debe ser mayor a hoy: {date_obj}"
                )
        return date_obj


class EmailValidator:
    """Validador para emails"""
    
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Valida formato de email"""
        if not email or not EmailValidator.EMAIL_PATTERN.match(email):
            raise ValidationError(f"Email inválido: {email}")
        return email.lower()
    
    @staticmethod
    def validate_email_not_empty(email: Optional[str]) -> str:
        """Valida que el email no esté vacío"""
        if not email:
            raise ValidationError("El email no puede estar vacío")
        return EmailValidator.validate_email(email)


class TurnoValidator:
    """Validador para turnos"""
    
    TURNO_CODES = [
        "M", "T", "N",  # Mañana, Tarde, Noche
        "D", "F",  # Día, Fiesta
        "V",  # Vacaciones
        "B", "L"  # Baja, Libre
    ]
    
    @staticmethod
    def validate_turno_code(code: str) -> str:
        """Valida que el código de turno sea válido"""
        code = code.upper().strip()
        if code not in TurnoValidator.TURNO_CODES:
            raise ValidationError(
                f"Código de turno inválido: {code}. "
                f"Debe ser uno de: {', '.join(TurnoValidator.TURNO_CODES)}"
            )
        return code
    
    @staticmethod
    def validate_horario(horario: str) -> str:
        """Valida que el horario tenga formato válido"""
        horario = horario.strip()
        pattern = r'^\d{2}:\d{2}-\d{2}:\d{2}$'
        if not re.match(pattern, horario):
            raise ValidationError(
                f"Formato de horario inválido: {horario}. "
                f"Use formato HH:MM-HH:MM"
            )
        return horario


class PermutaValidator:
    """Validador para permutas"""
    
    @staticmethod
    def validate_permuta_request(
        fecha_origen: str,
        fecha_destino: str,
        email_destino: str
    ) -> tuple:
        """Valida datos de solicitud de permuta"""
        # Validar fechas
        fecha_origen_obj = DateValidator.validate_date_string(fecha_origen)
        fecha_destino_obj = DateValidator.validate_date_string(fecha_destino)
        
        # Validar que las fechas sean diferentes
        if fecha_origen_obj == fecha_destino_obj:
            raise ValidationError(
                "Las fechas de origen y destino no pueden ser iguales"
            )
        
        # Validar que ambas fechas no estén en el pasado
        DateValidator.validate_date_in_past(fecha_origen_obj)
        DateValidator.validate_date_in_past(fecha_destino_obj)
        
        # Validar email
        email_destino = EmailValidator.validate_email_not_empty(email_destino)
        
        return fecha_origen_obj, fecha_destino_obj, email_destino


class PasswordValidator:
    """Validador para contraseñas"""
    
    @staticmethod
    def validate_password_strength(password: str) -> str:
        """Valida la fortaleza de la contraseña"""
        if not password or len(password) < 8:
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres"
            )
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_upper and has_lower and has_digit):
            raise ValidationError(
                "La contraseña debe contener mayúsculas, minúsculas y números"
            )
        
        return password


class PaginationValidator:
    """Validador para paginación"""
    
    @staticmethod
    def validate_pagination(skip: int = 0, limit: int = 50) -> tuple:
        """Valida parámetros de paginación"""
        if skip < 0:
            raise ValidationError("El parámetro 'skip' no puede ser negativo")
        
        if limit < 1 or limit > 1000:
            raise ValidationError(
                "El parámetro 'limit' debe estar entre 1 y 1000"
            )
        
        return skip, limit
