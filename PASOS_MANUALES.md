# 🚀 Pasos Finales para Desplegar en Railway

Hemos avanzado el 90% del proceso automáticamente. Debido a la seguridad de la interfaz de Railway, necesito que completes manualmente estos 2 pasos críticos:

## Paso 1: Configurar Variables de Entorno (2 min)

1. Ve a tu proyecto en Railway: **https://railway.app/dashboard**
2. Abre el servicio **"Postgres"** -> Pestaña **"Variables"**.
3. Copia el VALOR de **`DATABASE_URL`** (la interna está bien, empieza por `postgresql://...`).
4. Ve al servicio **"web"** (la API) -> Pestaña **"Variables"**.
5. Añade/Actualiza las siguientes variables:

| Variable | Valor |
|----------|-------|
| `DATABASE_URL` | **[PEGA AQUÍ LO QUE COPIASTE DEL PASO 3]** |
| `ENVIRONMENT` | `production` |
| `SECRET_KEY` | `5e6XamTd6xq+o1tyXfTTG0QAb0dNa3FYF7pfwXolomE=` |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_EXPIRATION_HOURS` | `24` |
| `LOG_LEVEL` | `INFO` |
| `ALLOWED_ORIGINS` | `*` |

*Al guardar, Railway redesplegará automáticamente tu API.* ✅

---

## Paso 2: Inicializar la Base de Datos (3 min)

Para crear las tablas y el usuario admin, ejecutaremos el script desde tu PC conectando a la BD remota.

1. En Railway -> Servicio **"Postgres"** -> Pestaña **"Variables"**.
2. Copia el valor de **`DATABASE_PUBLIC_URL`**.
   *(Si no existe, ve a "Settings" -> "Public Networking" en el servicio Postgres y actívalo).*
3. En tu terminal (PowerShell), ejecuta:

```powershell
# Reemplaza [TU_URL_PUBLICA] con lo que copiaste
$env:DATABASE_URL="[TU_URL_PUBLICA]"

# Ejecutar inicialización
python init_db.py init
```

Deberías ver:
```
✅ Conexión exitosa a la BD
🔨 Creando tablas...
✅ Tablas creadas exitosamente
👤 Creando usuario administrador inicial...
✅ Usuario admin creado: admin@example.com / admin123
```

---

## Paso 3: Verificar (Final)

Abre la URL de tu API (la puedes ver en el servicio "web" -> Settings -> Public Networking) y prueba:
- Ir a `/health` -> Debe decir `{"status": "healthy"}`
- Ir a `/docs` -> Prueba hacer login con `admin@example.com` / `admin123`

---

**¡Dame luz verde cuando hayas completado estos pasos o si tienes alguna duda!** 🚦
