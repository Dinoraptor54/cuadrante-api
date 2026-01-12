# 🎯 SOLUCIÓN: Usar Conexión Directa en lugar de Pooler

## El Problema
El error "No se encontró el inquilino o usuario" con el Transaction Pooler (puerto 6543) sugiere que debemos usar la conexión directa.

## ✅ URL CORRECTA A USAR EN RENDER

Copia y pega EXACTAMENTE esto en el campo `DATABASE_URL` de Render:

```
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
```

### Cambios clave:
1. **Puerto**: `6543` → `5432` (Session Pooler en lugar de Transaction Pooler)
2. **Usuario**: `postgres.wmnnbkkiskfvbxdgxcby` (con el project ID)
3. **Contraseña**: `Dinor%40ptor55.` (con @ codificado como %40)

## 📋 Pasos para Aplicar en Render

1. Ve a: https://dashboard.render.com/web/srv-d5dafu75r7bs73brdhu0/env
2. Click en "Editar" (Edit)
3. Busca el campo `DATABASE_URL`
4. **Borra todo** el contenido actual
5. **Pega exactamente** la URL de arriba
6. Click en "Guardar cambios" (Save Changes)
7. Espera a que Render inicie el nuevo despliegue
8. Ve a "Logs" y busca: `Application startup complete`

## 🔄 Si Esto No Funciona

Prueba con la conexión directa (sin pooler):

```
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@db.wmnnbkkiskfvbxdgxcby.supabase.co:5432/postgres
```

O con el host alternativo:

```
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-0-eu-central-1.pooler.supabase.com:6543/postgres?pgbouncer=true
```
