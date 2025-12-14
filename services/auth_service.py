# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from models import sql_models
from utils.security import verify_password, get_password_hash
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[sql_models.User]:
    """Busca un usuario por email"""
    return db.query(sql_models.User).filter(sql_models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[sql_models.User]:
    """Identifica al usuario verificando email y contraseña"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, user_data: dict) -> sql_models.User:
    """Crea un nuevo usuario en la base de datos"""
    hashed_password = get_password_hash(user_data["password"])
    db_user = sql_models.User(
        email=user_data["email"],
        hashed_password=hashed_password,
        full_name=user_data.get("full_name", ""),
        role=user_data.get("role", "vigilante"),
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
