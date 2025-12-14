# 🚀 DEPLOYMENT.md - Guía de Despliegue

**Última actualización**: 8 de Diciembre 2025  
**Versión**: 2.0

---

## 📋 Tabla de Contenidos

1. [Prerequisitos](#prerequisitos)
2. [Desarrollo Local](#desarrollo)
3. [Despliegue en Railway](#railway)
4. [Base de Datos PostgreSQL](#postgresql)
5. [Troubleshooting](#troubleshooting)
6. [Monitoreo](#monitoreo)

---

## 📦 Prerequisitos {#prerequisitos}

### Local
- Python 3.9+
- pip o poetry
- Git

### Production (Railway)
- Cuenta en [Railway](https://railway.app)
- GitHub conectado
- Tarjeta de crédito (para recursos)

---

## 💻 Desarrollo Local {#desarrollo}

### 1. Setup Inicial

```bash
# Clonar proyecto
git clone <tu-repo>
cd cuadrante_api

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar .env

```bash
# Copiar template
cp .env.example .env

# Editar .env (valores de desarrollo)
ENVIRONMENT=development
DATABASE_URL=sqlite:///./cuadrante.db
SECRET_KEY=dev-key-change-in-production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
LOG_LEVEL=DEBUG
```

### 3. Inicializar Base de Datos

```bash
# Crear tablas e insertar datos iniciales
python init_db.py init

# O resetear BD (desarrollo solo)
python init_db.py reset

# Verificar salud
python init_db.py health
```

### 4. Ejecutar API

```bash
# Desarrollo con auto-reload
python -m uvicorn main:app --reload --port 8000

# O directamente
python main.py

# Documentación: http://localhost:8000/docs
```

### 5. Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=. --cov-report=html

# Test específico
pytest tests/test_auth.py::test_login_exitoso -v
```

---

## 🚀 Despliegue en Railway {#railway}

### Paso 1: Preparar Repositorio GitHub

```bash
# Si no está en git
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/cuadrante-api.git
git push -u origin main
```

### Paso 2: Crear Proyecto en Railway

1. Ir a [railway.app](https://railway.app)
2. Click en "New Project"
3. Seleccionar "GitHub Repo"
4. Conectar cuenta GitHub si es necesario
5. Seleccionar `cuadrante-api`
6. Click "Deploy"

### Paso 3: Configurar Variables de Entorno

En Railway dashboard → Project → Settings → Variables:

```env
ENVIRONMENT=production
DEBUG=false

# Base de datos (Railway genera automáticamente)
# DATABASE_URL se crea al añadir PostgreSQL

# Seguridad
SECRET_KEY=<openssl rand -hex 32>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS (cambiar a tu dominio)
ALLOWED_ORIGINS=https://app.tudominio.com,https://tudominio.com

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs

# API
API_PORT=8000
API_HOST=0.0.0.0

# Desktop
DESKTOP_DATA_PATH=../../proyecto_modulo_cuadrante/datos_cuadrante
```

### Paso 4: Añadir Base de Datos PostgreSQL

En Railway:
1. Click "Add Service" → "PostgreSQL"
2. Railway crea automáticamente `DATABASE_URL`
3. Variable disponible para uso en app

### Paso 5: Inicializar Base de Datos

En Railway Terminal:
```bash
python init_db.py init
```

---

## 🗄️ Base de Datos PostgreSQL {#postgresql}

### Conexión String

```
postgresql://username:password@host:port/database
```

### Verificar Conexión

```bash
# En Railway Terminal
python init_db.py health

# Output:
# ✅ BD saludable
#    Empleados en BD: 1
#    Usuarios en BD: 1
```

### Migrar desde SQLite

```bash
# Exportar datos de SQLite local
python -c "
from models.sql_models import Empleado
from models.database import SessionLocal
db = SessionLocal()
for emp in db.query(Empleado).all():
    print(f'{emp.email},{emp.nombre}')
"

# Importar a PostgreSQL en Railway
python init_db.py reset
python init_db.py init
```

---

## 🔧 Troubleshooting {#troubleshooting}

### Error: "ModuleNotFoundError"

```bash
# Ejecutar desde raíz
cd cuadrante_api
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python main.py
```

### Error: "Error al conectar a BD"

```bash
# Verificar DATABASE_URL
echo $DATABASE_URL

# Probar conexión
python -c "from models.database import SessionLocal; SessionLocal()"

# Reset
python init_db.py reset
```

### Error: "CORS Blocked"

1. Verificar `ALLOWED_ORIGINS` en .env
2. En desarrollo: incluir `http://localhost:3000`
3. En producción: dominios específicos (no *)

### Error: "Invalid SECRET_KEY"

```bash
# Generar nueva
openssl rand -hex 32

# Actualizar en Railway
# Settings → Variables → SECRET_KEY
```

---

## 📊 Monitoreo {#monitoreo}

### Health Check

```bash
# Local
curl http://localhost:8000/health

# Production
curl https://tu-api.railway.app/health
```

### Logs en Railway

Dashboard → Deployments → [Tu Deployment] → Logs

### Métricas

- CPU usage
- Memory
- Network traffic
- Requests/sec

---

## 📋 Pre-Deployment Checklist

- [ ] `SECRET_KEY` generada y única
- [ ] `DATABASE_URL` apunta a PostgreSQL
- [ ] `ENVIRONMENT=production`
- [ ] `ALLOWED_ORIGINS` sin "*"
- [ ] `LOG_LEVEL=INFO`
- [ ] HTTPS habilitado
- [ ] Tests pasan (pytest tests/ -v)
- [ ] Contraseña admin cambiada
- [ ] BD inicializada (init_db.py init)

---

## 🔗 URLs

### Local
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Production
- API: https://cuadrante-api.railway.app
- Docs: https://cuadrante-api.railway.app/docs

---

**Status**: ✅ Production Ready

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
