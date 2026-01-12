# 🚨 SOLUCIÓN IMPORTANTE: Error IPv6 "Network is unreachable"

El error que has pegado es **clave** para resolver el problema:

```
connection to server at "db.wmnnbkkiskfvbxdgxcby.supabase.co" (2a05:d014:1c06:5f31:c59a:4f3c:2523:47da), port 5432 failed: Network is unreachable
```

## 🧠 ¿Qué significa este error?
1. **Render está intentando conectar por IPv6** (la dirección `2a05:...`).
2. **`db.wmnnbkkiskfvbxdgxcby.supabase.co`** es la dirección de conexión directa, que a menudo resuelve a IPv6.
3. **Render no puede alcanzar esa dirección IPv6**, por eso dice "Network is unreachable".

## ✅ La Solución Definitiva
Debes usar la dirección del **Pooler de Supabase**, que fuerza el uso de **IPv4** y es más compatible con Render.

### 1. Copia EXACTAMENTE esta URL:

```
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
```

*(Si esta no funciona, prueba cambiando `aws-0` por `aws-1`)*

### 2. Pasos en Render:
1. Ve a **Environment** en el dashboard.
2. Edita `DATABASE_URL`.
3. **Borra lo que hay** y pega la URL de arriba.
4. **Guarda cambios**.
5. Render rededesplegará automáticamente.

### 3. ¿Por qué es diferente a lo que tenías?
*   ❌ **Tenías:** `... @db.wmnnbkkiskfvbxdgxcby.supabase.co ...` (Directo IPv6, falla en Render)
*   ✅ **Nueva:** `... @aws-0-eu-central-1.pooler.supabase.com ...` (Pooler IPv4, funciona en Render)

---

> **Nota:** El puerto **5432** en el pooler actúa como "Session Mode", que es compatible con la mayoría de las conexiones directas pero usa la infraestructura de red del pooler que es más estable.
