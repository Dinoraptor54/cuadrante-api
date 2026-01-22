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
        
        # Decodificar token para ver el rol (sin verificar firma para simplicidad)
        import json
        import base64
        token = data.get('access_token')
        payload_part = token.split('.')[1]
        # Pad base64
        payload_part += '=' * (-len(payload_part) % 4)
        payload = json.loads(base64.b64decode(payload_part).decode('utf-8'))
        print(f"👮 ROL DETECTADO: {payload.get('rol')}")
        
        # --- PROBAR SYNC ---
        print("\n🔄 Probando endpoint de sincronización...")
        SYNC_URL = f"{BASE_URL}/api/sync/full"
        DUMMY_DATA = {
            "empleados": {},
            "cuadrantes": {},
            "config_turnos": {}
        }
        headers = {"Authorization": f"Bearer {data.get('access_token')}"}
        
        sync_response = requests.post(SYNC_URL, json=DUMMY_DATA, headers=headers)
        print(f"📡 Sync Status: {sync_response.status_code}")
        print(f"📄 Sync Response: {sync_response.text}")
        
    else:
        print("❌ LOGIN FALLIDO")
        print(f"📄 Respuesta: {response.text}")

except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN: {e}")
