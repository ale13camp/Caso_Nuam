# Mantenedor tributario NUAM DJ 1948

Proyecto Integrado TIHV43 · INACAP · Clase 10, Unidad 3 · Paralelo A.

Base funcional con Django, PostgreSQL y conexión preparada a MongoDB Atlas. Incluye login, grupos, navegación protegida, datos ficticios de dos corredores y consulta mínima para probar aislamiento. El cálculo, la edición, el importador y la consulta del historial corresponden a las próximas clases.

## Instalación en Windows

Requiere Python 3.12 o superior y PostgreSQL 16 o superior, local o en nube. Desde PowerShell, en la carpeta del repositorio:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia la clave generada a `SECRET_KEY` en `.env`. Completa `DATABASE_URL` con la conexión de PostgreSQL. Las credenciales se mantienen en ese archivo ignorado por Git. En nube usa la cadena del proveedor con `?sslmode=require`; no desactives la validación TLS en Atlas.

```dotenv
DATABASE_URL=postgresql://USUARIO:CONTRASENA@HOST:5432/BASE?sslmode=require
MONGODB_URI=mongodb+srv://USUARIO:CONTRASENA@CLUSTER/?retryWrites=true&w=majority
MONGODB_DATABASE=nuam
USE_SQLITE=false
```

Codifica caracteres especiales de usuario/contraseña según el formato URL. Nunca copies una cadena real al repositorio, capturas ni tickets.

