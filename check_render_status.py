"""
Script para verificar el estado de la API en Render
"""
import requests
import time

# URL de la API en Render
BASE_URL = "https://cuadrante-api.onrender.com"

print("🔍 Verificando estado de cuadrante-api en Render...\n")
print(f"URL base: {BASE_URL}\n")

# Endpoints a probar
endpoints = [
    "/",
    "/health",
    "/docs",
]

for endpoint in endpoints:
    url = f"{BASE_URL}{endpoint}"
    print(f"Probando: {endpoint}")
    
    try:
        response = requests.get(url, timeout=30)
        print(f"  ✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            # Mostrar un preview de la respuesta
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                print(f"  📄 Respuesta JSON: {response.json()}")
            elif 'text/html' in content_type:
                print(f"  📄 Respuesta HTML (primeros 200 chars): {response.text[:200]}...")
            else:
                print(f"  📄 Content-Type: {content_type}")
        else:
            print(f"  ⚠️ Respuesta: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print(f"  ❌ TIMEOUT - El servidor no respondió en 30 segundos")
        print(f"     Esto puede indicar que:")
        print(f"     - El servicio está inactivo (free tier de Render se suspende)")
        print(f"     - Hay un error que impide que el servidor inicie")
        
    except requests.exceptions.ConnectionError as e:
        print(f"  ❌ ERROR DE CONEXIÓN: {str(e)[:100]}")
        
    except Exception as e:
        print(f"  ❌ ERROR: {type(e).__name__}: {str(e)[:100]}")
    
    print()

print("\n" + "="*60)
print("DIAGNÓSTICO:")
print("="*60)
print("""
Si todos los endpoints dan TIMEOUT:
  → El servicio probablemente está inactivo o suspendido
  → En el plan gratuito de Render, los servicios se suspenden tras 15 min de inactividad
  → Solución: Accede manualmente a la URL para "despertar" el servicio
  
Si hay errores 500:
  → Hay un problema con la aplicación (probablemente la conexión a Supabase)
  → Revisa los logs en Render para ver el error específico
  
Si responde correctamente:
  → ¡Todo está funcionando! ✅
""")
