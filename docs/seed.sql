-- =============================================================
-- Datos de prueba — Turnero
-- Motor: PostgreSQL
--
-- Se corre DESPUÉS de docs/schema.sql, contra una base vacía (los ids
-- se dejan que los asigne SERIAL automáticamente, por eso el orden de
-- los INSERT importa: cada tabla referencia los ids de las anteriores
-- en el mismo orden en que quedan 1, 2, 3...).
-- =============================================================

-- -------------------------------------------------------------
-- Catálogos
-- -------------------------------------------------------------

INSERT INTO "tipo_servicio" ("nombre") VALUES
  ('Corte'),
  ('Barba'),
  ('Color'),
  ('Tratamiento facial'),
  ('Manicura'),
  ('Depilación');

INSERT INTO "tipo_insumo" ("nombre") VALUES
  ('Cosmético'),
  ('Higiene y descartables'),
  ('Herramienta'),
  ('Insumo capilar'),
  ('Insumo de manicura');

INSERT INTO "tipo_pagos" ("nombre") VALUES
  ('Efectivo'),
  ('Tarjeta de débito'),
  ('Tarjeta de crédito'),
  ('Transferencia'),
  ('Mercado Pago');

-- -------------------------------------------------------------
-- Clientes (10)
-- -------------------------------------------------------------

INSERT INTO "clientes" ("nombre", "apellido", "dni", "telefono", "direccion", "mail", "rol") VALUES
  ('Martina', 'Gómez', '30123456', '3511234567', 'Av. Colón 1234', 'martina.gomez@example.com', 'cliente'),
  ('Lucas', 'Fernández', '32456789', '3512345678', 'Bv. San Juan 456', 'lucas.fernandez@example.com', 'cliente'),
  ('Sofía', 'Rodríguez', '35123123', '3513456789', 'Rivera Indarte 789', 'sofia.rodriguez@example.com', 'VIP'),
  ('Mateo', 'López', '33987654', '3514567890', 'Duarte Quirós 234', 'mateo.lopez@example.com', 'cliente'),
  ('Valentina', 'Martínez', '36789012', '3515678901', 'Fructuoso Rivera 567', 'valentina.martinez@example.com', 'cliente'),
  ('Joaquín', 'García', '31456123', '3516789012', 'Vélez Sarsfield 890', 'joaquin.garcia@example.com', 'cliente'),
  ('Camila', 'Pérez', '34567890', '3517890123', 'Obispo Trejo 345', 'camila.perez@example.com', 'VIP'),
  ('Bautista', 'Sánchez', '37123456', '3518901234', 'Illia 678', 'bautista.sanchez@example.com', 'cliente'),
  ('Emma', 'Díaz', '38234567', '3519012345', 'Caseros 901', 'emma.diaz@example.com', 'cliente'),
  ('Thiago', 'Romero', '39345678', '3510123456', 'Humberto Primo 123', 'thiago.romero@example.com', 'cliente'),
  ('Milena', 'Suárez', '40111222', '3511111111', 'Rondeau 456', 'milena.suarez@example.com', 'cliente'),
  ('Ignacio', 'Castro', '40222333', '3512222222', 'Entre Ríos 789', 'ignacio.castro@example.com', 'cliente');

-- -------------------------------------------------------------
-- Profesionales (10)
-- -------------------------------------------------------------

INSERT INTO "profesionales" ("nombre", "apellido", "especialidad", "activo") VALUES
  ('Agustín', 'Torres', 'Barbero', TRUE),
  ('Federico', 'Molina', 'Barbero', TRUE),
  ('Julieta', 'Acosta', 'Colorista', TRUE),
  ('Rocío', 'Herrera', 'Esteticista', TRUE),
  ('Nicolás', 'Ferreyra', 'Barbero', TRUE),
  ('Milagros', 'Ortiz', 'Manicura', TRUE),
  ('Ezequiel', 'Aguirre', 'Barbero', FALSE),
  ('Abril', 'Ríos', 'Esteticista', TRUE),
  ('Santiago', 'Vega', 'Colorista', TRUE),
  ('Catalina', 'Juárez', 'Manicura', TRUE);

-- -------------------------------------------------------------
-- Servicios (10) — tipo_servicio_id: 1 Corte, 2 Barba, 3 Color,
-- 4 Tratamiento facial, 5 Manicura, 6 Depilación
-- -------------------------------------------------------------

INSERT INTO "servicios" ("tipo_servicio_id", "nombre", "descripcion", "duracion", "precio") VALUES
  (1, 'Corte clásico', 'Corte de cabello tradicional', 30, 4500.00),
  (1, 'Corte + lavado', 'Corte de cabello con lavado incluido', 45, 5500.00),
  (2, 'Arreglo de barba', 'Perfilado y prolijo de barba', 20, 3000.00),
  (2, 'Barba + afeitado', 'Arreglo de barba con afeitado a navaja', 30, 4000.00),
  (3, 'Coloración completa', 'Aplicación de color en todo el cabello', 90, 12000.00),
  (3, 'Mechas', 'Mechas con técnica de balayage', 120, 15000.00),
  (4, 'Limpieza facial', 'Limpieza facial profunda', 60, 8000.00),
  (4, 'Hidratación facial', 'Hidratación con productos específicos', 45, 7000.00),
  (5, 'Manicura clásica', 'Manicura tradicional', 40, 3500.00),
  (6, 'Depilación cejas', 'Depilación y diseño de cejas', 15, 2000.00);

