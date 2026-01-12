# 🚨 API Cuadrante Vigilantes

API REST para acceso móvil a cuadrantes de turnos, permutas, vacaciones y datos de empleados.

**Estado**: ✅ 95% Completado | Listo para Producción
**Versión**: 2.5.0 | Fecha: 5 de Enero 2026

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

# Editar .env con tus datos (SMTP es opcional)
ENVIRONMENT=development
DATABASE_URL=sqlite:///./cuadrante.db
SECRET_KEY=dev-key-change-in-production
# SMTP_HOST=smtp.example.com
# SMTP_USER=user@example.com
# SMTP_PASSWORD=secret
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

# Documentación
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### 5. Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v
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

### 🏖️ Vacaciones (NUEVO)
```
POST   /api/vacaciones/solicitar      Solicitar vacaciones
GET    /api/vacaciones/mis-solicitudes  Ver mis solicitudes
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

### ✅ Notificaciones por Email (NUEVO)
- Envío de emails para eventos (solicitud de permuta, vacaciones).
- Modo de simulación: si no se configura SMTP, las notificaciones se muestran en el log.

### ✅ Frontend Integrado (PWA) (NUEVO)
- La API sirve una aplicación web desde el directorio `/static`.
- Permite un despliegue unificado de frontend y backend.

### ✅ Validaciones Robustas
- Clases dedicadas para validar fechas, emails, turnos, etc.
- Excepciones personalizadas para errores de validación.

### ✅ Logging Estructurado
- Sistema de logging centralizado con niveles y rotación de archivos.
- Funciones específicas para eventos de negocio.

### ✅ Rate Limiting
- Middleware para limitar el número de solicitudes por IP.
- Protección contra ataques de fuerza bruta.

### ✅ Manejo Global de Errores
- Captura centralizada de excepciones para respuestas de error consistentes.

### ✅ Configuración Centralizada
- Uso de `pydantic-settings` para gestionar la configuración desde `.env`.

### ✅ 44+ Tests Automáticos
- Cobertura para autenticación, permutas, empleados y más.

---

## 🔧 Estructura del Proyecto

```
cuadrante_api/
├── main.py                    # Aplicación principal y servidor de PWA
├── config.py                  # Configuración centralizada
├── requirements.txt           # Dependencias
├── .env.example               # Template de configuración
│
├── static/                    # Frontend (PWA)
│   ├── index.html
│   └── ...
│
├── models/
│   ├── database.py           # Conexión a BD (get_db)
│   └── sql_models.py         # Modelos SQLAlchemy
│
├── routers/
│   ├── auth.py               # Autenticación
│   ├── turnos.py             # Turnos
│   ├── permutas.py           # Permutas
│   ├── empleados.py          # Empleados
│   ├── vacaciones.py         # (NUEVO) Gestión de vacaciones
│   └── sync.py               # Sincronización
│
├── services/
│   ├── auth_service.py
│   ├── turnos_service.py
│   ├── permutas_service.py
│   ├── empleados_service.py
│   ├── vacaciones_service.py   # (NUEVO) Lógica de vacaciones
│   ├── notification_service.py # (NUEVO) Envío de emails
│   └── sync_service.py
│
├── utils/
│   ├── validators.py         # Validaciones
│   ├── logging_config.py     # Logging
│   ├── rate_limiting.py      # Rate limiting
│   ├── error_handlers.py     # Manejo de errores
│   └── security.py           # Seguridad (JWT, etc)
│
└── tests/
    ├── test_auth.py
    ├── test_permutas.py
    ├── test_empleados.py
    └── conftest.py
```

---

## 🔐 Seguridad

Ver **SECURITY.md** para detalles completos sobre JWT, hashing de contraseñas, CORS y más.

---

## 🚀 Despliegue en Railway

Ver **DEPLOYMENT.md** para instrucciones detalladas sobre el despliegue y la configuración de PostgreSQL.

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ver cobertura de tests
pytest tests/ --cov=. --cov-report=html
```

---

## 📄 Licencia

Privado - Proyecto Dino

---

## ✨ Últimas Actualizaciones

**5 de Enero 2026**
- ✅ **Módulo de Vacaciones**: Añadida funcionalidad para solicitar y ver vacaciones.
- ✅ **Servicio de Notificaciones**: Implementado sistema de notificaciones por email para eventos clave.
- ✅ **Frontend Integrado**: La API ahora sirve una PWA desde el directorio `static`.
- ✅ **Manejo de Errores Global**: Añadido un sistema centralizado para gestionar excepciones.
- ✅ **Health Check**: Incluido endpoint `/health` para monitoreo en producción.
- ✅ **Soporte para PostgreSQL**: Añadida dependencia `psycopg2-binary` para producción.

**8 de Diciembre 2025**
- ✅ Validaciones robustas implementadas
- ✅ Logging estructurado completado
- ✅ Rate limiting activado
- ✅ 44 tests iniciales creados

**Status**: Migración a PostgreSQL y nuevas funcionalidades completadas. Listo para despliegue final.