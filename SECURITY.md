# 🔐 Guía de Seguridad - cuadrante_api

**Última actualización**: 2025-12-08  
**Versión**: 2.0.0

---

## 📋 Índice
1. [Autenticación y Autorización](#autenticación)
2. [Protección de Datos](#datos)
3. [Rate Limiting](#rate-limiting)
4. [CORS](#cors)
5. [Validaciones](#validaciones)
6. [Logging y Monitoreo](#logging)
7. [Deployment](#deployment)

---

## 🔐 Autenticación y Autorización {#autenticación}

### JWT (JSON Web Tokens)

La API usa JWT para autenticación stateless:

```python
# Generar token
token = create_access_token(
    data={"sub": "user@example.com"},
    expires_delta=timedelta(hours=24)
)

# Usar en requests
headers = {"Authorization": f"Bearer {token}"}
```

### Configuración Recomendada

```env
# .env
SECRET_KEY=<generar_clave_256_bits_segura>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Generar SECRET_KEY seguro:**
```bash
openssl rand -hex 32
```

### Mejores Prácticas

- ✅ Cambiar `SECRET_KEY` en producción
- ✅ Usar HTTPS para transmitir tokens
- ✅ Expiración de tokens: 24 horas (configurable)
- ✅ Refresh tokens para renovación segura
- ❌ Nunca hardcodear credenciales
- ❌ Nunca usar HTTP en producción

---

## 🛡️ Protección de Datos {#datos}

### Contraseñas

**Requisitos de Fortaleza:**
- Mínimo 8 caracteres
- Mayúsculas y minúsculas
- Al menos 1 número
- Implementado en: `utils/validators.py`

**Hashing:**
```python
# Usar bcrypt con salt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash(password)
```

### Datos en Base de Datos

- ✅ Contraseñas hasheadas (nunca en texto plano)
- ✅ Datos sensibles encriptados en reposo (recomendado)
- ✅ Conexiones SSL/TLS a BD

### Datos en Tránsito

- ✅ HTTPS obligatorio en producción
- ✅ TLS 1.2+ mínimo
- ✅ Certificados válidos

---

## ⏱️ Rate Limiting {#rate-limiting}

Protege contra:
- Ataques de fuerza bruta
- DoS (Denegación de Servicio)
- Abuso de API

### Configuración Actual

```python
# En main.py
from utils.rate_limiting import RateLimitMiddleware

app.add_middleware(
    RateLimitMiddleware,
    max_requests=100,
    window_seconds=60
)
```

**Límites predeterminados:**
- 100 solicitudes por 60 segundos (por IP)
- Headers de respuesta:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

### Respuesta de Límite Excedido

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/json

{
  "detail": "Demasiadas solicitudes. Intenta de nuevo más tarde."
}
```

### Para Producción

Usar **Redis** para rate limiting distribuido:

```python
# pip install redis
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)
```

---

## 🌐 CORS {#cors}

### Configuración Actual

```python
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Configuración para Producción

```env
# .env.production
ALLOWED_ORIGINS=https://app.tudominio.com,https://tudominio.com
```

### Valores Recomendados

```python
# Restringir métodos
allow_methods=["GET", "POST", "PUT", "DELETE"]  # No "*"

# Restringir headers
allow_headers=["Content-Type", "Authorization"]  # Específicos

# Controlar credenciales
allow_credentials=True  # Solo si es necesario
```

---

## ✅ Validaciones {#validaciones}

Módulo: `utils/validators.py`

### Validadores Disponibles

#### Fechas
```python
from utils.validators import DateValidator

DateValidator.validate_year(2025)
DateValidator.validate_month(12)
DateValidator.validate_day(25, 12, 2025)
DateValidator.validate_date_string("2025-12-25")
DateValidator.validate_date_in_past(date.today())
```

#### Emails
```python
from utils.validators import EmailValidator

EmailValidator.validate_email("user@example.com")
EmailValidator.validate_email_not_empty(email_str)
```

#### Turnos
```python
from utils.validators import TurnoValidator

TurnoValidator.validate_turno_code("M")  # M, T, N, D, F, V, B, L
TurnoValidator.validate_horario("08:00-16:00")
```

#### Contraseñas
```python
from utils.validators import PasswordValidator

PasswordValidator.validate_password_strength("SecurePass123")
```

#### Paginación
```python
from utils.validators import PaginationValidator

skip, limit = PaginationValidator.validate_pagination(
    skip=0, limit=50
)
```

### Uso en Endpoints

```python
from fastapi import APIRouter
from utils.validators import DateValidator, ValidationError

@router.get("/balance/{anio}")
async def get_balance(anio: int):
    try:
        validated_year = DateValidator.validate_year(anio)
        # Lógica aquí
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
```

---

## 📝 Logging y Monitoreo {#logging}

Módulo: `utils/logging_config.py`

### Niveles de Log

- **DEBUG**: Información detallada para diagnóstico
- **INFO**: Eventos normales (logins, cambios)
- **WARNING**: Situaciones inusuales
- **ERROR**: Errores que necesitan atención
- **CRITICAL**: Errores graves

### Uso

```python
from utils.logging_config import (
    log_info, log_error, log_warning,
    log_login, log_permuta_creada,
    log_error_bd, log_acceso_recurso
)

# Uso simple
log_info("Usuario conectado")
log_error("Error en BD", error=exception)

# Logs específicos de negocio
log_login("user@example.com", success=True)
log_permuta_creada("user1@ex.com", "user2@ex.com", "2025-12-01", "2025-12-02")
log_acceso_recurso("user@ex.com", "/api/turnos", "GET", True)
```

### Configuración en main.py

```python
from utils.logging_config import AppLogger

AppLogger.initialize(
    log_dir="logs",
    log_level="INFO",
    environment="production"
)
```

### Archivos de Log

- **Desarrollo**: Consola
- **Producción**: `logs/cuadrante_api_YYYYMMDD.log`
- **Rotación**: 10MB máximo, 10 backups

---

## 🚀 Deployment {#deployment}

### Checklist de Seguridad

- [ ] SECRET_KEY: Generada y única
- [ ] DATABASE_URL: PostgreSQL en producción
- [ ] ALLOWED_ORIGINS: Dominios específicos
- [ ] ENVIRONMENT=production
- [ ] LOG_LEVEL=WARNING
- [ ] HTTPS: Certificado SSL/TLS válido
- [ ] Rate limiting: Habilitado con Redis (opcional)
- [ ] CORS: Restringido
- [ ] Validaciones: Activas en todos los endpoints

### Variables de Entorno Críticas

```bash
# Generar
SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Base de datos (PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/cuadrante

# Seguridad
ENVIRONMENT=production
ALLOWED_ORIGINS=https://app.tudominio.com
LOG_LEVEL=INFO

# API
API_PORT=8000
API_HOST=0.0.0.0
```

### En Railway

1. **Variables de Entorno** → Añadir `SECRET_KEY`, `DATABASE_URL`, etc.
2. **Dominio** → Configurar HTTPS automático
3. **Health Check** → `GET /health`
4. **Logs** → Monitorizar en tiempo real

---

## 🔍 Auditoría y Monitoreo

### Eventos a Auditar

- ✅ Logins/Logouts
- ✅ Cambios de permutas
- ✅ Sincronización de datos
- ✅ Errores de BD
- ✅ Accesos denegados

### Integración con Herramientas

**Sentry** (para errores):
```bash
pip install sentry-sdk
```

**DataDog** (para monitoreo):
```bash
pip install datadog
```

---

## 📚 Referencias

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)

---

## ⚠️ Incidentes de Seguridad

Si descubres una vulnerabilidad:

1. **NO** la publiques públicamente
2. Contacta a: `admin@example.com`
3. Proporciona detalles del problema
4. Dale tiempo para parchear (7-30 días)

---

**Estado**: Revisado y actualizado  
**Siguiente revisión**: Cada 30 días
