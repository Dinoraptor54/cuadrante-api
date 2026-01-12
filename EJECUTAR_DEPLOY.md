# 🚀 COMANDOS PARA DESPLEGAR AHORA

Ya tienes cuentas en GitHub y Railway. Sigue estos pasos en orden:

---

## PASO 1: Crear Repositorio en GitHub 

### Opción A: Por navegador (Recomendado - Más fácil)
1. Abre: https://github.com/new
2. Repository name: **cuadrante-api**
3. Description: API REST para gestión de turnos de vigilantes
4. **Importante**: NO marcar "Add a README file" 
5. Click **"Create repository"**
6. GitHub te mostrará la URL del repo (guárdala)

### Opción B: Por línea de comandos (si tienes GitHub CLI)
```bash
gh repo create cuadrante-api --public --source=. --remote=origin
```

---

## PASO 2: Conectar y Subir a GitHub

**Después de crear el repo**, ejecuta estos comandos en la terminal:

```bash
# Ve al directorio del proyecto
cd "c:\mis proyectos dino\cuadrante_api"

# Añade el repositorio remoto (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/cuadrante-api.git

# Verifica que se añadió correctamente
git remote -v

# Sube el código a GitHub
git push -u origin master
```

**Espera** a que termine de subir (~30 segundos - 1 minuto).

---

## PASO 3: Configurar Railway

### 3.1. Crear Proyecto
1. Ve a: https://railway.app/
2. Click **"Login"** → Inicia sesión con GitHub
3. Click **"Start a New Project"**
4. Selecciona **"Deploy from GitHub repo"**
5. Si es la primera vez, autoriza a Railway
6. Busca y selecciona: **cuadrante-api**
7. Click **"Deploy Now"**

Railway empezará a construir la app automáticamente.

### 3.2. Añadir PostgreSQL
1. En tu proyecto Railway, click **"+ New"**
2. Click **"Database"**
3. Selecciona **"Add PostgreSQL"**
4. Railway lo creará automáticamente
   - Creará la variable `DATABASE_URL` automáticamente
   - La conectará con tu app

### 3.3. Configurar Variables de Entorno
1. Click en tu servicio (el que tiene tu código)
2. Ve a la pestaña **"Variables"**
3. Click **"+ Add Variable"** y añade estas (una por una):

```
ENVIRONMENT=production
SECRET_KEY=5e6XamTd6xq+o1tyXfTTG0QAb0dNa3FYF7pfwXolomE=
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
LOG_LEVEL=INFO
```

4. **IMPORTANTE**: Después de añadir las variables, necesitas añadir `ALLOWED_ORIGINS`:
   - Railway te muestra la URL de tu app arriba (algo como: `https://cuadrante-api-production-XXXX.up.railway.app`)
   - Añade una nueva variable:
     ```
     ALLOWED_ORIGINS=https://cuadrante-api-production-XXXX.up.railway.app
     ```
     (reemplaza con TU URL exacta)

5. Click **"Deploy"** si no se redesplega automáticamente

**Espera** ~2-3 minutos mientras Railway despliega.

---

## PASO 4: Inicializar Base de Datos

La BD PostgreSQL está vacía. Necesitas crear las tablas.

### Opción A: Usando Railway CLI (Recomendado)

```bash
# Instalar Railway CLI (solo una vez)
npm install -g @railway/cli

# O si no tienes npm, descarga desde: https://docs.railway.app/develop/cli#installation

# Login en Railway
railway login

# Conectar al proyecto
railway link

# Ejecutar init_db
railway run python init_db.py init
```

### Opción B: Usando Railway Dashboard (si la CLI no funciona)
1. En Railway → Tu servicio → Settings
2. Scroll a "Deploy Settings"
3. Add command: `python init_db.py init`
4. Deploy (solo esta vez)
5. Luego remueve el comando para que no se ejecute en cada deploy

---

## PASO 5: Verificar que Funciona

### Verificación Rápida (navegador)
1. Ve a: `https://tu-app.railway.app/health`
   - Debes ver: `{"status":"healthy"}`
2. Ve a: `https://tu-app.railway.app/docs`
   - Debes ver la interfaz Swagger

### Verificación Completa (script)
```bash
# En tu terminal local
python scripts/verify_deploy.py https://tu-app.railway.app
```

Deberías ver todos los checks en verde ✅

---

## PASO 6: Probar Login

En Swagger UI (`https://tu-app.railway.app/docs`):

1. Expandir **POST /api/auth/login**
2. Click **"Try it out"**
3. Llenar:
   - username: `admin@example.com`
   - password: `admin123`
4. Click **"Execute"**
5. Deberías recibir un token JWT

---

## ⚠️ IMPORTANTE - Después del Deploy

### Cambiar Contraseña de Admin
El password `admin123` es temporal. Debes cambiarlo:

1. En Swagger, autorízate con el token de admin
2. Usa el endpoint `POST /api/auth/cambiar-password`
3. Cambia a una contraseña segura

---

## 🎉 ¡Listo!

Tu API está en producción. Ahora cada vez que hagas cambios:

```bash
git add .
git commit -m "descripción del cambio"
git push
```

Railway redesplegará automáticamente en ~1-2 minutos.

---

## 🐛 Si Algo Falla

### Error: "Application failed to respond"
- Revisa logs en Railway: Dashboard → Logs
- Verifica que ejecutaste `init_db.py`

### Error: CORS
- Verifica que `ALLOWED_ORIGINS` tiene la URL correcta de Railway
- Debe incluir `https://` y NO terminar en `/`

### Base de datos vacía
- Ejecuta: `railway run python init_db.py init`

---

## 📞 Necesitas Ayuda?

Si un paso falla, dime en qué paso estás y qué error ves.
