# 📝 CHANGELOG - Cuadrante API

Todas las modificaciones notables del proyecto se documentan aquí.

## [v1.3.0] - 2026-01-22

### ✨ Añadido
- **Vista multi-empleado para coordinadores**: Nuevo endpoint `/api/schedule/{year}/{month}/empleado/{empleado_id}` permite ver turnos de cualquier empleado
- **Selector de empleados mejorado**: Nombre del empleado actual se muestra prominente en azul entre botones de navegación

### 🐛 Corregido
- **Bug crítico de renderizado**: Frontend esperaba `scheduleData.cuadrante[employeeName]` pero API devuelve `scheduleData.shifts`
- **URLs de API incorrectas**: Cambiado `/schedule/` a `/api/schedule/` en frontend
- **Host de base de datos**: Actualizado de `aws-0` a `aws-1-eu-central-1.pooler.supabase.com`
- **Aplicación de escritorio**: Reconstruido ejecutable con URL correcta de Render

### 🔧 Mantenimiento
- Creado `MANTENIMIENTO.md` con guía para reactivar proyecto pausado en Supabase
- Documentación de troubleshooting para error "Tenant or user not found"

---

## [v1.2.0] - 2026-01-11 (Sesión anterior)

### ✨ Añadido
- Despliegue inicial en Render
- Integración con Supabase PostgreSQL
- Sistema de sincronización desde app de escritorio

### 🐛 Corregido
- Error tipográfico en `DATABASE_URL` (`subabase.com` → `supabase.com`)

---

## [v1.1.0] - Fecha anterior

### ✨ Añadido
- API REST con FastAPI
- Autenticación JWT
- Endpoints de empleados, turnos, permutas, vacaciones
- Frontend PWA con login y visualización de cuadrantes

---

## [v1.0.0] - Fecha inicial

### ✨ Añadido
- Versión inicial del proyecto
- Aplicación de escritorio con Tkinter
- Gestión local de cuadrantes con SQLite

---

## Formato

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)

### Tipos de cambios
- **✨ Añadido** - Nuevas funcionalidades
- **🔄 Cambiado** - Cambios en funcionalidad existente
- **❌ Deprecado** - Funcionalidades que se eliminarán pronto
- **🗑️ Eliminado** - Funcionalidades eliminadas
- **🐛 Corregido** - Corrección de bugs
- **🔒 Seguridad** - Correcciones de vulnerabilidades
- **🔧 Mantenimiento** - Cambios internos, refactoring, documentación
