-- =============================================================
-- Script DDL — Turnero
-- Motor: PostgreSQL
--
-- Migrado desde SQLite (usado como prototipo en el Hito 2):
--   1. INTEGER PRIMARY KEY -> SERIAL PRIMARY KEY, para autoincremento
--      real (en SQLite un INTEGER PRIMARY KEY ya autoincrementa solo;
--      en PostgreSQL hace falta SERIAL, que crea una secuencia).
--   2. DATETIME -> TIMESTAMP (DATETIME no es un tipo válido en
--      PostgreSQL).
--   3. Se quitó "PRAGMA foreign_keys = ON", que es específico de
--      SQLite. En PostgreSQL las claves foráneas siempre se validan.
--   4. El resto (NOT NULL, UNIQUE, CHECK, DEFAULT, ON DELETE RESTRICT)
--      ya estaba en sintaxis estándar y no cambió.
-- =============================================================

-- -------------------------------------------------------------
-- Tablas catálogo (sin FK)
-- -------------------------------------------------------------

CREATE TABLE "tipo_servicio" (
  "id" SERIAL PRIMARY KEY,
  "nombre" VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "tipo_insumo" (
  "id" SERIAL PRIMARY KEY,
  "nombre" VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "tipo_pagos" (
  "id" SERIAL PRIMARY KEY,
  "nombre" VARCHAR(30) NOT NULL UNIQUE
);

-- -------------------------------------------------------------
-- Entidades principales
-- -------------------------------------------------------------

CREATE TABLE "clientes" (
  "id" SERIAL PRIMARY KEY,
  "nombre" VARCHAR(50) NOT NULL,
  "apellido" VARCHAR(50) NOT NULL,
  "dni" VARCHAR(10) NOT NULL UNIQUE,
  "telefono" VARCHAR(20),
  "direccion" VARCHAR(100),
  "mail" VARCHAR(100),
  "rol" VARCHAR(20),
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP
);

CREATE TABLE "profesionales" (
  "id" SERIAL PRIMARY KEY,
  "nombre" VARCHAR(50) NOT NULL,
  "apellido" VARCHAR(50) NOT NULL,
  "especialidad" VARCHAR(50),
  "activo" BOOLEAN DEFAULT TRUE,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP
);

CREATE TABLE "servicios" (
  "id" SERIAL PRIMARY KEY,
  "tipo_servicio_id" INTEGER NOT NULL,
  "nombre" VARCHAR(50) NOT NULL,
  "descripcion" TEXT,
  "duracion" INTEGER CHECK ("duracion" > 0),
  "precio" DECIMAL(10,2) NOT NULL CHECK ("precio" >= 0),
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP,
  FOREIGN KEY ("tipo_servicio_id") REFERENCES "tipo_servicio" ("id") ON DELETE RESTRICT
);

CREATE TABLE "insumos" (
  "id" SERIAL PRIMARY KEY,
  "tipo_insumo_id" INTEGER NOT NULL,
  "nombre" VARCHAR(50) NOT NULL,
  "descripcion" TEXT,
  "precio" DECIMAL(10,2) NOT NULL CHECK ("precio" >= 0),
  "codigo_barra" VARCHAR(20) UNIQUE,
  "fecha_vencimiento" DATE,
  "stock" INTEGER NOT NULL DEFAULT 0 CHECK ("stock" >= 0),
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP,
  FOREIGN KEY ("tipo_insumo_id") REFERENCES "tipo_insumo" ("id") ON DELETE RESTRICT
);

-- -------------------------------------------------------------
-- Turnos y tablas intermedias (N a N)
-- -------------------------------------------------------------

CREATE TABLE "turnos" (
  "id" SERIAL PRIMARY KEY,
  "cliente_id" INTEGER NOT NULL,
  "profesional_id" INTEGER NOT NULL,
  "tipo_pago_id" INTEGER NOT NULL,
  "fecha" TIMESTAMP NOT NULL,
  "hora_inicio" TIME,
  "hora_fin" TIME CHECK ("hora_fin" > "hora_inicio"),
  "precio_final" DECIMAL(10,2) CHECK ("precio_final" >= 0),
  "estado" VARCHAR(20) NOT NULL DEFAULT 'pendiente'
    CHECK ("estado" IN ('pendiente', 'confirmado', 'completado', 'cancelado')),
  "notas" TEXT,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP,
  FOREIGN KEY ("cliente_id") REFERENCES "clientes" ("id") ON DELETE RESTRICT,
  FOREIGN KEY ("profesional_id") REFERENCES "profesionales" ("id") ON DELETE RESTRICT,
  FOREIGN KEY ("tipo_pago_id") REFERENCES "tipo_pagos" ("id") ON DELETE RESTRICT
);

-- Resuelve turnos <-> servicios (un turno puede incluir varios servicios)
CREATE TABLE "turno_servicios" (
  "id" SERIAL PRIMARY KEY,
  "turno_id" INTEGER NOT NULL,
  "servicio_id" INTEGER NOT NULL,
  UNIQUE ("turno_id", "servicio_id"),
  FOREIGN KEY ("turno_id") REFERENCES "turnos" ("id") ON DELETE RESTRICT,
  FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id") ON DELETE RESTRICT
);

-- Resuelve servicios <-> insumos (qué insumos, y en qué cantidad, consume cada servicio)
CREATE TABLE "servicio_insumo" (
  "id" SERIAL PRIMARY KEY,
  "servicio_id" INTEGER NOT NULL,
  "insumo_id" INTEGER NOT NULL,
  "cantidad" INTEGER NOT NULL CHECK ("cantidad" > 0),
  UNIQUE ("servicio_id", "insumo_id"),
  FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id") ON DELETE RESTRICT,
  FOREIGN KEY ("insumo_id") REFERENCES "insumos" ("id") ON DELETE RESTRICT
);
