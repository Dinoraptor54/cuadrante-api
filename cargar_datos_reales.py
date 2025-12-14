# -*- coding: utf-8 -*-
"""
Carga los datos REALES del usuario desde los JSONs
en lugar de los datos ficticios
"""

import json
import sys
from pathlib import Path

sys.path.append('.')

from models.database import SessionLocal
from models.sql_models import Empleado, Turno, User
from utils.security import get_password_hash

# Rutas a los datos reales
DATOS_DIR = Path(r'c:\mis proyectos dino\baul de proyectos\proyectos con gemini\proyecto en marcha\datos_cuadrante')
EMPLEADOS_JSON = DATOS_DIR / 'empleados.json'
CUADRANTES_JSON = DATOS_DIR / 'cuadrantes.json'

def cargar_datos_reales():
    """Carga datos reales desde JSONs"""
    db = SessionLocal()
    
    try:
        # Limpiar datos anteriores
        print("🗑️  Limpiando datos anteriores...")
        db.query(Turno).delete()
        db.query(Empleado).delete()
        db.commit()
        
        # Cargar empleados reales
        print("👥 Cargando empleados reales...")
        with open(EMPLEADOS_JSON, 'r', encoding='utf-8') as f:
            empleados_json = json.load(f)
        
        empleados_map = {}  # nombre -> id
        for nombre, datos in empleados_json.items():
            emp = Empleado(
                nombre_completo=nombre,
                email=datos.get('email', ''),
                telefono=datos.get('telefono', ''),
                categoria=datos.get('categoria', 'Vigilante de Seguridad'),
                fecha_alta=datos.get('fecha_antiguedad', '')
            )
            db.add(emp)
            db.flush()
            empleados_map[nombre] = emp.id
            print(f"  ✅ {nombre}")
        
        db.commit()
        print(f"✅ {len(empleados_map)} empleados cargados")
        
        # Cargar cuadrante (turnos)
        print("\n📅 Cargando cuadrante (turnos)...")
        with open(CUADRANTES_JSON, 'r', encoding='utf-8') as f:
            cuadrantes_json = json.load(f)
        
        total_turnos = 0
        # Iterar por año/mes
        for anio_str, meses in cuadrantes_json.items():
            anio = int(anio_str)
            for mes_str, empleados_mes in meses.items():
                # Saltar keys con sufijo _cambios
                if '_cambios' in mes_str or not mes_str.isdigit():
                    continue
                
                mes = int(mes_str)
                
                for empleado_data in empleados_mes:
                    nombre = empleado_data['nombre']
                    if nombre not in empleados_map:
                        print(f"  ⚠️  Empleado no encontrado: {nombre}")
                        continue
                    
                    empleado_id = empleados_map[nombre]
                    turnos_dict = empleado_data.get('turnos', {})
                    
                    for dia_str, codigo in turnos_dict.items():
                        dia = int(dia_str)
                        turno = Turno(
                            empleado_id=empleado_id,
                            anio=anio,
                            mes=mes,
                            dia=dia,
                            codigo_turno=codigo
                        )
                        db.add(turno)
                        total_turnos += 1
        
        db.commit()
        print(f"✅ {total_turnos} turnos cargados")
        
        # Mostrar resumen
        print(f"\n{'='*50}")
        print("RESUMEN DE DATOS CARGADOS:")
        print(f"{'='*50}")
        
        # Turnos por mes/año
        for anio_str, meses in cuadrantes_json.items():
            for mes_str, empleados_mes in meses.items():
                total_mes = sum(
                    len(emp.get('turnos', {})) 
                    for emp in empleados_mes
                )
                print(f"  {anio_str}-{mes_str}: {total_mes} turnos")
        
        print(f"\n✅ ¡Datos reales cargados correctamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == '__main__':
    cargar_datos_reales()
