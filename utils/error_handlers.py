# -*- coding: utf-8 -*-
"""
Manejador Global de Errores
Centraliza el manejo de excepciones para toda la aplicación
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.logging_config import log_error, log_warning
from utils.validators import ValidationError
import traceback


def setup_error_handlers(app: FastAPI) -> None:
    """Registra todos los manejadores de error en la aplicación"""
    
    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        request: Request,
        exc: ValidationError
    ):
        """Maneja errores de validación personalizados"""
        log_warning(
            f"Error de validación: {exc.detail} "
            f"- Path: {request.url.path}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "type": "validation_error"}
        )
    
    @app.exception_handler(RequestValidationError)
    async def fastapi_validation_error_handler(
        request: Request,
        exc: RequestValidationError
    ):
        """Maneja errores de validación de FastAPI"""
        errors = []
        for error in exc.errors():
            field = ".".join(str(x) for x in error["loc"][1:])
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"]
            })
        
        log_warning(
            f"Error de validación FastAPI: {len(errors)} error(es) "
            f"- Path: {request.url.path}"
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Datos inválidos",
                "errors": errors,
                "type": "validation_error"
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ):
        """Maneja excepciones generales no capturadas"""
        
        # Log del error
        error_id = id(exc)  # ID único para tracking
        log_error(
            f"Error no manejado (ID: {error_id}) "
            f"- Path: {request.url.path} "
            f"- Método: {request.method}",
            error=exc
        )
        
        # No revelar detalles en producción
        import os
        environment = os.getenv("ENVIRONMENT", "development")
        
        if environment == "development":
            # En desarrollo, mostrar stacktrace
            detail = str(exc)
            traceback_str = traceback.format_exc()
        else:
            # En producción, mensaje genérico
            detail = "Error interno del servidor"
            traceback_str = None
        
        response = {
            "detail": detail,
            "type": "internal_error",
            "error_id": error_id
        }
        
        if traceback_str:
            response["traceback"] = traceback_str
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response
        )


class ErrorLoggingMiddleware:
    """Middleware para registrar errores en las respuestas"""
    
    def __init__(self, app: FastAPI):
        self.app = app
    
    async def __call__(self, request: Request, call_next):
        """Procesa la solicitud y registra errores"""
        try:
            response = await call_next(request)
            
            # Registrar errores en respuestas
            if response.status_code >= 400:
                status_name = status.HTTP_400_BAD_REQUEST
                if response.status_code == 401:
                    status_name = "Unauthorized"
                elif response.status_code == 403:
                    status_name = "Forbidden"
                elif response.status_code == 404:
                    status_name = "Not Found"
                elif response.status_code >= 500:
                    status_name = "Server Error"
                
                log_warning(
                    f"Error {response.status_code} ({status_name}) "
                    f"- {request.method} {request.url.path}"
                )
            
            return response
        
        except Exception as exc:
            # Si hay excepción no manejada
            log_error(
                f"Excepción en middleware "
                f"- {request.method} {request.url.path}",
                error=exc
            )
            raise


def get_error_response_schema():
    """Esquema de respuesta de error para documentación"""
    return {
        "type": "object",
        "properties": {
            "detail": {
                "type": "string",
                "description": "Descripción del error"
            },
            "type": {
                "type": "string",
                "enum": ["validation_error", "internal_error", "auth_error"],
                "description": "Tipo de error"
            },
            "error_id": {
                "type": "string",
                "description": "ID único para tracking"
            }
        }
    }
