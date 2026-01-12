# 🔧 Formato Correcto de DATABASE_URL para Supabase

## ❌ Error Actual
```
FATAL: No se encontró el inquilino o usuario
```

Este error indica que el formato del usuario en la URL de conexión es incorrecto.

## ✅ Formato Correcto para Supabase Pooler

La URL debe seguir este formato **exacto**:

```
postgresql://postgres.PROJECT_ID:PASSWORD@aws-1-eu-central-1.pooler.supabase.com:6543/postgres
```

### Componentes:
- **Usuario**: `postgres.PROJECT_ID` (ejemplo: `postgres.wmnnbkkiskfvbxdgxcby`)
- **Contraseña**: Tu contraseña URL-encoded (los caracteres especiales deben estar codificados)
  - Ejemplo: `@` → `%40`, `#` → `%23`, `!` → `%21`
- **Host**: `aws-1-eu-central-1.pooler.supabase.com`
- **Puerto**: `6543` (pooler) o `5432` (directo)
- **Base de datos**: `postgres`

## 📋 Pasos para Corregir en Render

1. Ve a tu panel de Render → `cuadrante-api` → **Ambiente**
2. Haz clic en el ícono del ojo 👁️ junto a `DATABASE_URL`
3. Verifica que el formato sea **exactamente** como se muestra arriba
4. Si encuentras errores comunes:
   - ❌ `postgres:PASSWORD@...` → ✅ `postgres.PROJECT_ID:PASSWORD@...`
   - ❌ `subabase.com` → ✅ `supabase.com`
   - ❌ Contraseña sin codificar → ✅ Contraseña URL-encoded

## 🔍 Cómo Obtener la URL Correcta desde Supabase

1. Ve a tu proyecto en Supabase
2. Settings → Database → Connection String
3. Selecciona "Transaction Pooler" o "Session Pooler"
4. Copia la URL completa
5. Reemplaza `[YOUR-PASSWORD]` con tu contraseña real (URL-encoded)

## 🚀 Después de Corregir

1. Guarda los cambios en Render
2. Render automáticamente iniciará un nuevo despliegue
3. Verifica los logs para confirmar: `Application startup complete`
