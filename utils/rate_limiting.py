# -*- coding: utf-8 -*-
"""
Módulo de rate limiting
Proporciona limitación de velocidad para endpoints
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict


class RateLimiter:
    """
    Limitador de velocidad para proteger contra abusos.
    Almacena intentos por IP/usuario en memoria.
    Para producción, usar Redis.
    """
    
    def __init__(self):
        # Formato: {ip_or_user: [(timestamp, count), ...]}
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_task = None
    
    async def is_rate_limited(
        self,
        identifier: str,
        max_requests: int = 100,
        window_seconds: int = 60
    ) -> bool:
        """
        Verifica si la solicitud excede el límite de velocidad.
        
        Args:
            identifier: IP del cliente o ID de usuario
            max_requests: Máximo de solicitudes permitidas
            window_seconds: Ventana de tiempo en segundos
        
        Returns:
            True si está limitado, False si está permitido
        """
        now = datetime.now()
        cutoff = now - timedelta(seconds=window_seconds)
        
        # Limpiar solicitudes antiguas
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]
        
        # Verificar límite
        if len(self.requests[identifier]) >= max_requests:
            return True
        
        # Registrar nueva solicitud
        self.requests[identifier].append(now)
        return False
    
    def get_remaining_requests(
        self,
        identifier: str,
        max_requests: int = 100,
        window_seconds: int = 60
    ) -> int:
        """Obtiene solicitudes restantes"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=window_seconds)
        
        valid_requests = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]
        
        return max(0, max_requests - len(valid_requests))


# Instancia global
rate_limiter = RateLimiter()


class RateLimitMiddleware:
    """Middleware de rate limiting para FastAPI"""
    
    def __init__(
        self,
        app,
        max_requests: int = 100,
        window_seconds: int = 60,
        exclude_paths: list = None
    ):
        self.app = app
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/openapi.json",
            "/health"
        ]
    
    async def __call__(self, request: Request, call_next):
        """Procesa la solicitud con rate limiting"""
        
        # Excluir rutas específicas
        if request.url.path in self.exclude_paths:
            return await call_next(request)
        
        # Obtener identificador (IP del cliente)
        client_ip = request.client.host
        
        # Verificar rate limit
        if await rate_limiter.is_rate_limited(
            client_ip,
            self.max_requests,
            self.window_seconds
        ):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Demasiadas solicitudes. "
                    "Intenta de nuevo más tarde."
                },
                headers={
                    "Retry-After": str(self.window_seconds)
                }
            )
        
        # Añadir headers de rate limit
        response = await call_next(request)
        
        remaining = rate_limiter.get_remaining_requests(
            client_ip,
            self.max_requests,
            self.window_seconds
        )
        
        response.headers["X-RateLimit-Limit"] = str(
            self.max_requests
        )
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        reset_time = datetime.now() + timedelta(
            seconds=self.window_seconds
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(reset_time.timestamp())
        )
        
        return response
