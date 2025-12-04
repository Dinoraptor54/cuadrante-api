# API Cuadrante Vigilantes

API REST para acceso móvil a cuadrantes de turnos, permutas y datos de empleados.

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
cd cuadrante_api
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env y configurar:
# - SECRET_KEY (generar una clave segura)
# - DESKTOP_DATA_PATH (ruta a datos_cuadrante)
```

### 3. Ejecutar Servidor de Desarrollo

```bash
python main.py
```

La API estará disponible en: `http://localhost:8000`

### 4. Documentación Interactiva

Abre en tu navegador:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📋 Endpoints Principales

### Autenticación
- `POST /api/auth/login` - Login de usuario
- `GET /api/auth/me` - Info del usuario actual

### Turnos
- `GET /api/turnos/mis-turnos/{anio}/{mes}` - Turnos del mes
- `GET /api/turnos/calendario/{anio}/{mes}` - Calendario completo (coordinador)

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
