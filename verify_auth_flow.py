import requests
import sys

BASE_URL = "http://localhost:8000/api/auth"

def test_auth_flow():
    # 1. Register a new user
    email = "test_user@example.com"
    password = "securepassword123"
    
    print(f"1. Registering user {email}...")
    register_data = {
        "email": email,
        "password": password,
        "full_name": "Test User",
        "role": "vigilante"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", json=register_data)
        if response.status_code == 200:
            print("   SUCCESS: User registered.")
        elif response.status_code == 400 and "already registered" in response.text:
            print("   NOTE: User already exists, proceeding to login.")
        else:
            print(f"   FAILURE: Registration failed. Status: {response.status_code}, Body: {response.text}")
            return
    except Exception as e:
        print(f"   ERROR: Could not connect to server. Is it running? {e}")
        return

    # 2. Login with correct credentials
    print("\n2. Logging in with correct credentials...")
    login_data = {"username": email, "password": password}
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    
    token = None
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"   SUCCESS: Login successful. Token received.")
    else:
        print(f"   FAILURE: Login failed. Status: {response.status_code}, Body: {response.text}")
        return

    # 3. Login with incorrect credentials
    print("\n3. Testing login with WRONG password...")
    wrong_login_data = {"username": email, "password": "wrongpassword"}
    response = requests.post(f"{BASE_URL}/login", data=wrong_login_data)
    
    if response.status_code == 401:
        print("   SUCCESS: Login rejected as expected.")
    else:
        print(f"   FAILURE: Unexpected status for wrong password. Status: {response.status_code}")

    # 4. Access protected endpoint (/me)
    if token:
        print("\n4. Accessing protected endpoint /me...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/me", headers=headers)
        
        if response.status_code == 200:
            user_info = response.json()
            if user_info["email"] == email:
               print(f"   SUCCESS: Protected data retrieved correctly. User: {user_info['email']}")
            else:
               print(f"   FAILURE: User email mismatch. Got: {user_info['email']}")
        else:
            print(f"   FAILURE: Could not access protected endpoint. Status: {response.status_code}")

if __name__ == "__main__":
    test_auth_flow()
