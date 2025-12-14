# Cómo Probar la Aplicación

Para probar la aplicación y las mejoras que he implementado, sigue estos pasos en tu terminal.

### 1. Instala las Dependencias

Asegúrate de que tienes todos los paquetes de Python necesarios. Ejecuta el siguiente comando en la carpeta `cuadrante_api`:

```bash
pip install -r requirements.txt
```

### 2. Inicia el Servidor

Una vez instaladas las dependencias, puedes iniciar el servidor de desarrollo. Este comando iniciará la API y la recargará automáticamente si haces cambios en el código.

```bash
uvicorn main:app --reload
```

### 3. Explora la API

Con el servidor en marcha, abre tu navegador web y visita la siguiente URL:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Ahí encontrarás la documentación interactiva (Swagger UI) que te permite probar cada uno de los *endpoints* de la API directamente desde el navegador.

### 4. Usuarios de Prueba

Para probar los endpoints que requieren autenticación (como solicitar permutas o ver tus próximos turnos), puedes usar los usuarios de prueba definidos en el fichero `INSTRUCCIONES_CONTINUACION.md`.

Por ejemplo, puedes usar el usuario coordinador para probar el endpoint de sincronización.
