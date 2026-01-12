# ✅ SOLUCIÓN CONFIRMADA: Guía de Despliegue Render

Este documento resume la configuración crítica para que el proyecto funcione en Render.

## 1. Conexión a Base de Datos (Supabase)

El problema principal era la conexión IPv6 y el cluster incorrecto.
Usa **EXACTAMENTE** esta URL en la variable de entorno `DATABASE_URL` de Render:

```
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-1-eu-central-1.pooler.supabase.com:5432/postgres
```

**Puntos clave:**
- **Host:** `aws-1-eu-central-1.pooler.supabase.com` (No aws-0, no db.supabase.co).
- **Puerto:** `5432` (Session Pooler).
- **Usuario:** `postgres.wmnnbkkiskfvbxdgxcby`.

## 2. Configuración del Frontend y CORS

Para que el login funcione desde la web (`https://cuadrante-api.onrender.com`):

### A. CORS (Backend)
En `config.py` (controlado por variable de entorno `ALLOWED_ORIGINS`):
- **Valor:** `*` (Permitir todo).
- Esto evita bloqueos del navegador al hacer peticiones API.

### B. JavaScript (Frontend)
El archivo `static/js/api.js` fuerza la conexión a producción:
- **API URL:** `https://cuadrante-api.onrender.com`

---
**Estado Final: 🚀 LISTO**
- La API arranca correctamente (Fix `Depends` en main.py).
- La BD tiene datos (Usuario `coordinador@capi.com` / `admin123`).
- El login funciona y muestra errores visibles si fallase.
