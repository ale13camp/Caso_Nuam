# Propuesta inicial del mantenedor de calificaciones tributarias NUAM DJ 1948

Proyecto Integrado TIHV43 · Ingeniería en Informática · INACAP
Destinatario: nuam
Equipo: Mauro Valdivia, Alejandra Campusano y Polette Henríquez
Docente: Sebastián Álvarez Trujillo
Paralelo A · 18 de noviembre de 2026 · Chile
Sede y número de grupo: por confirmar
Estado: propuesta inicial correspondiente a la clase 10

## Presentación

Proponemos implementar un mantenedor web para centralizar las calificaciones tributarias de la DJ 1948. La solución busca reducir los errores asociados al ingreso manual y distinguir la información oficial de los ajustes de cada corredor. En esta primera etapa preparamos el acceso por perfiles, la estructura de datos y las pantallas que permitirán desarrollar las operaciones de negocio en las clases siguientes.

## Equipo líder

Mauro Valdivia participa en la configuración del entorno y el desarrollo de autenticación y permisos. Sus responsabilidades registradas en Jira incluyen el cálculo de factores y la consulta de calificaciones. Esa participación en el diseño y las reglas de negocio fundamenta su función técnica en la implementación.

Alejandra Campusano participa en el modelado de usuarios, corredores y calificaciones, además de la preparación de la auditoría. El tablero también le asigna actividades de modificación de registros y validación de archivos. Su participación documentada en el diseño de datos permite dar continuidad entre el informe de la unidad 2 y las restricciones de la implementación.

Polette Henríquez participa en las interfaces de acceso y mantenedor, en las pruebas de aislamiento y en la preparación de la propuesta. Sus tareas registradas conectan los criterios de aceptación con los recorridos del usuario. Esta continuidad entre interfaz y verificación fundamenta su función en la experiencia de uso y la revisión funcional.

Estas funciones corresponden a responsabilidades de trabajo registradas en Jira. Cada integrante deberá revisar su descripción y complementar únicamente antecedentes verificables antes de la entrega definitiva.

## Objetivo general

Implementar un mantenedor web de calificaciones tributarias DJ 1948 que centralice la información, proteja los datos de cada corredor y permita desarrollar operaciones trazables con validaciones comunes.

## Objetivos específicos

1. Habilitar autenticación y permisos para Operador, Consultor, Auditor y Administrador técnico, aplicados en el servidor.
2. Mantener separados los registros oficiales y los ajustes locales, evitando accesos entre corredores mediante restricciones de datos y autorización.
3. Preparar la persistencia relacional en PostgreSQL y la entrega de eventos de auditoría a MongoDB Atlas, conservando evidencia ante fallos de conexión.
4. Construir la navegación base del mantenedor y verificar su acceso mediante pruebas reproducibles y datos ficticios.
5. En las etapas siguientes, incorporar cálculo decimal, mantención e importación CSV y comparar los resultados obtenidos con el plan de pruebas de la unidad 2.

## Beneficios esperados y verificación

Para nuam, la solución propone una estructura común para consultar información y seguir las modificaciones. Para los corredores, busca evitar el acceso a ajustes ajenos y reducir errores de preparación mediante validaciones compartidas. La reducción de tiempos y errores es un beneficio esperado; todavía no se ha medido y requiere una comparación con el proceso actual.

El hito de clase 10 se aceptará al demostrar una instalación reproducible, usuarios de dos corredores sin acceso cruzado, permisos por perfil y restricciones de integridad. La conexión de nube deberá acreditarse con PostgreSQL conectado y un documento de prueba visible en Atlas.

## Alcance de esta primera etapa

La arquitectura utiliza Django con plantillas, PostgreSQL para usuarios y calificaciones y MongoDB Atlas para auditoría. PostgreSQL reemplaza SQLite de la propuesta U2 para atender la base relacional en nube. La demostración local no acredita por sí sola esa conexión.

El equipo confirmó que todavía no dispone de PostgreSQL en nube ni de un clúster Atlas. Ambos recursos quedan pendientes de creación y configuración. Cálculo, edición, eliminación, carga CSV y consulta completa del historial se implementarán en las clases posteriores. Las secciones de desafío, justificación, enfoque técnico, gestión y resultados se completarán según la ruta de la unidad 3.
