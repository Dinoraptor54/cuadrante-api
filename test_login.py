import requests

url = "http://localhost:8000/api/auth/login"
payload = {
    "username": "coordinador@capi.com",
    "password": "admin"
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
    response = requests.post(url, data=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
