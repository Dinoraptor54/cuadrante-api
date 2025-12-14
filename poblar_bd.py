# -*- coding: utf-8 -*-
"""
Script para poblar la base de datos con datos reales del proyecto desktop
Ejecutar: python poblar_bd.py
"""

import json
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Importar modelos y base de datos
from models.database import SessionLocal, engine
from models import sql_models

# Crear todas las tablas
sql_models.Base.metadata.create_all(bind=engine)

# Contexto de encriptación (usando SHA256 en lugar de bcrypt por compatibilidad)
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Ruta a los datos del proyecto desktop
DESKTOP_DATA_PATH = Path("../baul de proyectos/proyectos con gemini/proyecto en marcha/proyecto_modulo_cuadrante/datos_cuadrante")

def cargar_json(archivo: str) -> dict:
    """Carga un archivo JSON desde la carpeta de datos"""
    ruta = DESKTOP_DATA_PATH / archivo
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Archivo no encontrado: {ruta}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer JSON {archivo}: {e}")
        return {}


def poblar_usuarios(db: Session):
    """Crea usuarios de prueba basados en los empleados"""
    print("\n[*] Creando usuarios...")
    
    empleados_data = cargar_json("empleados.json")
    
    # Usuario coordinador (basado en Molina Alés Eugenia - Jefe de Equipo)
    coordinador = db.query(sql_models.User).filter(
        sql_models.User.email == "coordinador@capi.com"
    ).first()
    
    if not coordinador:
        coordinador = sql_models.User(
            email="coordinador@capi.com",
            hashed_password=pwd_context.hash("admin"),
            full_name="Molina Alés Eugenia",
            role="coordinador",
            is_active=True
        )
        db.add(coordinador)
        print("  [OK] Usuario coordinador creado: coordinador@capi.com / admin")
    
    # Usuarios vigilantes
    usuarios_creados = 0
    for nombre, datos in empleados_data.items():
        email = datos.get("email")
        if not email or email == "":
            # Generar email basado en el nombre
            email = nombre.lower().replace(" ", ".") + "@capi.com"
        
        # Verificar si ya existe
        usuario_existente = db.query(sql_models.User).filter(
            sql_models.User.email == email
        ).first()
        
        if not usuario_existente:
            rol = "coordinador" if datos.get("categoria") == "Jefe de Equipo" else "vigilante"
            
            nuevo_usuario = sql_models.User(
                email=email,
                hashed_password=pwd_context.hash("pass"),  # Contraseña por defecto
                full_name=nombre,
                role=rol,
                is_active=True
            )
            db.add(nuevo_usuario)
            usuarios_creados += 1
    
    db.commit()
    print(f"  [OK] {usuarios_creados} usuarios vigilantes creados (password: pass)")


def poblar_empleados(db: Session):
    """Pobla la tabla de empleados con datos reales"""
    print("\n[*] Poblando empleados...")
    
    empleados_data = cargar_json("empleados.json")
    empleados_creados = 0
    
    for nombre, datos in empleados_data.items():
        # Verificar si ya existe
        empleado_existente = db.query(sql_models.Empleado).filter(
            sql_models.Empleado.nombre_completo == nombre
        ).first()
        
        if not empleado_existente:
            email = datos.get("email", "")
            if not email:
                email = nombre.lower().replace(" ", ".") + "@capi.com"
            
            nuevo_empleado = sql_models.Empleado(
                nombre_completo=nombre,
                email=email,
                telefono=datos.get("telefono", ""),
                dni=datos.get("dni", ""),
                fecha_alta=datos.get("fecha_antiguedad", ""),
                categoria=datos.get("categoria", "Vigilante de Seguridad")
            )
            db.add(nuevo_empleado)
            empleados_creados += 1
    
    db.commit()
    print(f"  [OK] {empleados_creados} empleados creados")


