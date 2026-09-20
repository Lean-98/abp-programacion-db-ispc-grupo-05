CREATE TABLE "servicios" (
  "id" integer PRIMARY KEY,
  "tipo_servicio_id" integer NOT NULL,
  "nombre" varchar,
  "descripcion" text,
  "duracion" integer,
  "precio" decimal,
  "updated_at" timestamp,
  "created_at" timestamp
);

CREATE TABLE "tipo_servicio" (
  "id" integer PRIMARY KEY,
  "nombre" varchar
);

CREATE TABLE "profesionales" (
  "id" integer PRIMARY KEY,
  "nombre" varchar,
  "apellido" varchar,
  "especialidad" varchar,
  "activo" bool,
  "updated_at" timestamp,
  "created_at" timestamp
);

CREATE TABLE "clientes" (
  "id" integer PRIMARY KEY,
  "nombre" varchar,
  "apellido" varchar,
  "dni" integer,
  "telefono" integer,
  "direccion" varchar,
  "mail" varchar,
  "rol" varchar,
  "updated_at" timestamp,
  "created_at" timestamp
);

CREATE TABLE "insumos" (
  "id" integer PRIMARY KEY,
  "tipo_insumo_id" integer NOT NULL,
  "nombre" varchar,
  "descripcion" text,
  "precio" decimal,
  "codigo_barra" integer,
  "fecha_vencimiento" date,
  "stock" integer,
  "updated_at" timestamp,
  "created_at" timestamp
);

CREATE TABLE "tipo_insumo" (
  "id" integer PRIMARY KEY,
  "nombre" varchar
);

CREATE TABLE "turno_servicios" (
  "id" integer PRIMARY KEY,
  "turno_id" integer NOT NULL,
  "servicio_id" integer NOT NULL
);

CREATE TABLE "servicio_insumo" (
  "id" integer PRIMARY KEY,
  "servicio_id" integer NOT NULL,
  "insumo_id" integer NOT NULL,
  "cantidad" integer
);

CREATE TABLE "turnos" (
  "id" integer PRIMARY KEY,
  "cliente_id" integer NOT NULL,
  "profesional_id" integer NOT NULL,
  "tipo_pago_id" integer NOT NULL,
  "hora_inicio" date,
  "hora_fin" date,
  "fecha" datetime NOT NULL,
  "precio_final" decimal,
  "estado" varchar,
  "notas" text,
  "updated_at" timestamp,
  "created_at" timestamp
);

CREATE TABLE "tipo_pagos" (
  "id" integer PRIMARY KEY,
  "nombre" varchar
);

ALTER TABLE "turnos" ADD FOREIGN KEY ("cliente_id") REFERENCES "clientes" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "turnos" ADD FOREIGN KEY ("profesional_id") REFERENCES "profesionales" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "servicios" ADD FOREIGN KEY ("tipo_servicio_id") REFERENCES "tipo_servicio" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "insumos" ADD FOREIGN KEY ("tipo_insumo_id") REFERENCES "tipo_insumo" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "turnos" ADD FOREIGN KEY ("tipo_pago_id") REFERENCES "tipo_pagos" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "turno_servicios" ADD FOREIGN KEY ("turno_id") REFERENCES "turnos" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "turno_servicios" ADD FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "servicio_insumo" ADD FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "servicio_insumo" ADD FOREIGN KEY ("insumo_id") REFERENCES "insumos" ("id") DEFERRABLE INITIALLY IMMEDIATE;
