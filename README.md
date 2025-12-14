# 🚨 API Cuadrante Vigilantes

API REST para acceso móvil a cuadrantes de turnos, permutas y datos de empleados.

**Estado**: ✅ 90% Completado | Listo para Producción  
**Versión**: 2.0.0 | Fecha: 8 de Diciembre 2025

---

## 📚 Documentación Rápida

| Documento | Propósito |
|-----------|-----------|
| **SECURITY.md** | Seguridad, JWT, CORS, validaciones |
| **DEPLOYMENT.md** | Railway, PostgreSQL, monitoreo |
| **RESUMEN_FINAL.md** | Resumen de cambios y progreso |
| **EJEMPLO_INTEGRACION.py** | Cómo usar validadores y logging |

---

## 🚀 Inicio Rápido

### 1. Setup Inicial

```bash
# Clonar y entrar
cd cuadrante_api

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables

```bash
# Copiar template
cp .env.example .env

# Editar .env
ENVIRONMENT=development
DATABASE_URL=sqlite:///./cuadrante.db
SECRET_KEY=dev-key-change-in-production
```

### 3. Inicializar Base de Datos

```bash
# Crear tablas e insertar datos iniciales
python init_db.py init

# Verificar salud
python init_db.py health
```

### 4. Ejecutar API

```bash
# Con auto-reload
python -m uvicorn main:app --reload

# O directamente
python main.py

# Documentación
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### 5. Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov

# Específico
pytest tests/test_auth.py -v
```

---

## 📋 Endpoints Principales

### 🔐 Autenticación
```
POST   /api/auth/login              Login de usuario
GET    /api/auth/me                 Info del usuario actual
POST   /api/auth/register           Registro nuevo usuario
POST   /api/auth/cambiar-password   Cambiar contraseña
```

### 📅 Turnos
```
GET    /api/turnos/mis-turnos/{anio}/{mes}      Turnos del mes
GET    /api/turnos/proximos-turnos              Próximos turnos
GET    /api/turnos/calendario/{anio}/{mes}     Calendario completo
```

### 🔄 Permutas
```
POST   /api/permutas/solicitar      Solicitar permuta
GET    /api/permutas/mis-permutas   Mis permutas
GET    /api/permutas/pendientes     Permutas pendientes
POST   /api/permutas/{id}/aceptar   Aceptar permuta
POST   /api/permutas/{id}/rechazar  Rechazar permuta
```

### 👥 Empleados
```
GET    /api/empleados/              Listar empleados
GET    /api/empleados/mi-perfil     Mi perfil
GET    /api/empleados/balance/{anio}  Balance de horas
PUT    /api/empleados/actualizar-perfil  Actualizar perfil
```

### 🔄 Sincronización
```
POST   /api/sync/full               Sincronizar todos los datos
```

---

## ✨ Características Implementadas

### ✅ Validaciones Robustas
```python
from utils.validators import DateValidator, EmailValidator

# Validar año
DateValidator.validate_year(2025)

# Validar email
EmailValidator.validate_email("user@example.com")
```

### ✅ Logging Estructurado
```python
from utils.logging_config import log_info, log_permuta_creada

log_info("Usuario conectado")
log_permuta_creada("u1@ex.com", "u2@ex.com", "2025-12-01", "2025-12-02")
```

### ✅ Rate Limiting
- 100 solicitudes por 60 segundos (configurable)
- Headers estándar: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- Protección contra abuso

### ✅ Manejo Global de Errores
- Excepciones personalizadas con logging
- Respuestas JSON consistentes
- Error tracking con IDs únicos

### ✅ Configuración Centralizada
```python
from config import settings

