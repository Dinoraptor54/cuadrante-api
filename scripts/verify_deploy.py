#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que el deployment en Railway funciona correctamente
Uso: python scripts/verify_deploy.py https://tu-app.railway.app
"""

import sys
import requests
from typing import Dict, Any


def check_endpoint(base_url: str, endpoint: str, description: str) -> bool:
    """Verifica que un endpoint responda correctamente"""
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {description}: OK")
            return True
        else:
            print(f"❌ {description}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {description}: {str(e)}")
        return False


def test_login(base_url: str, email: str, password: str) -> str:
    """Prueba el login y devuelve el token si funciona"""
    url = f"{base_url}/api/auth/login"
    try:
        response = requests.post(
            url,
            data={"username": email, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Login exitoso: {email}")
            return token
        else:
            print(f"❌ Login fallido: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None


def test_protected_endpoint(base_url: str, token: str) -> bool:
    """Prueba un endpoint protegido con el token"""
    url = f"{base_url}/api/empleados"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            empleados_count = len(data.get("empleados", []))
            print(f"✅ Endpoint protegido OK: {empleados_count} empleados")
            return True
        else:
            print(f"❌ Endpoint protegido: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Endpoint protegido error: {str(e)}")
        return False


def verify_deploy(base_url: str):
    """Verifica el deployment completo"""
    
    print("=" * 60)
    print(f"VERIFICANDO DEPLOYMENT: {base_url}")
    print("=" * 60)
    print()
    
    # Remover trailing slash
    base_url = base_url.rstrip("/")
    
    # 1. Health check
    print("1. Health Check")
    health_ok = check_endpoint(base_url, "/health", "Health endpoint")
    print()
    
    # 2. API Root
    print("2. API Root")
    api_ok = check_endpoint(base_url, "/api/", "API root endpoint")
    print()
    
    # 3. Swagger docs
    print("3. Swagger Documentation")
    docs_ok = check_endpoint(base_url, "/docs", "Swagger UI")
    print()
    
    # 4. Test login
    print("4. Test de Autenticación")
    print("   Probando con usuario admin...")
    token = test_login(base_url, "admin@example.com", "admin123")
    print()
    
    # 5. Test endpoint protegido
    if token:
        print("5. Test de Endpoint Protegido")
        protected_ok = test_protected_endpoint(base_url, token)
        print()
    else:
        print("5. Test de Endpoint Protegido")
        print("⚠️  Saltado (no hay token)")
        print()
        protected_ok = False
    
    # Resumen
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    results = {
        "Health Check": health_ok,
        "API Root": api_ok,
        "Swagger Docs": docs_ok,
        "Login": token is not None,
        "Endpoint Protegido": protected_ok
    }
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {name}")
    
    print()
    print(f"Resultado: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("🎉 ¡Deployment verificado exitosamente!")
        return 0
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar configuración.")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/verify_deploy.py https://tu-app.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1]
    exit_code = verify_deploy(base_url)
    sys.exit(exit_code)
