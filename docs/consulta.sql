-- =============================================================
-- Consultas SQL documentadas — Turnero
-- Motor: PostgreSQL
--
-- 5 consultas que responden preguntas reales de gestión del negocio.
-- Incluyen al menos un JOIN, una función de agregación y una
-- subconsulta, como pide la consigna.
-- =============================================================


-- -------------------------------------------------------------
-- 1) Agenda completa: turnos con cliente, profesional y servicios
--    ya resueltos (no IDs). Es la misma consulta que usa la
--    aplicación en la pantalla de Turnos (datos.listar_turnos_detalle).
--    Usa JOIN (x4) y una función de agregación de texto (STRING_AGG)
--    para mostrar varios servicios en una sola fila por turno.
-- -------------------------------------------------------------

SELECT
    t.id,
    t.fecha,
    t.hora_inicio,
    c.nombre || ' ' || c.apellido AS cliente,
    p.nombre || ' ' || p.apellido AS profesional,
    STRING_AGG(s.nombre, ', ' ORDER BY s.nombre) AS servicios,
    t.estado,
    t.precio_final
FROM turnos t
JOIN clientes c ON c.id = t.cliente_id
JOIN profesionales p ON p.id = t.profesional_id
LEFT JOIN turno_servicios ts ON ts.turno_id = t.id
LEFT JOIN servicios s ON s.id = ts.servicio_id
GROUP BY t.id, c.nombre, c.apellido, p.nombre, p.apellido
ORDER BY t.fecha, t.hora_inicio;


-- -------------------------------------------------------------
-- 2) Facturación y cantidad de turnos completados por profesional.
--    Pregunta: ¿cuánto facturó cada profesional y cuántos turnos
--    completó? Sirve para medir carga de trabajo y productividad.
--    Usa JOIN + funciones de agregación (COUNT y SUM).
-- -------------------------------------------------------------

SELECT
    p.nombre || ' ' || p.apellido AS profesional,
    COUNT(t.id) AS cantidad_turnos,
    COALESCE(SUM(t.precio_final), 0) AS facturacion_total
FROM profesionales p
LEFT JOIN turnos t ON t.profesional_id = p.id AND t.estado = 'completado'
GROUP BY p.id, p.nombre, p.apellido
ORDER BY facturacion_total DESC;


-- -------------------------------------------------------------
-- 3) Ranking de servicios más solicitados.
--    Pregunta: ¿qué servicios se piden más? Sirve para decidir
--    promociones, turnos de personal o stock de insumos asociados.
--    Usa JOIN + función de agregación (COUNT).
-- -------------------------------------------------------------

SELECT
    s.nombre AS servicio,
    COUNT(ts.id) AS veces_solicitado
FROM servicios s
LEFT JOIN turno_servicios ts ON ts.servicio_id = s.id
GROUP BY s.id, s.nombre
ORDER BY veces_solicitado DESC;


-- -------------------------------------------------------------
-- 4) Clientes que nunca sacaron un turno.
--    Pregunta: ¿qué clientes están cargados pero nunca vinieron?
--    Sirve para una campaña de contacto o para depurar la base.
--    Usa una subconsulta correlacionada (NOT EXISTS).
-- -------------------------------------------------------------

SELECT c.id, c.nombre, c.apellido, c.telefono
FROM clientes c
WHERE NOT EXISTS (
    SELECT 1 FROM turnos t WHERE t.cliente_id = c.id
)
ORDER BY c.apellido, c.nombre;


-- -------------------------------------------------------------
-- 5) Insumos con stock por debajo del promedio de su mismo tipo.
--    Pregunta: ¿qué insumos conviene reponer, comparados con el
--    resto de su categoría? Sirve como alerta temprana de stock.
--    Usa JOIN + subconsulta correlacionada con función de
--    agregación (AVG) dentro de la subconsulta.
-- -------------------------------------------------------------

SELECT i.nombre, ti.nombre AS tipo, i.stock
FROM insumos i
JOIN tipo_insumo ti ON ti.id = i.tipo_insumo_id
WHERE i.stock < (
    SELECT AVG(i2.stock)
    FROM insumos i2
    WHERE i2.tipo_insumo_id = i.tipo_insumo_id
)
ORDER BY ti.nombre, i.stock;
