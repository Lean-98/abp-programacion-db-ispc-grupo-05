-- =============================================================
-- Script DDL — Turnero (barbería y centro de estética)
-- Motor: SQLite
--
-- Correcciones sobre la primera versión (export crudo de dbdiagram):
--   1. Las FK se movieron adentro de cada CREATE TABLE. SQLite no
--      soporta ALTER TABLE ... ADD FOREIGN KEY (no existe ADD CONSTRAINT).
--   2. Se agregó PRAGMA foreign_keys = ON, porque SQLite ignora las
--      FK por defecto si no se activa explícitamente en cada conexión.
--   3. Se agregaron las restricciones NOT NULL / UNIQUE / CHECK / DEFAULT
--      documentadas en docs/diccionario-datos.md (antes el DDL y el
--      diccionario no coincidían).
-- =============================================================

PRAGMA foreign_keys = ON;

-- -------------------------------------------------------------
-- Tablas catálogo (sin FK)
-- -------------------------------------------------------------

CREATE TABLE "tipo_servicio" (
  "id" INTEGER PRIMARY KEY,
  "nombre" VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "tipo_insumo" (
  "id" INTEGER PRIMARY KEY,
  "nombre" VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "tipo_pagos" (
  "id" INTEGER PRIMARY KEY,
  "nombre" VARCHAR(30) NOT NULL UNIQUE
);

-- -------------------------------------------------------------
-- Entidades principales
-- -------------------------------------------------------------

CREATE TABLE "clientes" (
  "id" INTEGER PRIMARY KEY,
  "nombre" VARCHAR(50) NOT NULL,
  "apellido" VARCHAR(50) NOT NULL,
  "dni" INTEGER NOT NULL UNIQUE,
  "telefono" INTEGER,
  "direccion" VARCHAR(100),
  "mail" VARCHAR(100),
  "rol" VARCHAR(20),
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP
);

CREATE TABLE "profesionales" (
  "id" INTEGER PRIMARY KEY,
  "nombre" VARCHAR(50) NOT NULL,
  "apellido" VARCHAR(50) NOT NULL,
  "especialidad" VARCHAR(50),
  "activo" BOOLEAN DEFAULT TRUE,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP
);

CREATE TABLE "servicios" (
  "id" INTEGER PRIMARY KEY,
  "tipo_servicio_id" INTEGER NOT NULL,
  "nombre" VARCHAR(50) NOT NULL,
  "descripcion" TEXT,
  "duracion" INTEGER CHECK ("duracion" > 0),
  "precio" DECIMAL(10,2) CHECK ("precio" >= 0),
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP,
  FOREIGN KEY ("tipo_servicio_id") REFERENCES "tipo_servicio" ("id")
);

CREATE TABLE "insumos" (
  "id" INTEGER PRIMARY KEY,
  "tipo_insumo_id" INTEGER NOT NULL,
  "nombre" VARCHAR(50) NOT NULL,
  "descripcion" TEXT,
  "precio" DECIMAL(10,2) CHECK ("precio" >= 0),
  "codigo_barra" INTEGER UNIQUE,
  "fecha_vencimiento" DATE,
  "stock" INTEGER NOT NULL DEFAULT 0 CHECK ("stock" >= 0),
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP,
  FOREIGN KEY ("tipo_insumo_id") REFERENCES "tipo_insumo" ("id")
);

-- -------------------------------------------------------------
-- Turnos y tablas intermedias (N a N)
-- -------------------------------------------------------------

CREATE TABLE "turnos" (
  "id" INTEGER PRIMARY KEY,
  "cliente_id" INTEGER NOT NULL,
  "profesional_id" INTEGER NOT NULL,
  "tipo_pago_id" INTEGER NOT NULL,
  "fecha" DATETIME NOT NULL,
  "hora_inicio" TIME,
  "hora_fin" TIME CHECK ("hora_fin" > "hora_inicio"),
  "precio_final" DECIMAL(10,2) CHECK ("precio_final" >= 0),
  "estado" VARCHAR(20) NOT NULL DEFAULT 'pendiente'
    CHECK ("estado" IN ('pendiente', 'confirmado', 'completado', 'cancelado')),
  "notas" TEXT,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP,
  FOREIGN KEY ("cliente_id") REFERENCES "clientes" ("id"),
  FOREIGN KEY ("profesional_id") REFERENCES "profesionales" ("id"),
  FOREIGN KEY ("tipo_pago_id") REFERENCES "tipo_pagos" ("id")
);

-- Resuelve turnos <-> servicios (un turno puede incluir varios servicios)
CREATE TABLE "turno_servicios" (
  "id" INTEGER PRIMARY KEY,
  "turno_id" INTEGER NOT NULL,
  "servicio_id" INTEGER NOT NULL,
  UNIQUE ("turno_id", "servicio_id"),
  FOREIGN KEY ("turno_id") REFERENCES "turnos" ("id"),
  FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id")
);

-- Resuelve servicios <-> insumos (qué insumos, y en qué cantidad, consume cada servicio)
CREATE TABLE "servicio_insumo" (
  "id" INTEGER PRIMARY KEY,
  "servicio_id" INTEGER NOT NULL,
  "insumo_id" INTEGER NOT NULL,
  "cantidad" INTEGER NOT NULL CHECK ("cantidad" > 0),
  UNIQUE ("servicio_id", "insumo_id"),
  FOREIGN KEY ("servicio_id") REFERENCES "servicios" ("id"),
  FOREIGN KEY ("insumo_id") REFERENCES "insumos" ("id")
);
