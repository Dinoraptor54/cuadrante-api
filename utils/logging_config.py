# -*- coding: utf-8 -*-
"""
Módulo de logging
Proporciona logging estructurado para la aplicación
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional, Dict


class AppLogger:
    """Gestor centralizado de logging"""
    
    _loggers: Dict[str, logging.Logger] = {}
    _initialized = False
    log_dir: str = "logs"
    log_level: int = logging.INFO
    environment: str = "development"
    
    @staticmethod
    def initialize(
        log_dir: str = "logs",
        log_level: str = "INFO",
        environment: str = "development"
    ):
        """Inicializa el sistema de logging"""
        if AppLogger._initialized:
            return
        
        # Crear directorio de logs si no existe
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        AppLogger.log_dir = log_dir
        AppLogger.log_level = getattr(logging, log_level.upper(), logging.INFO)
        AppLogger.environment = environment
        AppLogger._initialized = True
    
    @staticmethod
    def get_logger(name: str = "cuadrante_api") -> logging.Logger:
        """Obtiene o crea un logger con configuración estándar"""
        if name in AppLogger._loggers:
            return AppLogger._loggers[name]
        
        # Configurar logger
        logger = logging.getLogger(name)
        logger.setLevel(AppLogger.log_level)
        
        # Evitar duplicados
        if logger.hasHandlers():
            return logger
        
        # Formato de logging
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(AppLogger.log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler para archivo (solo en producción)
        if AppLogger.environment == "production":
            log_file = os.path.join(
                AppLogger.log_dir,
                f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10485760,  # 10MB
                backupCount=10,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        AppLogger._loggers[name] = logger
        return logger


# Logger global
logger = AppLogger.get_logger()


def log_info(message: str, **kwargs):
    """Log nivel INFO"""
    logger.info(message, extra=kwargs)


def log_debug(message: str, **kwargs):
    """Log nivel DEBUG"""
    logger.debug(message, extra=kwargs)


def log_warning(message: str, **kwargs):
    """Log nivel WARNING"""
    logger.warning(message, extra=kwargs)


def log_error(message: str, error: Optional[Exception] = None, **kwargs):
    """Log nivel ERROR"""
    if error:
        logger.error(f"{message} - {str(error)}", extra=kwargs, exc_info=True)
    else:
        logger.error(message, extra=kwargs)


def log_critical(
    message: str,
    error: Optional[Exception] = None,
    **kwargs
):
    """Log nivel CRITICAL"""
    if error:
        logger.critical(
            f"{message} - {str(error)}",
            extra=kwargs,
            exc_info=True
        )
    else:
        logger.critical(message, extra=kwargs)


# Logs específicos de negocio
def log_login(email: str, success: bool, error: Optional[str] = None):
    """Log de intentos de login"""
    if success:
        log_info(f"Login exitoso para usuario: {email}")
    else:
        error_msg = error or 'Credenciales inválidas'
        log_warning(f"Login fallido para usuario: {email} - {error_msg}")


def log_permuta_creada(
    solicitante: str,
    receptor: str,
    fecha_origen: str,
    fecha_destino: str
):
    """Log de creación de permuta"""
    log_info(
        f"Permuta creada: {solicitante} -> {receptor} "
        f"(origen: {fecha_origen}, destino: {fecha_destino})"
    )


def log_permuta_aceptada(permuta_id: int, usuario: str):
    """Log de aceptación de permuta"""
    log_info(f"Permuta #{permuta_id} aceptada por {usuario}")


def log_sincronizacion(total_registros: int, tiempo_segundos: float):
    """Log de sincronización de datos"""
    log_info(
        f"Sincronización completada: {total_registros} registros "
        f"en {tiempo_segundos:.2f}s"
    )


def log_error_bd(operacion: str, error: Exception):
    """Log de errores de base de datos"""
    log_error(
        f"Error en operación de BD: {operacion}",
        error=error
    )


def log_acceso_recurso(
    usuario: str,
    recurso: str,
    metodo: str = "GET",
    exitoso: bool = True
):
    """Log de acceso a recursos"""
    estado = "éxito" if exitoso else "denegado"
    log_info(f"Acceso {estado}: {usuario} - {metodo} {recurso}")
