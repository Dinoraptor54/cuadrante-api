import requests
import json

API_URL = "https://cuadrante-api.onrender.com"

def get_token():
    print("Authenticating...")
    r = requests.post(f"{API_URL}/api/auth/login", data={
        "username": "coordinador@capi.com",
        "password": "admin123"
    })
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        return None
    return r.json()["access_token"]

def check_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Get Employees
    print("\n--- Fetching Employees ---")
    r = requests.get(f"{API_URL}/api/empleados/", headers=headers, params={"limit": 100})
    if r.status_code == 200:
        response_data = r.json()
        # Handle if it's a list or dict with items
        empleados = response_data if isinstance(response_data, list) else response_data.get("items", [])
        
        print(f"Found {len(empleados)} employees.")
        for emp in empleados:
            print(f"ID: {emp.get('id')} - Name: {emp.get('nombre_completo')}")
            
            # 2. Check Schedule for first employee found
            print(f"  Checking schedule for {emp.get('nombre_completo')} (Nov 2025)...")
            r_sched = requests.get(f"{API_URL}/api/schedule/2025/11", headers=headers)
            if r_sched.status_code == 200:
                schedule = r_sched.json()
                print(f"  Schedule response keys: {schedule.keys()}")
                # Assuming structure, verify if user has shifts
                # This depends on API structure, usually it returns a list or dict keyed by ID
                user_shifts = schedule.get(str(emp.get('id')), [])
                # Or maybe it returns a list of all shifts?
                # Let's print a sample to confirm structure
                print(f"  Sample Data: {str(schedule)[:200]}...")
            else:
                print(f"  Failed to get schedule: {r_sched.status_code}")
            
            # Break after first one to check structure
            break
    else:
        print(f"Failed to fetch employees: {r.status_code}")

if __name__ == "__main__":
    token = get_token()
    if token:
        check_data(token)
