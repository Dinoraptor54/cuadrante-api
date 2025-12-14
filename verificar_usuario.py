# -*- coding: utf-8 -*-
from models.database import SessionLocal
from models import sql_models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

db = SessionLocal()
user = db.query(sql_models.User).filter(
    sql_models.User.email == 'coordinador@capi.com'
).first()

if user:
    print(f"Usuario encontrado: {user.email}")
    print(f"Nombre: {user.full_name}")
    print(f"Rol: {user.role}")
    print(f"Hash (primeros 50 chars): {user.hashed_password[:50]}...")
    
    # Probar verificación de contraseña
    result = pwd_context.verify("admin", user.hashed_password)
    print(f"\nVerificación de contraseña 'admin': {result}")
else:
    print("Usuario NO encontrado")

db.close()