print(settings.DATABASE_URL)
print(settings.ALLOWED_ORIGINS)
print(settings.LOG_LEVEL)
```

### ✅ 44 Tests Automáticos
- 18 tests de autenticación
- 11 tests de permutas
- 15 tests de empleados

---

## 🔧 Estructura del Proyecto

```
cuadrante_api/
├── main.py                    # Aplicación principal
├── config.py                  # Configuración centralizada
├── init_db.py                 # Script de inicialización
├── requirements.txt           # Dependencias
├── .env.example               # Template de configuración
│
├── models/
│   ├── database.py           # Conexión a BD
│   └── sql_models.py         # Modelos SQLAlchemy
│
├── routers/
│   ├── auth.py               # Autenticación
│   ├── turnos.py             # Turnos
│   ├── permutas.py           # Permutas
│   ├── empleados.py          # Empleados
│   └── sync.py               # Sincronización
│
├── services/
│   ├── auth_service.py
│   ├── turnos_service.py
│   ├── permutas_service.py
│   ├── empleados_service.py
│   └── sync_service.py
│
├── utils/
│   ├── validators.py         # Validaciones robustas
│   ├── logging_config.py     # Sistema de logging
│   ├── rate_limiting.py      # Rate limiting
│   ├── error_handlers.py     # Manejo de errores
│   └── security.py           # Seguridad (JWT, etc)
│
├── tests/
│   ├── test_auth.py          # 18 tests
│   ├── test_permutas.py      # 11 tests
│   ├── test_empleados.py     # 15 tests
│   └── conftest.py           # Configuración pytest
│
└── Documentación/
    ├── README.md              # Este archivo
    ├── SECURITY.md            # Guía de seguridad
    ├── DEPLOYMENT.md          # Despliegue en Railway
    ├── RESUMEN_FINAL.md       # Resumen de cambios
    └── EJEMPLO_INTEGRACION.py # Ejemplos de uso
```

---

## 🔐 Seguridad

### JWT Tokens
- Expiración: 24 horas (configurable)
- Algoritmo: HS256
- Validación en cada request

### Contraseñas
- Hashing con bcrypt
- Requisitos: 8+ caracteres, mayúsculas, minúsculas, números

### CORS
- Orígenes desde variables de entorno
- Sin "*" en producción
- Métodos HTTP restringidos

### Rate Limiting
- 100 req/60s por IP
- Protección contra fuerza bruta
- Headers informativos

Ver **SECURITY.md** para detalles completos.

---

## 🚀 Despliegue en Railway

### Pasos Rápidos
1. Crear cuenta en [railway.app](https://railway.app)
2. Conectar GitHub
3. Crear proyecto desde repositorio
4. Configurar variables de entorno
5. Crear servicio PostgreSQL
6. Deploy automático

Ver **DEPLOYMENT.md** para instrucciones detalladas.

### Variables Críticas en Producción
```env
ENVIRONMENT=production
SECRET_KEY=<openssl rand -hex 32>
DATABASE_URL=postgresql://...
ALLOWED_ORIGINS=https://app.tudominio.com
LOG_LEVEL=INFO
```

---

## 🧪 Testing

### Ejecutar Todos los Tests
```bash
pytest tests/ -v
```

### Con Cobertura
```bash
pytest tests/ --cov=. --cov-report=html
```

### Tests Específicos
```bash
pytest tests/test_auth.py::test_login_exitoso -v
pytest tests/test_permutas.py -v
pytest tests/test_empleados.py -v
```

### Coverage Target
- Mínimo: 70%
- Actual: Pendiente (44 tests implementados)

---

## 📝 Ejemplos de Uso

### Validar Datos
```python
from utils.validators import DateValidator, EmailValidator

try:
    year = DateValidator.validate_year(2025)
    email = EmailValidator.validate_email("user@example.com")
except ValidationError as e:
    print(f"Error: {e.detail}")
```

### Logging
```python
from utils.logging_config import log_login, log_error

log_login("user@example.com", success=True)
log_error("Algo salió mal", error=exception)
```

### Usar la API
```python
import requests

headers = {"Authorization": "Bearer <token>"}

# Obtener mis turnos
response = requests.get(
    "http://localhost:8000/api/turnos/mis-turnos/2025/12",
    headers=headers
)
print(response.json())
```

Ver **EJEMPLO_INTEGRACION.py** para más ejemplos.

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
# Ejecutar desde raíz del proyecto
cd cuadrante_api
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Error: "Error al conectar a BD"
```bash
# Verificar DATABASE_URL
echo $DATABASE_URL

