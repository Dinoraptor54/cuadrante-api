import requests

BASE_URL = "https://cuadrante-api.onrender.com"
LOGIN_URL = f"{BASE_URL}/api/auth/login"

CREDENTIALS = {
    "username": "coordinador@capi.com",
    "password": "admin123"
}

print(f"🔍 Probando login en: {LOGIN_URL}")
print(f"👤 Usuario: {CREDENTIALS['username']}")

try:
    response = requests.post(LOGIN_URL, data=CREDENTIALS)
    
    print(f"📡 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ LOGIN EXITOSO!")
        print(f"🔑 Token recibido: {data.get('access_token')[:20]}...")
    else:
        print("❌ LOGIN FALLIDO")
        print(f"📄 Respuesta: {response.text}")

except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN: {e}")
