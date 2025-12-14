# -*- coding: utf-8 -*-
"""
Script para verificar todos los datos en la base de datos
"""
from models.database import SessionLocal
from models.sql_models import Empleado, Turno, User, Permuta, Vacacion, ConfiguracionTurno

db = SessionLocal()

print("=" * 60)
print("DATOS EN LA BASE DE DATOS cuadrante.db")
print("=" * 60)

# Empleados
empleados = db.query(Empleado).all()
print(f"\n[EMPLEADOS]: {len(empleados)}")
for emp in empleados:
    print(f"  - {emp.nombre_completo} ({emp.email or 'sin email'})")

# Usuarios
users = db.query(User).all()
print(f"\n[USUARIOS]: {len(users)}")
for u in users:
    print(f"  - {u.email} (Rol: {u.role})")

# Turnos
turnos = db.query(Turno).all()
print(f"\n[TURNOS]: {len(turnos)}")
if turnos:
    # Agrupar por año/mes
    turnos_por_mes = {}
    for t in turnos:
        key = f"{t.anio}-{t.mes:02d}"
        turnos_por_mes[key] = turnos_por_mes.get(key, 0) + 1
    
    for mes, count in sorted(turnos_por_mes.items()):
        print(f"  - {mes}: {count} turnos")

# Permutas
permutas = db.query(Permuta).all()
print(f"\n[PERMUTAS]: {len(permutas)}")
for p in permutas[:5]:
    print(f"  - {p.estado} - {p.fecha_solicitud}")

# Vacaciones
vacaciones = db.query(Vacacion).all()
print(f"\n[VACACIONES]: {len(vacaciones)}")

# Configuración de turnos
config_turnos = db.query(ConfiguracionTurno).all()
print(f"\n[CONFIGURACION TURNOS]: {len(config_turnos)}")
for cfg in config_turnos:
    print(f"  - {cfg.codigo}: {cfg.nombre} ({cfg.hora_inicio or 'sin hora'} - {cfg.hora_fin or 'sin hora'})")

print("\n" + "=" * 60)
print("RESUMEN:")
print("=" * 60)
print(f"Total empleados: {len(empleados)}")
print(f"Total usuarios: {len(users)}")
print(f"Total turnos: {len(turnos)}")
print(f"Total permutas: {len(permutas)}")
print(f"Total vacaciones: {len(vacaciones)}")
print(f"Total config turnos: {len(config_turnos)}")
print("=" * 60)

db.close()
