# -*- coding: utf-8 -*-
"""
Script para poblar BD con datos de prueba
"""

from models.database import SessionLocal
from models.sql_models import Empleado, User, Turno, Permuta
from services.auth_service import get_password_hash
from datetime import datetime, timedelta

def populate_test_data():
    """Poblamos la BD con datos de prueba"""
    db = SessionLocal()
    
    # Verificar si ya hay datos
    count = db.query(Empleado).count()
    if count > 0:
        print("ℹ️ BD ya contiene datos, no se sobrescribe")
        db.close()
        return
    
    # Crear empleados
    print("📝 Creando empleados...")
    empleados = [
        Empleado(
            nombre_completo="Juan García López",
            email="juan@example.com",
            telefono="611234567",
            dni="12345678A",
            categoria="Vigilante"
        ),
        Empleado(
            nombre_completo="María López Rodríguez",
            email="maria@example.com",
            telefono="622345678",
            dni="87654321B",
            categoria="Coordinador"
        ),
        Empleado(
            nombre_completo="Carlos Pérez Martínez",
            email="carlos@example.com",
            telefono="633456789",
            dni="11223344C",
            categoria="Vigilante"
        ),
        Empleado(
            nombre_completo="Ana Sánchez Ruiz",
            email="ana@example.com",
            telefono="644567890",
            dni="55667788D",
            categoria="Vigilante"
        ),
    ]
    db.add_all(empleados)
    db.commit()
    print(f"✅ {len(empleados)} empleados creados")
    
    # Crear usuarios
    print("👤 Creando usuarios...")
    usuarios = [
        User(
            email="juan@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Juan García López",
            role="vigilante"
        ),
        User(
            email="maria@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="María López Rodríguez",
            role="coordinador"
        ),
        User(
            email="carlos@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Carlos Pérez Martínez",
            role="vigilante"
        ),
        User(
            email="ana@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Ana Sánchez Ruiz",
            role="vigilante"
        ),
    ]
    db.add_all(usuarios)
    db.commit()
    print(f"✅ {len(usuarios)} usuarios creados")
    
    # Crear turnos para diciembre 2025
    print("📅 Creando turnos...")
    turnos = []
    codigos_turnos = ["N", "D", "L", "M"]  # Noche, Día, Libra, Madrugada
    
    for dia in range(1, 31):
        for idx, empleado in enumerate(empleados):
            codigo = codigos_turnos[idx % len(codigos_turnos)]
            turno = Turno(
                empleado_id=empleado.id,
                anio=2025,
                mes=12,
                dia=dia,
                codigo_turno=codigo
            )
            turnos.append(turno)
    
    db.add_all(turnos)
    db.commit()
    print(f"✅ {len(turnos)} turnos creados")
    
    # Crear una permuta de ejemplo
    print("🔄 Creando permutas...")
    permuta = Permuta(
        solicitante_id=1,  # Juan
        receptor_id=2,     # María
        fecha_origen="2025-12-15",
        fecha_destino="2025-12-20",
        estado="pendiente",
        motivo="Necesito cambiar estos turnos por un asunto familiar"
    )
    db.add(permuta)
    db.commit()
    print("✅ Permuta de ejemplo creada")
    
    db.close()
    print("\n✅ ¡Datos de prueba poblados correctamente!")

if __name__ == "__main__":
    populate_test_data()
