import requests
import sys

API_URL = "https://cuadrante-api.onrender.com"

try:
    print(f"Checking {API_URL}/health...")
    r = requests.get(f"{API_URL}/health", timeout=10)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
    if r.status_code == 200:
        print("✅ API is HEALTHY")
    else:
        print("❌ API returned non-200 status")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
