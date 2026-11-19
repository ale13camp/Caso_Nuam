# Plan de implementación de la clase 10

Fecha: 18/11/2026. Paralelo A. Plan autorizado en la conversación.

Objetivo: aplicación Django con PostgreSQL, conexión preparada a Atlas, login, roles y aislamiento; documento inicial de propuesta para nuam. Partida: repositorio remoto vacío y tablero Jira existente.

- [x] Entorno, repositorio aislado en rama feature y dependencias.
- [x] Modelos, migraciones y datos ficticios de dos corredores.
- [x] Login, permisos, interfaces y consulta mínima protegida.
- [x] Comandos de diagnóstico, evento de prueba y entrega idempotente de auditoría.
- [ ] Bases en nube y documento visible en Atlas: no existen las cuentas/recursos aún.
- [x] Pruebas finales, revisión de código y propuesta Word de tres páginas.
- [ ] Revisión del equipo y demostración al docente.

Dependencias: entorno → modelos/usuarios → acceso/interfaces → pruebas. Los cambios en datos de negocio y la auditoría integral quedan para próximas clases. Las tareas con alcance posterior permanecen abiertas.

Decisiones: PostgreSQL reemplaza SQLite del diseño U2; MongoDB solo para auditoría/cargas. Se permite SQLite explícito para demo y pruebas rápidas, sin presentarlo como evidencia de integración. No se inventan contribuciones del equipo ni resultados de nube.
