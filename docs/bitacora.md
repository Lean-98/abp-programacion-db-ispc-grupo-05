# Bitácora de equipo — Proyecto Turnero

Carrera: Tecnicatura Superior en Desarrollo de Software — ISPC

Materias: Programación I y Base de Datos

Comisión: B2

Grupo: N.º 5 — **Pioneros de Python**

Período documentado: 29 de agosto al 11 de octubre de 2026

---

## Objetivo del proyecto

El equipo desarrolló **Turnero**, una aplicación de escritorio destinada a gestionar clientes, profesionales, servicios, insumos y turnos de una barbería y centro de estética.

El sistema fue implementado con **Python** y **Tkinter** para la interfaz gráfica, y **PostgreSQL** para el almacenamiento de datos. El proyecto integró el diseño de la base de datos, las operaciones de alta, baja, modificación y consulta, las validaciones de los formularios, la configuración del entorno y la documentación técnica y de usuario.

---

## Organización y metodología de trabajo

El equipo trabajó mediante una combinación de reuniones virtuales y comunicación por chat. Estas modalidades permitieron coordinar las tareas, compartir avances, resolver dificultades y organizar la integración de los componentes desarrollados por los distintos integrantes.

La distribución del trabajo contempló diferentes responsabilidades: diseño de la base de datos, acceso a datos, desarrollo de la interfaz, validaciones, documentación y coordinación.

**Git y GitHub** se utilizaron para administrar el código fuente, registrar los cambios realizados y compartir las contribuciones de los integrantes. El historial de commits permite reconstruir la evolución técnica del proyecto y reconocer diversas contribuciones individuales.

---

## Integrantes y responsabilidades

De acuerdo con el README del repositorio, el equipo estuvo integrado por:

Emiliano Nicolás Rivero: coordinación del equipo y desarrollo de funcionalidades de interfaz.

Leandro Alexis Piazza: desarrollo de interfaz, conexión de formularios y operaciones con la base de datos, configuración y documentación del entorno.

Bianca Nahir Piazza: diseño del modelo de datos, diccionario de datos, script DDL y configuración de roles y permisos en **PostgreSQL**.

Tomás Alejandro Villegas: desarrollo e integración de validaciones de los datos ingresados.

Silvina Andrea Otoño: documentación del proyecto, manual de usuario y actividades de prueba.

---

## Registro cronológico de actividades

### 29 y 30 de agosto de 2026 — Inicio y planificación

Se creó el repositorio compartido y se incorporó un primer boceto del diagrama entidad-relación. También se inició la documentación general del proyecto.

Contribuciones registradas: Leandro Alexis Piazza.

Resultado: se establecieron la base del repositorio y los primeros elementos de diseño y documentación.

### 20 de septiembre de 2026 — Diseño de datos e interfaz

Se incorporaron el script DDL, el diccionario de datos, la estructura de carpetas y las actualizaciones del diagrama entidad-relación. También se desarrolló la interfaz base de **Tkinter** y las pantallas ABM de profesionales, servicios e insumos.

Contribuciones registradas:

Bianca Nahir Piazza: documentación del modelo de datos, script DDL y actualización del diagrama.

Leandro Alexis Piazza: estructura de carpetas, documentación principal, interfaz base y conexión inicial de pantallas.

Emiliano Nicolás Rivero: desarrollo de las pantallas ABM de profesionales, servicios e insumos.

Resultado: se estableció la estructura inicial de la aplicación y se documentó el modelo de datos.

### 21 y 28 de septiembre de 2026 — Correcciones del esquema

Se realizaron ajustes al DDL para su compatibilidad con **SQLite** y, posteriormente, se corrigieron tipos y restricciones del esquema y se unificó el nombre del proyecto como **Turnero**.

Contribución registrada: Leandro Alexis Piazza.

Resultado: se avanzó en la adecuación del esquema de la base de datos y en la consistencia del proyecto.

### 9 de octubre de 2026 — Acceso a datos y configuración del entorno

Se desarrollaron funciones de acceso a datos para clientes, turnos, profesionales, servicios, insumos y tipos de pago. Se incorporaron roles de **PostgreSQL** con diferentes permisos y se configuró su integración con **Docker Compose**.

También se documentaron los pasos para instalar las dependencias y ejecutar el entorno de desarrollo.

Contribuciones registradas:

Leandro Alexis Piazza: acceso a datos de clientes y turnos, conexión del ABM de clientes e instructivo de instalación.

Bianca Nahir Piazza: roles y permisos de **PostgreSQL** e integración de roles.sql en **Docker Compose**.

Emiliano Nicolás Rivero: funciones de acceso a datos para profesionales, servicios, insumos y tipos de pago.

