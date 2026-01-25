from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from models.database import get_db, engine
from models import sql_models
from services import sync_service
from routers.auth import get_current_user

# Crear tablas si no existen
sql_models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Modelos Pydantic para recibir datos
class SyncData(BaseModel):
    empleados: Dict[str, Any]
    cuadrantes: Dict[str, Any] # Estructura anidada anio -> mes -> lista vigilantes
    config_turnos: Dict[str, Any]
    festivos: Optional[Dict[str, Any]] = None

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
        sync_service.sync_data(db, data.dict())
        return {"status": "success", "message": "Sincronización completada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en sincronización: {str(e)}")
