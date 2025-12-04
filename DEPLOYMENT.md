# Pasos para desplegar en Railway

## 1. Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `cuadrante-api`
3. Descripción: "API REST para gestión de cuadrantes de vigilantes"
4. Público o Privado (tu elección)
5. **NO** marcar "Initialize with README" (ya lo tenemos)
6. Click en "Create repository"

## 2. Conectar repositorio local con GitHub

Copia y pega estos comandos en tu terminal (reemplaza `TU-USUARIO` con tu usuario de GitHub):

```bash
cd "c:\mis proyectos dino\cuadrante_api"
git remote add origin https://github.com/TU-USUARIO/cuadrante-api.git
git branch -M main
git push -u origin main
```

## 3. Desplegar en Railway

### Opción A: Desde Railway Dashboard
1. Ve a https://railway.app
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway a acceder a tu GitHub
5. Selecciona el repositorio `cuadrante-api`
6. Railway detectará automáticamente que es FastAPI
7. Configura las variables de entorno:
   - `SECRET_KEY`: (genera una clave segura)
   - `DATABASE_URL`: `sqlite:///./cuadrante.db`
8. Click en "Deploy"

### Opción B: Desde CLI de Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Iniciar proyecto
cd "c:\mis proyectos dino\cuadrante_api"
railway init

# Desplegar
railway up
```

## 4. Configurar dominio

1. En Railway dashboard, ve a tu proyecto
2. Click en "Settings" → "Domains"
3. Click en "Generate Domain"
4. Tu API estará disponible en: `https://tu-proyecto.railway.app`

## 5. Verificar despliegue

Visita:
- `https://tu-proyecto.railway.app/` - Debe mostrar info de la API
- `https://tu-proyecto.railway.app/docs` - Documentación Swagger
- `https://tu-proyecto.railway.app/health` - Health check

## 6. Actualizar código en el futuro

```bash
cd "c:\mis proyectos dino\cuadrante_api"
git add .
git commit -m "Descripción de cambios"
git push
```

Railway redespliegará automáticamente.

## Notas importantes

- ⚠️ La base de datos SQLite se reiniciará en cada despliegue
- 💡 Para producción, considera usar PostgreSQL
- 🔐 Cambia el `SECRET_KEY` en las variables de entorno de Railway
- 📝 Los logs estarán disponibles en Railway dashboard