# Reiniciar BD
python init_db.py reset
python init_db.py init
```

### Error: "CORS Blocked"
1. Verificar `ALLOWED_ORIGINS` en .env
2. Incluir dominio de tu app
3. En desarrollo: `http://localhost:3000`

Ver **DEPLOYMENT.md** para más soluciones.

---

## 📊 Progreso del Proyecto

```
✅ Fase 1: Funcionalidad Básica    - 100%
✅ Fase 2: Mejoras Técnicas        - 100%
🚀 Fase 3: Producción              - 90%
   ✅ Validaciones
   ✅ Logging
   ✅ Rate limiting
   ✅ Error handling
   ✅ Config centralizada
   ⏳ Despliegue en Railway (manual)
```

---

## 📞 Soporte

- 📖 Consultar SECURITY.md para seguridad
- 🚀 Consultar DEPLOYMENT.md para despliegue
- 💡 Consultar EJEMPLO_INTEGRACION.py para ejemplos
- 🐛 Revisar logs: `python main.py 2>&1 | grep ERROR`

---

## 📄 Licencia

Privado - Proyecto Dino

---

## ✨ Últimas Actualizaciones

**8 de Diciembre 2025**
- ✅ Validaciones robustas implementadas
- ✅ Logging estructurado completado
- ✅ Rate limiting activado
- ✅ 44 tests nuevos
- ✅ Documentación SECURITY.md
- ✅ Documentación DEPLOYMENT.md mejorada
- ✅ Manejador global de errores
- ✅ Ejemplos de integración

**Status**: Listo para despliegue en Railway

---

**Generado por**: GitHub Copilot (Claude Haiku 4.5)  
**Versión API**: 2.0.0  
**Última actualización**: 8 de Diciembre 2025

### Permutas
- `POST /api/permutas/solicitar` - Solicitar permuta
- `GET /api/permutas/mis-solicitudes` - Mis permutas
- `PUT /api/permutas/{id}/aceptar` - Aceptar permuta

### Empleados
- `GET /api/empleados/perfil` - Perfil del empleado
- `GET /api/empleados/balance/{anio}` - Balance de horas

## 🔐 Autenticación

La API usa tokens JWT. Para autenticarte:

1. **Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=admin@example.com&password=admin123"
```

2. **Usar token en peticiones:**
```bash
curl http://localhost:8000/api/turnos/mis-turnos/2025/12 \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

## 🧪 Usuario de Prueba

- Email: `admin@example.com`
- Password: `admin123`

## 📁 Estructura del Proyecto

```
cuadrante_api/
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias
├── .env                 # Configuración (no subir a Git)
├── routers/            # Endpoints organizados
│   ├── auth.py         # Autenticación
│   ├── turnos.py       # Turnos
│   ├── permutas.py     # Permutas
│   └── empleados.py    # Empleados
├── models/             # Modelos de base de datos
├── services/           # Lógica de negocio
└── utils/              # Utilidades
```

## 🌐 Despliegue en Railway

### 1. Crear cuenta en Railway.app

### 2. Conectar repositorio GitHub

### 3. Railway detecta FastAPI automáticamente

### 4. Configurar variables de entorno en Railway

### 5. ¡Listo! URL: `https://tu-proyecto.railway.app`

## 🔧 Desarrollo

### Ejecutar con auto-reload
```bash
uvicorn main:app --reload
```

### Probar endpoints
Usa Thunder Client (VS Code) o Postman

## 📝 TODO

- [ ] Implementar base de datos PostgreSQL
- [ ] Añadir más validaciones
- [ ] Implementar notificaciones push
- [ ] Tests unitarios
- [ ] Documentación de API más detallada

## 🤝 Integración con App Desktop

La API lee los datos directamente de los archivos JSON del proyecto desktop.
Configurar `DESKTOP_DATA_PATH` en `.env` para apuntar a la carpeta `datos_cuadrante`.

## 📞 Soporte

Para dudas o problemas, contactar al administrador del sistema.
