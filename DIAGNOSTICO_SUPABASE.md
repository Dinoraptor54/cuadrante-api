# 🔍 Diagnóstico Completo del Error de Conexión a Supabase

## Posibles Causas del Error "No se encontró el inquilino o usuario"

### 1. ❌ Formato de Usuario Incorrecto
**Síntoma**: Error al conectar con el pooler de Supabase

**Formatos posibles**:
```bash
# ❌ INCORRECTO - Solo postgres
postgresql://postgres:PASSWORD@aws-1-eu-central-1.pooler.supabase.com:6543/postgres

# ✅ CORRECTO - Con project ID
postgresql://postgres.wmnnbkkiskfvbxdgxcby:PASSWORD@aws-1-eu-central-1.pooler.supabase.com:6543/postgres
```

### 2. ❌ Usar Pooler en lugar de Conexión Directa
**Problema**: El pooler requiere autenticación diferente

**Solución**: Usar conexión directa en puerto 5432:
```bash
postgresql://postgres.wmnnbkkiskfvbxdgxcby:PASSWORD@aws-1-eu-central-1.compute-1.amazonaws.com:5432/postgres
```

### 3. ❌ Contraseña con Caracteres Especiales sin Codificar
**Problema**: Caracteres como `@`, `#`, `!` deben estar URL-encoded

**Ejemplos**:
- `@` → `%40`
- `#` → `%23`
- `!` → `%21`
- `$` → `%24`

### 4. ❌ Proyecto en Pausa o Credenciales Incorrectas
**Verificar en Supabase**:
1. Ve a tu proyecto en Supabase
2. Settings → Database
3. Verifica que el proyecto esté activo
4. Copia la "Connection string" correcta

## 🔧 Soluciones a Probar (en orden)

### Opción 1: Conexión Directa (Recomendada)
```bash
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-1-eu-central-1.compute-1.amazonaws.com:5432/postgres
```

### Opción 2: Session Pooler
```bash
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-1-eu-central-1.pooler.supabase.com:5432/postgres
```

### Opción 3: Transaction Pooler (puerto 6543)
```bash
postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor%40ptor55.@aws-1-eu-central-1.pooler.supabase.com:6543/postgres
```

## 📝 Pasos para Obtener la URL Correcta desde Supabase

1. Ve a: https://supabase.com/dashboard/project/wmnnbkkiskfvbxdgxcby
2. Click en "Settings" (⚙️) en el menú lateral
3. Click en "Database"
4. Busca la sección "Connection string"
5. Selecciona "URI" (no "Connection pooling")
6. Copia la URL completa
7. Reemplaza `[YOUR-PASSWORD]` con `Dinor%40ptor55.`

## 🧪 Verificación Local

Antes de configurar en Render, prueba la conexión localmente:

```bash
# En tu terminal local
psql "postgresql://postgres.wmnnbkkiskfvbxdgxcby:Dinor@ptor55.@aws-1-eu-central-1.compute-1.amazonaws.com:5432/postgres"
```

Si esto funciona, usa esa misma URL en Render (con la contraseña URL-encoded).