Resultado: se estableció la infraestructura necesaria para conectar la aplicación con **PostgreSQL**.

### 10 de octubre de 2026 — Integración de funcionalidades

Se conectaron a la base de datos los ABM de profesionales, servicios e insumos, así como la agenda de turnos. También se conectó el formulario de creación y edición de turnos y se incorporaron datos de prueba mediante docs/seed.sql.

Contribuciones registradas:

Emiliano Nicolás Rivero: conexión de los ABM de profesionales, servicios e insumos y de la agenda de turnos.

Leandro Alexis Piazza: conexión del formulario de turnos, incorporación de datos de prueba y actualización del README.

Silvina Andrea Otoño: actualizaciones del proyecto registradas mediante commits.

Resultado: se integraron las principales pantallas con las operaciones de base de datos y se prepararon datos de ejemplo para las pruebas.

### 11 de octubre de 2026 — Validaciones, documentación y correcciones finales

Se incorporó el módulo de validaciones y se conectó con los formularios de clientes, insumos, profesionales, servicios y turnos. Se agregó el manual de usuario y se implementó un script para generar copias de seguridad de la base de datos.

También se registró una corrección de conflictos de integración que afectaban el funcionamiento de la aplicación.

Contribuciones registradas:

Tomás Alejandro Villegas: módulo de validaciones e integración con los formularios.

Silvina Andrea Otoño: manual de usuario.

Leandro Alexis Piazza: script de respaldo y corrección de conflictos de integración.

Resultado: se ampliaron los controles de entrada, la documentación y las herramientas de respaldo, y se corrigieron problemas de integración.

---

## Herramientas y tecnologías utilizadas

**Python**: lenguaje de programación.

**Tkinter y ttk**: desarrollo de la interfaz gráfica.

**PostgreSQL**: gestión y almacenamiento de datos.

**Docker Compose**: configuración y ejecución del servicio de base de datos.

**SQL**: creación de tablas, restricciones, relaciones, permisos y consultas.

**Git y GitHub**: control de versiones y colaboración.

**Markdown y MkDocs**: organización de la documentación.

## Dificultades y soluciones

- Durante el desarrollo se trabajó sobre distintos aspectos técnicos que quedaron reflejados en los archivos y commits:

- Compatibilidad del esquema: se ajustó el DDL durante la evolución del proyecto para adaptarlo a distintos motores de base de datos.

- Integración con PostgreSQL: se incorporaron funciones de acceso a datos y se conectaron progresivamente las pantallas de gestión.

- Validación de formularios: se creó un módulo compartido para controlar los datos ingresados en las distintas secciones.

- Conflictos de integración: se registró una corrección de conflictos de merge que afectaban la aplicación.

- Respaldo de la información: se agregó un script para generar copias de seguridad de la base de datos.

La resolución de estos puntos contribuyó a consolidar la integración del sistema. Los commits documentan los cambios realizados, aunque no contienen todos los detalles de las conversaciones o del diagnóstico de cada inconveniente.

## Pruebas realizadas

Estas pruebas formaron parte de la verificación de la aplicación antes de considerarla lista para entregar.

Las áreas funcionales que corresponde contemplar en esta verificación incluyen:

- Alta, consulta, modificación y baja de clientes.

- Gestión de profesionales, servicios e insumos.

- Consulta y filtrado de la agenda de turnos.

- Creación y edición de turnos y asociación de servicios.

- Validación de los campos ingresados y presentación de mensajes de error.

- Conexión con **PostgreSQL** y conservación de los datos.

- Configuración del entorno de ejecución.

## Estado final del proyecto

Al cierre del período documentado, el equipo informó que la aplicación funciona correctamente y está lista para entregar.

El material del repositorio muestra la integración de las principales pantallas con **PostgreSQL**, la implementación de validaciones, el esquema relacional con sus restricciones, los datos de prueba, la configuración del entorno y la documentación de instalación y uso.

El resultado representa la integración de las distintas áreas de trabajo del equipo en una aplicación de gestión de turnos.

## Conclusión y aprendizaje grupal

El desarrollo de **Turnero** permitió integrar conocimientos de programación, diseño de bases de datos, interfaces gráficas, consultas SQL, control de versiones y documentación técnica.

La división de responsabilidades hizo posible trabajar en diferentes componentes de manera paralela, mientras que las reuniones virtuales y la comunicación por chat facilitaron la coordinación del trabajo. La integración de los módulos requirió conectar las interfaces con las operaciones de base de datos, unificar criterios y corregir problemas de compatibilidad e integración.

Como aprendizaje general, el proyecto evidencia la importancia de mantener una estructura organizada, documentar los cambios, validar los datos y coordinar las contribuciones de todos los integrantes para obtener un sistema integrado.