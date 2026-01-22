import requests
import sys

API_URL = "https://cuadrante-api.onrender.com"

def check_health():
    print(f"Checking health at {API_URL}/health ...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=60)
        print(f"Health Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error checking health: {e}")
        with open("connection_error.log", "w") as f:
            f.write(str(e))
        return False

def check_login():
    print(f"\nChecking login at {API_URL}/api/auth/login ...")
    try:
        response = requests.post(f"{API_URL}/api/auth/login", data={
            "username": "coordinador@capi.com",
            "password": "admin123"
        }, timeout=10)
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            print("Login Successful")
            print(f"Token: {response.json().get('access_token')[:10]}...")
            return True
        else:
            print(f"Login Failed: {response.text}")
            return False
    except Exception as e:
        print(f"Error checking login: {e}")
        return False

if __name__ == "__main__":
    health = check_health()
    if health:
        check_login()
    else:
        print("Skipping login check due to health check failure.")
