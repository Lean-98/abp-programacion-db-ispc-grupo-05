-- =============================================================
-- Roles de acceso — Turnero
-- Motor: PostgreSQL
--
-- Se corre DESPUÉS de schema.sql (necesita que las tablas ya existan
-- para poder hacer GRANT sobre ellas).
--
-- turnero_lectura: solo consulta (SELECT). Pensado para alguien que
--   solo necesita ver información, por ejemplo el dueño del local
--   revisando la agenda o el stock, sin poder modificar nada.
--
-- turnero_app: lectura y escritura (SELECT, INSERT, UPDATE, DELETE).
--
-- Las contraseñas son simples a propósito, para la demo en clase.
-- =============================================================

-- -------------------------------------------------------------
-- Rol de solo lectura
-- -------------------------------------------------------------

CREATE ROLE turnero_lectura LOGIN PASSWORD 'lectura123';

GRANT CONNECT ON DATABASE turnero TO turnero_lectura;
GRANT USAGE ON SCHEMA public TO turnero_lectura;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO turnero_lectura;

-- Para que las tablas que se creen después también queden con
-- permiso de lectura automáticamente, sin tener que repetir el GRANT.
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO turnero_lectura;

-- -------------------------------------------------------------
-- Rol de lectura y escritura 
-- -------------------------------------------------------------

CREATE ROLE turnero_app LOGIN PASSWORD 'app123';

GRANT CONNECT ON DATABASE turnero TO turnero_app;
GRANT USAGE ON SCHEMA public TO turnero_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO turnero_app;

-- Las columnas SERIAL (id) usan una secuencia interna; sin este GRANT,
-- turnero_app puede hacer SELECT/INSERT pero falla al generar el
-- siguiente id porque no tiene permiso para usar la secuencia.
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO turnero_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO turnero_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
  GRANT USAGE, SELECT ON SEQUENCES TO turnero_app;
