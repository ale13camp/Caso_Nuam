# Registro de implementación de la clase 10

Plan: docs/plan-clase10.md. Fecha: 18/11/2026. Referencias: guía de clase 10, informe final U2 y proyecto Jira NUAM (56 elementos consultados).

## Decisiones

- Trabajo en un clon nuevo dentro de Eva 3/Caso_Nuam y rama feature/HU-06-clase10. El remoto estaba vacío; main/dev se inicializan desde un commit de base. No hay trabajo previo que aislar con un worktree adicional.
- Se implementa el plan aprobado sin ampliar cálculo, CRUD ni CSV. Las pruebas se escribieron primero y fallaron por ausencia de modelos/comandos; después se implementaron y pasaron.
- El equipo confirmó que aún no tiene recursos de nube. Se preparan variables y comandos; se verifica PostgreSQL real local y se mantiene Atlas como pendiente.
- Se permite SQLite únicamente con activación explícita para pruebas rápidas o demo. La aplicación local preparada utiliza PostgreSQL con rol nuam_app de mínimo privilegio global. La suite PostgreSQL utiliza una cuenta separada para crear y destruir su base de prueba.
- Se usa Django Admin para usuarios y grupos. El registro administrativo de Django conserva sus cambios; el envío de esos cambios a Atlas queda para auditoría integral.
- El evento de prueba de auditoría queda en el outbox. No se afirma su entrega mientras Atlas no esté configurado.
- El documento refleja responsabilidades existentes de Jira; no inventa experiencia, contribuciones ni mediciones de beneficios.

## Cambios de seguimiento

Se ajustaron NUAM-16, NUAM-17 y NUAM-23 para expresar Django/PostgreSQL/Atlas, conservando responsables e identificadores. No se cerraron tareas ni se publicaron comentarios en nombre del equipo.

## Progreso

- Entorno y modelos: implementados; migraciones aplicadas en PostgreSQL local.
- Acceso e interfaces: implementados con consulta mínima para comprobar aislamiento.
- Conexiones: PostgreSQL local comprobado. Atlas y PostgreSQL en nube pendientes.
- Propuesta: texto inicial en Markdown y documento Word generado desde el mismo contenido.
- Revisión independiente: detectó que un transporte MongoDB sin confirmación podía marcar eventos como entregados. Se agregó confirmación por mayoría y rechazo de resultados no confirmados, con regresión RED → GREEN y pruebas de entrega/reintento. La integración real con Atlas sigue pendiente.
- Ajuste de instrucciones: la salida de credenciales demo se agrega al archivo local para no perder claves al repetir la instalación.
- Render de propuesta: el renderizador LibreOffice no está instalado en este equipo. Se utilizó Word instalado, exportación PDF y rasterización para inspeccionar las tres páginas; se eliminó un borde heredado de la plantilla.

Las pruebas locales nuevas no sustituyen las evidencias históricas de la unidad 2. Los commits del agente tampoco prueban contribuciones de cada integrante.

## Verificación final

25/25 pruebas aprobadas en SQLite y 25/25 en PostgreSQL. Chrome y Edge: login y navegación de cinco cuentas, aislamiento de operadores y presentación móvil comprobados. Ruff, migraciones y comprobación de despliegue sin incidencias. La propuesta tiene tres páginas verificadas visualmente. Sin hallazgos de código importantes pendientes tras la corrección; conexiones en nube, colaboradores y demostración docente pendientes.
