# Evidencias de implementación

Fecha de verificación: 18/11/2026. Entorno: Windows, Python 3.12, Django 5.2.19 y PostgreSQL 16.16 portátil en localhost. Datos ficticios. No se usan resultados de la unidad 2 como evidencia de esta ejecución.

| Verificación | Resultado obtenido | Evidencia |
|---|---|---|
| Suite en PostgreSQL | 25 pruebas aprobadas; 0 fallos; base test_nuam creada y destruida | [Salida PostgreSQL](evidencias/postgresql-tests.txt) |
| Suite rápida SQLite | 25 pruebas aprobadas; 0 fallos | Comando del README, ejecutado con config.test_settings |
| Configuración Django | Sin incidencias; ninguna migración pendiente de generar | `check`, `makemigrations --check --dry-run` |
| Ajustes de despliegue | `check --deploy` sin incidencias con DEBUG=false y SECURE_COOKIES=true | Comprobación de configuración, no un despliegue publicado |
| Estilo | Ruff sin errores; 28 archivos formateados | `ruff check .` y `ruff format --check .` |
| Chrome y Edge | Login, navegación y logout de 5 perfiles/cuentas en cada navegador; sin errores JavaScript | [Resultado de navegador](evidencias/browser-results.json) |
| Aislamiento en navegador | Cada operador ve su ajuste y el oficial, sin el ajuste del otro corredor | [Listado del corredor A](evidencias/calificaciones.png) |
| Presentación móvil | Login e inicio sin desbordamiento horizontal a 390 px | [Inicio móvil](evidencias/inicio-movil.png) |
| Login | Formulario etiquetado y foco visible | [Acceso](evidencias/login.png) |
| Contraseñas | Hash Argon2; claves demo aleatorias fuera de Git | Suite de acceso y seed_demo |
| Integridad | Rechazo de clave foránea inexistente, duplicados y factores fuera de rango | Suite de modelos |
| MongoDB | Sin configurar; check_connections devuelve error de integración incompleta | Resultado real: relational=postgresql, relational_ok=true, mongodb=sin_configurar |
| Outbox sin Atlas | Evento ficticio conservado sin delivered_at; sync_audit informa que debe reintentarse | Base local; UUID de prueba d6401333-12f4-4517-81fb-a2e5890315a7 |
| Transporte de auditoría | Pruebas de confirmación, datos del evento y reintento idempotente aprobadas con frontera de red sustituida | No acreditan conexión real a Atlas |
| Propuesta Word | 3 páginas exportadas con Word e inspeccionadas como imágenes; sin cortes ni superposiciones | [Documento](Propuesta_NUAM_Clase10.docx) |

## Recorrido de demostración

1. Abrir la aplicación local e iniciar sesión como operador_a con la clave guardada localmente.
2. Consultar calificaciones: se muestran NUAM-DEMO-LOCAL-A y NUAM-DEMO-OFICIAL.
3. Cerrar sesión e ingresar como operador_b: se muestran NUAM-DEMO-LOCAL-B y el oficial.
4. Intentar abrir el ID local de A con B: respuesta 404. Como consultor, abrir /ingreso/: respuesta 403.
5. Ingresar como auditor_a para comprobar el acceso a la pantalla base de historial.
6. Ingresar como admin_tecnico: administrar cuentas y grupos, sin calificaciones disponibles en Admin ni en las rutas de negocio.
7. Ejecutar check_connections y explicar el pendiente de Atlas y de las bases en nube.

## Pendientes que impiden cerrar el hito completo

- Crear PostgreSQL en nube y Atlas; configurar conexiones y probar inserción/lectura del documento en Atlas.
- Agregar colaboradores reales y acceso del docente en GitHub; se necesitan sus identificadores de cuenta.
- Cada integrante debe realizar y acreditar sus propias contribuciones; no se atribuyen los commits del agente a todo el equipo.
- Revisión del equipo, confirmación de sede/grupo y demostración al docente.
- Ejecución por otro integrante siguiendo el README para acreditar instalación independiente.

La búsqueda, cálculo, CRUD, CSV y auditoría integral quedan fuera de esta clase, según el plan.
