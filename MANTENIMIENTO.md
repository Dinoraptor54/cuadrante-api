# 🛠️ Guía de Mantenimiento y Solución de Problemas

Esta guía contiene instrucciones críticas para mantener el proyecto operativo a largo plazo, especialmente considerando limitaciones de servicios gratuitos.

## 🚨 Problema Común: "API no responde" o "Database Error"

Si la API en Render no responde o da errores de conexión a la base de datos después de unos días sin uso, la causa más probable es:

### **Supabase Pausó el Proyecto**

**Causa**: Los proyectos gratuitos de Supabase se **pausan automáticamente** después de 7 días de inactividad (sin conexiones).
**Síntoma**:
- El endpoint `/health` da timeout.
- Logs en Render muestran `FATAL: Tenant or user not found`.
- Comandos `curl` a Supabase dan `requested project not found`.

### ✅ Solución Rápida
1. Entra a [Supabase Dashboard](https://supabase.com/dashboard/projects).
2. Verás el proyecto en estado **"Paused"**.
3. Haz clic en **"Restore Project"** o el botón de reactivar.
4. Espera unos minutos hasta que el icono se ponga verde.
5. **Render reconectará automáticamente** (o puedes forzar un "Manual Deploy" para acelerarlo).

---

## 📅 Rutina de Mantenimiento (Para evitar pausas)

Para evitar que esto ocurra, se recomienda generar actividad en la base de datos al menos una vez por semana.

### Opción A: Uso Manual
Simplemente abre la aplicación web o la app de escritorio y haz login una vez a la semana.

### Opción B: Script de "Ping"
Puedes ejecutar este comando semanalmente para mantener la base de datos despierta:

```bash
# Ejecutar desde tu terminal local
curl https://cuadrante-api.onrender.com/health
```

---

## 📋 Credenciales Importantes

**Render**: [Dashboard](https://dashboard.render.com/)
**Supabase**: [Dashboard](https://supabase.com/dashboard/)

> **Nota**: Si alguna vez se elimina el proyecto de Supabase y creas uno nuevo, recuerda actualizar la `DATABASE_URL` en Render con el nuevo Password y Project ID.
