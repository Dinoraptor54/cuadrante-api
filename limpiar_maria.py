# -*- coding: utf-8 -*-
"""
Script para limpiar datos de María del Val Rodriguez
Ella trabajó hasta mediados de agosto (día 20), eliminar registros posteriores
"""

import json
from pathlib import Path

# Ruta al archivo de cuadrantes
CUADRANTES_PATH = Path("../baul de proyectos/proyectos con gemini/proyecto en marcha/proyecto_modulo_cuadrante/datos_cuadrante/cuadrantes.json")

# Cargar datos
with open(CUADRANTES_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Buscando registros de Del Val Rodriguez Maria...")
print("=" * 60)

# Buscar y mostrar dónde aparece
for year, meses in data.items():
    for mes, vigilantes in meses.items():
        if isinstance(vigilantes, list):
            for v in vigilantes:
                if v.get('nombre') == 'Del Val Rodriguez Maria':
                    turnos = v.get('turnos', {})
                    dias = sorted([int(d) for d in turnos.keys()])
                    print(f"\nAño {year}, Mes {mes}:")
                    print(f"  Dias trabajados: {dias}")
                    
                    # Si es agosto (mes 8) y año 2025, solo mantener hasta día 20
                    if year == "2025" and mes == "8":
                        print(f"  -> AGOSTO 2025: Manteniendo solo hasta día 20")
                        # Filtrar turnos
                        turnos_filtrados = {dia: turno for dia, turno in turnos.items() if int(dia) <= 20}
                        v['turnos'] = turnos_filtrados
                        print(f"  -> Turnos después del filtro: {sorted([int(d) for d in turnos_filtrados.keys()])}")

print("\n" + "=" * 60)
print("Guardando cambios...")

# Guardar archivo actualizado
with open(CUADRANTES_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Archivo actualizado correctamente!")
print("\nResumen:")
print("- María del Val trabajó hasta el 20 de agosto de 2025")
print("- Se eliminaron sus turnos posteriores a esa fecha")