def poblar_configuracion_turnos(db: Session):
    """Pobla la configuración de turnos"""
    print("\n[*] Poblando configuracion de turnos...")
    
    turnos_data = cargar_json("turnos.json")
    turnos_creados = 0
    
    for codigo, datos in turnos_data.items():
        # Verificar si ya existe
        config_existente = db.query(sql_models.ConfiguracionTurno).filter(
            sql_models.ConfiguracionTurno.codigo == codigo
        ).first()
        
        if not config_existente:
            nueva_config = sql_models.ConfiguracionTurno(
                codigo=codigo,
                descripcion=datos.get("leyenda", ""),
                horario=datos.get("leyenda", ""),
                color=datos.get("color_fondo", "#FFFFFF")
            )
            db.add(nueva_config)
            turnos_creados += 1
    
    db.commit()
    print(f"  [OK] {turnos_creados} configuraciones de turno creadas")


def poblar_turnos(db: Session):
    """Pobla los turnos de los empleados"""
    print("\n[*] Poblando turnos...")
    
    cuadrantes_data = cargar_json("cuadrantes.json")
    turnos_creados = 0
    
    # Obtener todos los empleados para mapear nombres a IDs
    empleados = db.query(sql_models.Empleado).all()
    empleados_map = {emp.nombre_completo: emp.id for emp in empleados}
    
    # Iterar sobre años y meses
    for anio_str, meses in cuadrantes_data.items():
        anio = int(float(anio_str))  # Convertir a float primero por si es '2025.0'
        
        for mes_str, vigilantes_list in meses.items():
            # Saltar entradas de cambios (ej: "11_cambios")
            if "_cambios" in mes_str or not vigilantes_list:
                continue
            
            try:
                mes = int(mes_str)
            except ValueError:
                continue
            
            # Iterar sobre vigilantes
            for vigilante_data in vigilantes_list:
                nombre = vigilante_data.get("nombre")
                turnos_dict = vigilante_data.get("turnos", {})
                
                empleado_id = empleados_map.get(nombre)
                if not empleado_id:
                    print(f"  [WARN] Empleado no encontrado: {nombre}")
                    continue
                
                # Borrar turnos existentes de este empleado en este mes/año
                db.query(sql_models.Turno).filter(
                    sql_models.Turno.empleado_id == empleado_id,
                    sql_models.Turno.anio == anio,
                    sql_models.Turno.mes == mes
                ).delete()
                
                # Insertar nuevos turnos
                for dia_str, codigo_turno in turnos_dict.items():
                    try:
                        dia = int(dia_str)
                        nuevo_turno = sql_models.Turno(
                            empleado_id=empleado_id,
                            anio=anio,
                            mes=mes,
                            dia=dia,
                            codigo_turno=codigo_turno
                        )
                        db.add(nuevo_turno)
                        turnos_creados += 1
                    except ValueError:
                        continue
    
    db.commit()
    print(f"  [OK] {turnos_creados} turnos creados")


def main():
    """Función principal"""
    print("=" * 60)
    print("POBLANDO BASE DE DATOS CON DATOS REALES")
    print("=" * 60)
    
    # Verificar que existe la carpeta de datos
    if not DESKTOP_DATA_PATH.exists():
        print(f"\n[ERROR] No se encuentra la carpeta de datos:")
        print(f"   {DESKTOP_DATA_PATH.absolute()}")
        print("\nAsegurate de que la ruta es correcta.")
        sys.exit(1)
    
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # Poblar datos
        poblar_usuarios(db)
        poblar_empleados(db)
        poblar_configuracion_turnos(db)
        poblar_turnos(db)
        
        print("\n" + "=" * 60)
        print("BASE DE DATOS POBLADA EXITOSAMENTE")
        print("=" * 60)
        
        # Mostrar estadísticas
        total_usuarios = db.query(sql_models.User).count()
        total_empleados = db.query(sql_models.Empleado).count()
        total_turnos = db.query(sql_models.Turno).count()
        total_config = db.query(sql_models.ConfiguracionTurno).count()
        
        print(f"\nEstadisticas:")
        print(f"   Usuarios: {total_usuarios}")
        print(f"   Empleados: {total_empleados}")
        print(f"   Turnos: {total_turnos}")
        print(f"   Configuraciones de turno: {total_config}")
        
        print(f"\nCredenciales de acceso:")
        print(f"   Coordinador: coordinador@capi.com / admin123")
        print(f"   Vigilantes: [email] / vigilante123")
        
    except Exception as e:
        print(f"\n[ERROR]: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
