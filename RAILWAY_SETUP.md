# 🚀 Guía de Despliegue en Railway

Esta guía te llevará paso a paso para desplegar `cuadrante_api` en Railway.

---

## 📋 Pre-requisitos

- ✅ Cuenta en GitHub (gratuita)
- ✅ Cuenta en Railway (gratuita - $5 crédito/mes)
- ✅ Git instalado localmente

---

## 🔐 Paso 1: Generar SECRET_KEY Segura

Antes de desplegar, necesitas una clave segura:

```bash
python generate_secret_key.py
```

**Guarda una de las claves generadas** - la necesitarás en el Paso 5.

---

## 📦 Paso 2: Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `cuadrante-api`
3. Puede ser **público** o **privado**
4. **NO** marcar "Initialize with README" (ya tienes uno)
5. Click **"Create repository"**

---

## 🔗 Paso 3: Conectar Repositorio Local con GitHub

Copia el comando que GitHub te muestra, o usa estos:

```bash
# En el directorio cuadrante_api
git remote add origin https://github.com/TU_USUARIO/cuadrante-api.git

# Hacer commit de todos los cambios
git add .
git commit -m "feat: complete cuadrante_api ready for production deploy"

# Subir a GitHub
git push -u origin master
```

**Espera a que termine** - puede tardar 1-2 minutos dependiendo de tu conexión.

---

## 🚂 Paso 4: Configurar Railway

### 4.1. Crear Cuenta
1. Ve a https://railway.app/
2. Click **"Start a New Project"**
3. Inicia sesión con GitHub

### 4.2. Conectar Repositorio
1. Click **"Deploy from GitHub repo"**
2. Autoriza a Railway acceso a tus repositorios
3. Selecciona **`cuadrante-api`**
4. Railway detectará automáticamente:
   - ✅ Python
   - ✅ `Procfile`
   - ✅ `requirements.txt`

### 4.3. Añadir PostgreSQL
1. En tu proyecto Railway, click **"+ New"**
2. Selecciona **"Database"**
3. Selecciona **"Add PostgreSQL"**
4. Railway creará automáticamente la variable **`DATABASE_URL`**

---

## ⚙️ Paso 5: Configurar Variables de Entorno

En Railway:
1. Click en tu servicio (el que tiene tu código)
2. Ir a pestaña **"Variables"**
3. Añadir estas variables (click **"+ New Variable"**):

```bash
ENVIRONMENT=production
SECRET_KEY=[pegar la clave del Paso 1]
ALLOWED_ORIGINS=https://tu-app.railway.app
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
LOG_LEVEL=INFO
```

⚠️ **Importante**: El `ALLOWED_ORIGINS` debe ser exactamente tu URL de Railway.

Railway te mostrará la URL en la parte superior, algo como:
- `https://cuadrante-api-production-XXXX.up.railway.app`

**Nota**: `DATABASE_URL` ya está configurado automáticamente por Railway.

---

## 🚀 Paso 6: Desplegar

Railway hará el deploy automáticamente:

1. Ve a la pestaña **"Deployments"**
2. Verás el progreso del build
3. Tarda ~2-3 minutos
4. Cuando termine, verás **"Success"** ✅

---

## 🗄️ Paso 7: Inicializar Base de Datos

La base de datos PostgreSQL está vacía. Necesitas inicializarla:

### Opción A: Usando Railway CLI (Recomendado)

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ejecutar comando
railway run python init_db.py init
```

### Opción B: Localmente y luego subir datos

Esta opción es más avanzada - requiere configurar PostgreSQL localmente y migrar datos.

---

## ✅ Paso 8: Verificar Deployment

### 8.1. Verificación Automática

Usa el script de verificación:

```bash
python scripts/verify_deploy.py https://tu-app.railway.app
```

Deberías ver:
```
✅ Health Check: OK
✅ API Root: OK
✅ Swagger Docs: OK
✅ Login exitoso
✅ Endpoint protegido OK
```

### 8.2. Verificación Manual

1. **Accede a Swagger UI**:
   ```
   https://tu-app.railway.app/docs
   ```

2. **Test de Login**:
   - Expandir `POST /api/auth/login`
   - Click **"Try it out"**
   - Username: `admin@example.com`
   - Password: `admin123`
   - Click **"Execute"**
   - Deberías recibir un token JWT

3. **Autorizar Swagger**:
   - Click **"Authorize"** (candado arriba)
   - Pegar el token recibido
   - Click **"Authorize"**

4. **Probar Endpoints**:
   - `GET /api/empleados` - debe listar empleados
   - `GET /api/turnos/proximos-turnos` - debe listar turnos

---

## 🔄 Paso 9: Deploy Continuo

¡Ya está configurado! Ahora cada vez que hagas cambios:

```bash
git add .
git commit -m "descripción del cambio"
git push
```

Railway detectará automáticamente el push y redesplegará en ~1-2 minutos.

---

## 📊 Monitoreo

### Ver Logs en Vivo
1. En Railway Dashboard
2. Click tu servicio
3. Pestaña **"Logs"**
4. Verás todos los logs en tiempo real

### Métricas
Railway te muestra automáticamente:
- CPU usage
- Memory usage
- Network traffic
- Request counts

---

## 🔒 Seguridad Post-Deploy

### ⚠️ IMPORTANTE: Cambiar Contraseña Admin

El usuario admin tiene password por defecto. Debes cambiarlo:

1. Crear un script temporal o usar Swagger
2. Usar endpoint `/api/auth/cambiar-password`
3. Cambiar de `admin123` a algo seguro

---

## 🐛 Troubleshooting

### Error: "Application failed to respond"
- Revisar logs en Railway
- Verificar que `DATABASE_URL` existe
- Verificar que ejecutaste `init_db.py`

### Error: "SECRET_KEY" en logs
- Verificar que la variable `SECRET_KEY` está configurada
- Debe ser diferente a `dev-secret-key-change-in-production`

### CORS Error en el frontend
- Verificar que `ALLOWED_ORIGINS` tiene la URL correcta
- Debe incluir el protocolo `https://`
- Sin trailing slash al final

### Base de datos vacía
- Ejecutar `railway run python init_db.py init`
- O subir datos desde local (avanzado)

---

## 🔙 Rollback

Si algo falla:

1. En Railway → **"Deployments"**
2. Click en el deployment anterior que funcionaba
3. Click **"Redeploy"**
4. Railway volverá a esa versión

---

## 💰 Costos

**Plan Gratuito de Railway**:
- $5 de crédito gratis/mes
- Suficiente para desarrollo/pruebas
- ~500 horas de uptime/mes

**Si necesitas más**:
- Plan Developer: $5/mes (sin límite de uso)
- Solo pagas por lo que uses

---

## 📚 Recursos Adicionales

- 📖 [Documentación de Railway](https://docs.railway.app/)
- 🔧 [Railway CLI](https://docs.railway.app/develop/cli)
- 🐛 [Railway GitHub](https://github.com/railwayapp)

---

## ✅ Checklist Final

- [ ] Repositorio en GitHub creado y pusheado
- [ ] Proyecto en Railway creado
- [ ] PostgreSQL añadido
- [ ] Variables de entorno configuradas
- [ ] Deploy completado exitosamente
- [ ] `init_db.py` ejecutado
- [ ] Swagger UI accesible
- [ ] Login funciona
- [ ] Scripts de verificación pasan
- [ ] Contraseña admin cambiada

---

¡Listo! Tu API está en producción 🎉