```powershell
New-Item -ItemType Directory -Force .local | Out-Null
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo >> .local/demo-accounts.txt
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Abre [la aplicación local](http://127.0.0.1:8000). Las contraseñas aleatorias están en `.local/demo-accounts.txt`; no se versionan. Ejecutar de nuevo `seed_demo` conserva las cuentas existentes y no vuelve a mostrar sus claves: guarda la primera salida. Para cambiar una clave utiliza `manage.py changepassword USUARIO`.

En macOS/Linux: `python3 -m venv .venv` y `.venv/bin/python` en lugar de `.venv\Scripts\python.exe`.

### Demostración sin PostgreSQL

Solo si aún no está disponible: configura `USE_SQLITE=true`, crea `.local`, ejecuta migraciones y carga demo. Es una alternativa explícita para recorrer pantallas; **no acredita la integración con PostgreSQL ni con la nube**. El funcionamiento por defecto requiere PostgreSQL.

### Entorno local preparado en este equipo

La copia de trabajo dispone de PostgreSQL portátil en `.local/postgres`, en `127.0.0.1:55432`. La base es `nuam` y la aplicación utiliza `nuam_app` sin `SUPERUSER`, `CREATEDB` ni `CREATEROLE`. Todo queda fuera de Git; no se instala un servicio global. Tras reiniciar el equipo, desde la raíz del repositorio:

```powershell
& .\.local\postgres\bin\pg_ctl.exe -D .\.local\pgdata -l .\.local\postgres.log -o '-h 127.0.0.1 -p 55432' -w start
# Para detener únicamente esta instancia:
& .\.local\postgres\bin\pg_ctl.exe -D .\.local\pgdata -w stop
```

Los otros integrantes deben configurar su propia conexión; los binarios y las credenciales locales no se comparten. PostgreSQL portátil se obtuvo del paquete de pruebas de [Zonky](https://github.com/zonkyio/embedded-postgres-binaries).

## Cuentas y permisos

| Usuarios demo | Perfil | Acceso |
|---|---|---|
| `operador_a`, `operador_b` | Operador | Consulta propia y pantallas base de ingreso/carga |
| `consultor_a`, `consultor_b` | Consultor | Consulta propia |
| `auditor_a`, `auditor_b` | Auditor | Consulta propia y pantalla base de historial |
| `admin_tecnico` | Administrador técnico | Django Admin para cuentas y grupos |

Los oficiales se comparten como lectura. Los ajustes locales se filtran por el corredor del usuario autenticado, incluso cuando se cambia un ID en la URL. Una cuenta sin rol, sin corredor o con corredor inactivo no puede consultar datos de negocio. El rol técnico queda excluido de esas vistas aunque la cuenta sea superusuario.

La administración requiere cuenta activa, `is_staff` y grupo Administrador técnico. La cuenta demo tiene permisos sobre usuarios/grupos; las calificaciones, factores y el outbox no están registrados en Admin. Los cambios realizados mediante Admin quedan en su registro administrativo de Django. Su sincronización a Atlas queda pendiente junto con la auditoría integral.

## Bases en la nube y auditoría

**Pendiente confirmado:** el equipo aún no tiene PostgreSQL en nube ni clúster Atlas. La ejecución local no sustituye estas evidencias.

1. Crear una base PostgreSQL en el proveedor elegido por el equipo; guardar una conexión TLS en `.env`. Utilizar una cuenta propietaria del esquema para migraciones y una cuenta de ejecución con solo los permisos necesarios sobre tablas/secuencias, sin privilegios globales.
2. Crear un clúster MongoDB Atlas, autorizar las IP del equipo y un usuario de servicio restringido a la base `nuam`. Para el log bastan lectura e inserción/actualización requeridas por el upsert; no dar borrado ni administración del clúster a usuarios operativos.
3. Completar `.env` y aplicar migraciones al PostgreSQL de nube. Cargar únicamente datos ficticios.
4. Verificar conexiones y enviar un evento:

```powershell
.\.venv\Scripts\python.exe manage.py check_connections
.\.venv\Scripts\python.exe manage.py create_audit_probe --username operador_a
.\.venv\Scripts\python.exe manage.py sync_audit
```

`check_connections` termina con error si falta una base o se usa SQLite. No muestra cadenas de conexión. En Atlas Data Explorer o Compass, buscar el UUID mostrado en `nuam.auditoria._id`. Capturar el documento y el resultado del comando sin secretos.

El outbox está en PostgreSQL. `sync_audit` procesa hasta 100 eventos, usa UUID como `_id` y `$setOnInsert` para reintentos idempotentes. Si MongoDB falla, el evento permanece pendiente. La clase 10 incluye el evento de conexión; todavía no hay CRUD de negocio ni garantía de auditoría integral. MongoDB no necesita transacciones multirregistro para este diseño: el lote futuro será atómico en PostgreSQL y la entrega del log será eventual.

## Modelo y navegación

- `core`: usuario personalizado, corredor, calificación, factor y outbox; servicios de acceso y auditoría; vistas y comandos.
- `config`: configuración por variables de entorno, rutas y WSGI.
- `templates` y `static`: interfaz común y estilos adaptables, sin dependencias externas de frontend.
- `docs`: propuesta inicial, alcance, evidencias y trazabilidad con Jira.

La clave local combina corredor, ejercicio, mercado, instrumento, fecha de pago, secuencia y dividendo. Los registros oficiales tienen una clave equivalente sin corredor. Montos como centavos enteros; factores como enteros escalados por `100000000`. Los rangos de columnas y reglas de cálculo deben contrastarse con el HDU antes de la clase 11; aquí no se implementa el cálculo.

Rutas: `/login/`, `/logout/` (POST con CSRF), `/`, `/calificaciones/`, `/calificaciones/<id>/`, `/ingreso/`, `/carga/`, `/historial/` y `/admin/`. Las pantallas base de ingreso/carga/historial no guardan ni simulan operaciones.

## Pruebas

```powershell
# Suite rápida aislada con SQLite en memoria:
.\.venv\Scripts\python.exe manage.py test core.tests --settings=config.test_settings -v 2
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py check
```

Para ejecutar la suite en PostgreSQL usa una **base de pruebas separada** y una cuenta de pruebas con permiso `CREATEDB`. Establece `USE_SQLITE=false` y `DATABASE_URL` en las variables del proceso antes de ejecutar el mismo comando. No otorgues ese permiso a `nuam_app`, ni uses credenciales de producción para pruebas.

La suite verifica aislamiento por lista/ID, permisos, sesión, CSRF, integridad referencial, unicidad, precisión almacenada y conservación de eventos ante errores de transporte. La integración real con Atlas requiere los comandos anteriores; una prueba con transporte sustituido no acredita la nube.

## Trabajo colaborativo y siguiente hito

Se conservan los identificadores y responsables de Jira. Ramas: `main` estable, `dev` integración y `feature/HU-xx` por historia. Las bases `main`/`dev` se inicializan con el repositorio; la implementación se entrega en una rama de trabajo para revisión. Integrar mediante PR revisado por otro integrante. Los commits del agente no acreditan contribuciones personales del resto del equipo.

No cerrar HU-06 ni tareas que incluyan auditoría/funciones posteriores. Para clase 11, el **24/11/2026**, completar las conexiones de nube pendientes y comenzar cálculo y mantenedor. La EVA 3 del paralelo A es el **02/12/2026**.

## Referencias técnicas

- [Usuario personalizado y migración inicial en Django](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/)
- [Login, logout y autenticación Django](https://docs.djangoproject.com/en/5.2/topics/auth/default/)
- [Upsert de MongoDB](https://www.mongodb.com/docs/manual/reference/method/db.collection.updateone/)
- [Jira NUAM](https://maurovaldiviac.atlassian.net/browse/NUAM-6)

Antes de desplegar: `DEBUG=false`, clave secreta propia, `ALLOWED_HOSTS` explícitos y HTTPS. `SECURE_COOKIES=true` en HTTPS. El despliegue y los archivos estáticos del servidor se completarán en la clase 12; `runserver` solo se usa en desarrollo.
