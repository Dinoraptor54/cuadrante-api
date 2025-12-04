# -*- coding: utf-8 -*-
"""
API REST para Cuadrante de Vigilantes
Permite acceso móvil a turnos, permutas y datos de empleados
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import uvicorn

# Importar routers
from routers import auth, turnos, permutas, empleados, sync

# Crear app FastAPI
app = FastAPI(
    title="Cuadrante Vigilantes API",
    description="API REST para gestión de turnos y cuadrantes de vigilantes",
    version="1.0.0"
)

# Configurar CORS (permitir acceso desde app móvil/web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(turnos.router, prefix="/api/turnos", tags=["Turnos"])
app.include_router(permutas.router, prefix="/api/permutas", tags=["Permutas"])
app.include_router(empleados.router, prefix="/api/empleados", tags=["Empleados"])
app.include_router(sync.router, prefix="/api/sync", tags=["Sincronización"])


@app.get("/")
async def root():
    """Endpoint raíz - información de la API"""
    return {
        "message": "API Cuadrante Vigilantes",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {"status": "healthy"}


if __name__ == "__main__":
    # Ejecutar servidor de desarrollo
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload en desarrollo
    )
