# abp-programaci-n-db-ispc-grupo-pp
ABP - TSDS ISPC 2026

// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table servicios {
  id integer [primary key]
  nombre varchar
  descripcion text
  duracion integer
  precio decimal
  updated_at timestamp
  created_at timestamp
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


Table tipo_servicio {
  id integer [primary key]
  nombre varchar
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

Table turnos {
  id integer [primary key]
  cliente_id integer [not null]
  servicio_id integer [not null]
  profesional_id integer [not null]
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


// Relación uno a uno
Ref: servicios.id - tipo_servicio.id
Ref: productos.id - tipo_producto.id
Ref: turnos.id - tipo_pagos.id


// Relación 1 a N (un cliente tiene muchos turnos)
Ref: turnos.cliente_id > clientes.id
Ref: turnos.servicio_id > servicios.id
Ref: turnos.profesional_id > profesionales.id