# ✅ SOLUCIÓN CONFIRMADA: Usar AWS-1

He verificado localmente tu conexión y **he encontrado el problema exacto**.

El error `Tenant or user not found` ocurre porque tu proyecto está alojado en el cluster `aws-1` de Supabase, pero estabas intentando conectar al `aws-0`.

## 🚀 La URL DEFINITIVA para Render

Copia y pega **exactamente** esta URL en Render. Esta ha sido probada y FUNCIONA:

```
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-1-eu-central-1.pooler.supabase.com:5432/postgres
```

### Pasos finales:
1. Ve a **Render** → **Environment**.
2. Edita `DATABASE_URL`.
3. Pega la URL de arriba (con `aws-1` y puerto `5432`).
4. Guarda los cambios.

Render rededesplegará y **esta vez debería funcionar**.
