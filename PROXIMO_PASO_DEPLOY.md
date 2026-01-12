# 🚀 GUÍA RÁPIDA: Deploy en Railway

## ✅ Preparación Completada

Todos los archivos están listos para desplegar en Railway:

- ✅ Configuración de seguridad
- ✅ Scripts de verificación
- ✅ Documentación completa
- ✅ Commit realizado

---

## 📝 SECRET_KEYS Generadas

Usa UNA de estas claves en Railway (Variables → SECRET_KEY):

```
1. 5e6XamTd6xq+o1tyXfTTG0QAb0dNa3FYF7pfwXolomE=
2. jRte9QxYKw97xKPsR+QKtf7lCsViEIc8nas2j7fC7co=
3. De4kZw5fFSOvwE9g86oD57FQBpCa43aC9gmuxKU88Rs=
```

⚠️ **Importante**: Guarda la que elijas - la necesitarás en el Paso 5.

---

## 🎯 Próximos Pasos (Manual)

### 1. Crear Repositorio en GitHub
```
1. Ve a https://github.com/new
2. Nombre: cuadrante-api
3. Público o Privado
4. NO marcar "Initialize with README"
5. Click "Create repository"
```

### 2. Conectar y Subir
```bash
# En el directorio cuadrante_api
git remote add origin https://github.com/TU_USUARIO/cuadrante-api.git
git push -u origin master
```

### 3. Configurar Railway
```
1. https://railway.app/ → Login con GitHub
2. "Start a New Project" → "Deploy from GitHub repo"
3. Seleccionar cuadrante-api
4. Añadir "+ New" → "Database" → "PostgreSQL"
```

### 4. Añadir Variables de Entorno
En Railway → Settings → Variables:
```
ENVIRONMENT=production
SECRET_KEY=[una de las claves de arriba]
ALLOWED_ORIGINS=https://tu-app.railway.app
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
LOG_LEVEL=INFO
```

### 5. Inicializar Base de Datos
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Conectar y ejecutar
railway login
railway link
railway run python init_db.py init
```

### 6. Verificar
```bash
python scripts/verify_deploy.py https://tu-app.railway.app
```

---

## 📚 Documentación Completa

Para guía detallada paso a paso, ver:
- **`RAILWAY_SETUP.md`** - Guía completa con screenshots y troubleshooting
- **`implementation_plan.md`** - Plan técnico de implementación

---

## 🔍 Verificación

Después del deploy, verificar:
- ✅ `https://tu-app.railway.app/health` → `{"status":"healthy"}`
- ✅ `https://tu-app.railway.app/docs` → Swagger UI
- ✅ Login con `admin@example.com` / `admin123`
- ✅ Cambiar contraseña de admin

---

## 💡 Deploy Continuo

Después del setup inicial, cada cambio se despliega automáticamente:
```bash
git add .
git commit -m "tu mensaje"
git push
```
Railway redespliega en ~1-2 minutos.

---

## 📊 Estado del Proyecto

**Archivos Preparados**: 74 archivos
**Tests**: 44 tests (todos pasan)
**Datos Reales**: 1,526 turnos de 7 empleados
**Listo para Producción**: ✅ SÍ

---

¿Necesitas ayuda? Revisa `RAILWAY_SETUP.md` para solución de problemas.