-- -------------------------------------------------------------
-- Insumos (10) — tipo_insumo_id: 1 Cosmético, 2 Higiene y descartables,
-- 3 Herramienta, 4 Insumo capilar, 5 Insumo de manicura
-- -------------------------------------------------------------

INSERT INTO "insumos" ("tipo_insumo_id", "nombre", "descripcion", "precio", "codigo_barra", "fecha_vencimiento", "stock") VALUES
  (1, 'Shampoo profesional', 'Shampoo para todo tipo de cabello', 3500.00, '7791234567891', '2027-06-30', 20),
  (1, 'Tintura rubio ceniza', 'Tintura permanente', 4200.00, '7791234567892', '2026-12-31', 15),
  (2, 'Toallas descartables', 'Toallas de un solo uso', 500.00, '7791234567893', NULL, 200),
  (2, 'Guantes de látex (caja)', 'Caja x100 unidades', 1200.00, '7791234567894', NULL, 50),
  (3, 'Máquina de corte', 'Máquina eléctrica para corte de cabello', 25000.00, '7791234567895', NULL, 5),
  (3, 'Tijera de barbero', 'Tijera de acero inoxidable', 8000.00, '7791234567896', NULL, 8),
  (4, 'Cera para peinar', 'Cera de fijación fuerte', 2200.00, '7791234567897', '2027-03-15', 30),
  (4, 'Acondicionador', 'Acondicionador hidratante', 3000.00, '7791234567898', '2027-01-20', 18),
  (5, 'Esmalte semipermanente', 'Esmalte de larga duración', 2800.00, '7791234567899', '2026-11-10', 25),
  (5, 'Removedor de cutícula', 'Gel removedor de cutículas', 1500.00, '7791234567900', '2027-05-05', 12);

-- -------------------------------------------------------------
-- Turnos (12), en 3 fechas distintas — cliente_id y profesional_id
-- del 1 al 10, tipo_pago_id del 1 al 5, en el mismo orden en que
-- quedaron cargados arriba.
-- -------------------------------------------------------------

INSERT INTO "turnos" ("cliente_id", "profesional_id", "tipo_pago_id", "fecha", "hora_inicio", "hora_fin", "precio_final", "estado", "notas") VALUES
  (1, 1, 1, '2026-09-15 10:00:00', '10:00', '10:30', 4500.00, 'completado', NULL),
  (2, 2, 2, '2026-09-15 11:00:00', '11:00', '11:45', 5500.00, 'completado', NULL),
  (3, 3, 3, '2026-09-15 14:00:00', '14:00', '15:30', 12000.00, 'completado', NULL),
  (4, 1, 1, '2026-09-16 09:30:00', '09:30', '10:00', 7500.00, 'confirmado', NULL),
  (5, 4, 4, '2026-09-16 10:30:00', '10:30', '11:30', 8000.00, 'confirmado', NULL),
  (6, 5, 1, '2026-09-16 12:00:00', '12:00', '12:20', 3000.00, 'pendiente', NULL),
  (7, 6, 2, '2026-09-16 15:00:00', '15:00', '15:40', 3500.00, 'pendiente', NULL),
  (8, 9, 5, '2026-09-18 09:00:00', '09:00', '11:00', 15000.00, 'confirmado', NULL),
  (9, 1, 1, '2026-09-18 10:00:00', '10:00', '10:30', 4500.00, 'cancelado', 'Cliente canceló por lluvia'),
  (10, 8, 3, '2026-09-18 11:30:00', '11:30', '12:15', 7000.00, 'pendiente', NULL),
  (1, 2, 1, '2026-09-19 09:00:00', '09:00', '09:30', 4000.00, 'pendiente', NULL),
  (3, 10, 2, '2026-09-19 16:00:00', '16:00', '16:15', 2000.00, 'pendiente', NULL);

-- -------------------------------------------------------------
-- Servicios incluidos en cada turno (turno_id y servicio_id en el
-- mismo orden en que quedaron cargados arriba — algunos turnos
-- tienen más de un servicio)
-- -------------------------------------------------------------

INSERT INTO "turno_servicios" ("turno_id", "servicio_id") VALUES
  (1, 1),
  (2, 2),
  (3, 5),
  (4, 1),
  (4, 3),
  (5, 7),
  (6, 3),
  (7, 9),
  (8, 6),
  (9, 1),
  (10, 8),
  (11, 4),
  (12, 10);

-- -------------------------------------------------------------
-- Insumos que consume cada servicio
-- -------------------------------------------------------------

INSERT INTO "servicio_insumo" ("servicio_id", "insumo_id", "cantidad") VALUES
  (1, 1, 1),
  (2, 1, 1),
  (2, 3, 2),
  (3, 7, 1),
  (4, 7, 1),
  (4, 4, 1),
  (5, 2, 1),
  (5, 4, 2),
  (6, 2, 2),
  (6, 4, 2),
  (7, 3, 3),
  (8, 8, 1),
  (9, 9, 1),
  (9, 10, 1),
  (10, 3, 1);
