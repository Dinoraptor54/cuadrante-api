import requests

API_URL = "https://cuadrante-api.onrender.com"

# Login
print("Logging in...")
r = requests.post(f"{API_URL}/api/auth/login", data={
    "username": "coordinador@capi.com",
    "password": "admin123"
})
token = r.json()["access_token"]
print(f"Token: {token[:20]}...")

# Get schedule
print("\nFetching schedule for Jan 2026...")
r = requests.get(f"{API_URL}/api/schedule/2026/1", headers={
    "Authorization": f"Bearer {token}"
})

print(f"Status: {r.status_code}")
data = r.json()
print(f"\nResponse structure:")
print(f"Keys: {data.keys()}")
print(f"\nFull response:")
import json
print(json.dumps(data, indent=2, ensure_ascii=False))
