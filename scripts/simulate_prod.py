
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment to PRODUCTION
os.environ["ENVIRONMENT"] = "production"
os.environ["DATABASE_URL"] = "postgresql://postgres:HbFEJUwPNwjYmovKnujYgHOVBVladdmq@hopper.proxy.rlwy.net:13339/railway"
os.environ["SECRET_KEY"] = "tu_clave_secreta_aqui_cambiar_en_produccion" 
os.environ["ALLOWED_ORIGINS"] = "https://web-production-52b18.up.railway.app"

print("🔧 SIMULANDO ARRANQUE EN PRODUCCIÓN...")
print("="*60)
print(f"DATABASE_URL: {os.environ['DATABASE_URL']}")
print(f"SECRET_KEY: {os.environ['SECRET_KEY']}")
print(f"ALLOWED_ORIGINS: {os.environ['ALLOWED_ORIGINS']}")
print("="*60)

try:
    from config import validate_settings
    if validate_settings():
        print("✅ VALIDACIÓN EXITOSA: La app debería arrancar.")
    else:
        print("❌ VALIDACIÓN FALLIDA: La app se cerrará.")
except ImportError:
    print("❌ Error de importación. Ejecutar desde la raíz del proyecto.")
except Exception as e:
    print(f"❌ Excepción inesperada: {e}")
