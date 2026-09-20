# Tecnicatura Superior en Desarrollo de Software
## Programación y Base de Datos — Comisión B2 — Grupo N°5
## "Pioneros de Python"

**Profesores:** Enzo Eduardo Bruno y Maria Florencia Garcia Zavia

## Descripción del proyecto

Sistema de gestión de turnos para una barbería y centro de estética, desarrollado como Trabajo Integrador ABP para las materias Programación I y Base de Datos de la Tecnicatura Superior en Desarrollo de Software (ISPC). La aplicación de escritorio permite administrar clientes, profesionales, servicios y turnos desde una interfaz gráfica construida con Tkinter, conectada a una base de datos relacional diseñada y normalizada por el equipo.

## Integrantes y roles

| Rol | Responsabilidad principal | Responsable |
|---|---|---|
| Coordinador | Organiza reuniones, controla el cumplimiento de plazos y consolida las entregas. Además desarrolla su propia funcionalidad. | Rivero Nicolas |
| Modelo de datos | Diseña el modelo E-R, aplica la normalización, redacta el diccionario de datos y el script DDL. Equivalente a un rol de diseñador/a de bases de datos. | Otoño Silvina, Piazza Bianca |
| Interfaz | Construye las ventanas, formularios y listados en Tkinter, y define la navegación entre pantallas. | Rivero Nicolas, Piazza Leandro |
| Acceso a datos | Programa la conexión y las funciones que ejecutan las sentencias SQL desde Python, y configura roles y permisos en el SGBD. | Piazza Bianca, Piazza Leandro |
| Validaciones | Implementa el control de los datos ingresados, el manejo de errores y los mensajes al usuario. | Villegas Tomas |
| Documentación y pruebas | Redacta el informe, arma el manual de usuario y prueba sistemáticamente el sistema. Además desarrolla su propia funcionalidad. | Otoño Silvina |

**Integrantes:** Bianca Nahir Piazza, Leandro Alexis Piazza, Tomas Alejandro Villegas, Emiliano Nicolas Rivero, Silvina Andrea Otoño.

## Tecnologías utilizadas

- **Lenguaje:** Python 3.10+
- **Interfaz gráfica:** Tkinter / ttk
- **Base de datos:** SQLite
- **Control de versiones:** Git / GitHub

## Funcionalidades previstas

- Ventana principal como punto de acceso a las distintas secciones del sistema.
- Alta, baja, modificación y consulta de clientes, profesionales, servicios y turnos.
- Agenda/listado de turnos con búsqueda y filtrado por fecha o cliente.
- Consulta combinada (JOIN) que muestre turnos junto con los datos del cliente, servicio y profesional asociados.
- Validación de los campos obligatorios y mensajes claros al usuario ante operaciones exitosas y errores.

## Modelo ER

```dbml
// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table servicios {
  id integer [primary key]
  tipo_servicio_id integer [not null]
  nombre varchar
  descripcion text
  duracion integer
  precio decimal
  updated_at timestamp
  created_at timestamp
}

Table tipo_servicio {
  id integer [primary key]
  nombre varchar
}


Table profesionales {
  id integer [primary key]
  nombre varchar
  apellido varchar
  especialidad varchar
  activo bool
  updated_at timestamp
  created_at timestamp
}


Table clientes {
  id integer [primary key]
  nombre varchar
  apellido varchar
  dni integer
  telefono integer
  direccion varchar
  mail varchar
  rol varchar
  updated_at timestamp
  created_at timestamp
}

Table insumos {
  id integer [primary key]
  tipo_insumo_id integer [not null]
  nombre varchar
  descripcion text
  precio decimal
  codigo_barra integer
  fecha_vencimiento date
  stock integer
  updated_at timestamp
  created_at timestamp
}

Table tipo_insumo {
  id integer [primary key]
  nombre varchar
}

Table turno_servicios {
  id integer [primary key]
  turno_id integer [not null]
  servicio_id integer [not null]
  }


Table servicio_insumo {
  id integer [primary key]
  servicio_id integer [not null]
  insumo_id integer [not null]
  cantidad integer
  }


Table turnos {
  id integer [primary key] 
  cliente_id integer [not null]
  profesional_id integer [not null]
  tipo_pago_id integer [not null]
  hora_inicio date
  hora_fin date
  fecha datetime [not null]
  precio_final decimal
  estado varchar
  notas text
  updated_at timestamp
  created_at timestamp
}

Table tipo_pagos {
  id integer [primary key]
  nombre varchar
}


// Relación 1 a N 
Ref: turnos.cliente_id > clientes.id
Ref: turnos.profesional_id > profesionales.id

Ref: servicios.tipo_servicio_id > tipo_servicio.id
Ref: insumos.tipo_insumo_id > tipo_insumo.id
Ref: turnos.tipo_pago_id > tipo_pagos.id

// Relación N a N 
Ref: turno_servicios.turno_id > turnos.id
Ref: turno_servicios.servicio_id > servicios.id

Ref: servicio_insumo.servicio_id > servicios.id
Ref: servicio_insumo.insumo_id > insumos.id
```
