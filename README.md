# Módulo Programador - TSDS - 2026
## ABP - COM B.2 - GRUPO 05


## Modelo ER

```
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

Table productos {
  id integer [primary key]
  tipo_producto_id integer [not null]
  nombre varchar
  descripcion text
  precio decimal
  codigo_barra integer
  fecha_vencimiento date
  stock integer
  updated_at timestamp
  created_at timestamp
}

Table tipo_producto {
  id integer [primary key]
  nombre varchar
}

Table turno_productos {
  id integer [primary key]
  turno_id integer [not null]
  producto_id integer [not null]
  cantidad integer
  }


Table turnos {
  id integer [primary key] 
  cliente_id integer [not null]
  servicio_id integer [not null]
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
Ref: turnos.servicio_id > servicios.id
Ref: turnos.profesional_id > profesionales.id

Ref: servicios.tipo_servicio_id > tipo_servicio.id
Ref: productos.tipo_producto_id > tipo_producto.id
Ref: turnos.tipo_pago_id > tipo_pagos.id

Ref: turno_productos.turno_id > turnos.id
Ref: turno_productos.producto_id > productos.id
```
