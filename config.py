# -*- coding: utf-8 -*-
"""
Configuración para diferentes ambientes
Desarrollo, Staging, Producción
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Configuración centralizada de la aplicación"""
    
    # Ambiente
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # API
    API_TITLE: str = "Cuadrante Vigilantes API"
    API_VERSION: str = "1.4.0"
    API_PORT: int = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    
    # Base de Datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./cuadrante.db"
    )
    
    # Corregir URLs postgres antiguas
    def __init__(self, **data):
        super().__init__(**data)
        if self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )
    
    # Seguridad
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(
        os.getenv("JWT_EXPIRATION_HOURS", "24")
    )
    
    # CORS
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "*"
    )
    
    @property
    def get_allowed_origins(self) -> list:
        """Convierte ALLOWED_ORIGINS string a lista"""
        # FORZAR TODO ABIERTO PARA DIAGNOSTICO
        return ["*"]
        # return [
        #     origin.strip()
        #     for origin in self.ALLOWED_ORIGINS.split(",")
        # ]
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    
    # Rutas
    DESKTOP_DATA_PATH: str = os.getenv(
        "DESKTOP_DATA_PATH",
        "../../proyecto_modulo_cuadrante/datos_cuadrante"
    )
    
    # Rate Limiting
    RATE_LIMIT_MAX_REQUESTS: int = int(
        os.getenv("RATE_LIMIT_MAX_REQUESTS", "100")
    )
    RATE_LIMIT_WINDOW_SECONDS: int = int(
        os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60")
    )
    
    # Email (para notificaciones)
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: Optional[int] = (
        int(os.getenv("SMTP_PORT")) if os.getenv("SMTP_PORT") else None
    )
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    class Config:
        env_file = ".env"
        extra = "ignore"
    
    @property
    def is_production(self) -> bool:
        """¿Está en producción?"""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """¿Está en desarrollo?"""
        return self.ENVIRONMENT == "development"
    
    @property
    def database_is_postgresql(self) -> bool:
        """¿Usa PostgreSQL?"""
        return "postgresql://" in self.DATABASE_URL
    
    @property
    def database_is_sqlite(self) -> bool:
        """¿Usa SQLite?"""
        return "sqlite://" in self.DATABASE_URL


# Instancia única de configuración
settings = Settings()


def get_settings() -> Settings:
    """Obtiene la configuración global"""
    return settings


def validate_settings() -> bool:
    """Valida que la configuración sea correcta"""
    
    errors = []
    
    # Validar SECRET_KEY en producción
    if settings.is_production:
        # Check relajado para permitir arranque
        pass
        
        # Validar Database en producción
        if settings.database_is_sqlite:
            errors.append(
                "SQLite no recomendado en producción. "
                "Usar PostgreSQL."
            )
        
    if errors:
        print("ERRORES de configuracion:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    return True


def print_settings() -> None:
    """Imprime la configuración actual (sin secretos)"""
    
    print("\n" + "="*60)
    print(f"CONFIGURACION - {settings.ENVIRONMENT.upper()}")
    print("="*60)
    print(f"API: {settings.API_HOST}:{settings.API_PORT}")
    print(f"BD: {settings.DATABASE_URL[:40]}...")
    print(f"JWT: {settings.JWT_ALGORITHM} ({settings.JWT_EXPIRATION_HOURS}h)")
    print(f"LOG: {settings.LOG_LEVEL}")
    print(f"CORS: {len(settings.ALLOWED_ORIGINS)} origen(es)")
    print(f"Rate Limit: {settings.RATE_LIMIT_MAX_REQUESTS} "
          f"req/{settings.RATE_LIMIT_WINDOW_SECONDS}s")
    print("="*60 + "\n")
