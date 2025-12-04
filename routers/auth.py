# -*- coding: utf-8 -*-
"""
Router de autenticación
Maneja login, registro y generación de tokens JWT
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

router = APIRouter()

# Configuración
SECRET_KEY = os.getenv("SECRET_KEY", "clave_temporal_desarrollo")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 días

# Contexto de encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Modelos Pydantic
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict


class UserInfo(BaseModel):
    email: str
    nombre: str
    rol: str


# Funciones auxiliares
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contraseña coincida con el hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera hash de contraseña"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Obtiene usuario actual desde el token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return {"email": email, "nombre": payload.get("nombre"), "rol": payload.get("rol")}
    except JWTError:
        raise credentials_exception


# Endpoints
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login de usuario
    Devuelve token JWT si las credenciales son correctas
    """
    # TODO: Verificar contra base de datos
    # Por ahora, usuario de prueba
    if form_data.username == "admin@example.com" and form_data.password == "admin123":
        user_data = {
            "sub": form_data.username,
            "nombre": "Administrador",
            "rol": "coordinador"
        }
        
        access_token = create_access_token(data=user_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "email": form_data.username,
                "nombre": "Administrador",
                "rol": "coordinador"
            }
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email o contraseña incorrectos",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/me", response_model=UserInfo)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Obtiene información del usuario actual"""
    return current_user


@router.post("/register")
async def register(user: UserLogin):
    """
    Registro de nuevo usuario
    TODO: Implementar creación en base de datos
    """
    # Por ahora, solo devuelve éxito
    return {
        "message": "Usuario registrado correctamente",
        "email": user.email
    }
