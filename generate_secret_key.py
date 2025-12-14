#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera una SECRET_KEY segura para producción
Usa secrets para generar 32 bytes aleatorios (256 bits)
"""

import secrets
import base64

def generate_secret_key():
    """Genera una SECRET_KEY criptográficamente segura"""
    # Generar 32 bytes aleatorios (256 bits)
    random_bytes = secrets.token_bytes(32)
    
    # Convertir a base64 para que sea string
    secret_key = base64.b64encode(random_bytes).decode('utf-8')
    
    return secret_key


if __name__ == "__main__":
    print("=" * 60)
    print("GENERADOR DE SECRET_KEY SEGURA")
    print("=" * 60)
    print()
    
    # Generar 3 opciones
    print("Aquí tienes 3 SECRET_KEYs seguras (elige una):")
    print()
    
    for i in range(3):
        key = generate_secret_key()
        print(f"{i+1}. {key}")
    
    print()
    print("=" * 60)
    print("INSTRUCCIONES:")
    print("=" * 60)
    print("1. Copia UNA de las claves de arriba")
    print("2. En Railway Settings -> Variables")
    print("3. Añade: SECRET_KEY=[clave copiada]")
    print("4. NO compartas esta clave públicamente")
    print("=" * 60)
