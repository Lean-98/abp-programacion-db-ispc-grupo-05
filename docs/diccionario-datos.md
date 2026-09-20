# Diccionario de datos


Este documento detalla, para cada tabla del modelo E-R, el nombre y tipo de dato de cada columna, la clave primaria, las claves foráneas (y a qué tabla remiten) y las restricciones adicionales aplicadas.

---

## clientes

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| nombre | VARCHAR(50) | NOT NULL |
| apellido | VARCHAR(50) | NOT NULL |
| dni | INTEGER | NOT NULL, UNIQUE |
| telefono | INTEGER | |
| direccion | VARCHAR(100) | |
| mail | VARCHAR(100) | |
| rol | VARCHAR(20) | |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | |

---

## profesionales

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| nombre | VARCHAR(50) | NOT NULL |
| apellido | VARCHAR(50) | NOT NULL |
| especialidad | VARCHAR(50) | |
| activo | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | |

---

## tipo_servicio

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| nombre | VARCHAR(50) | NOT NULL, UNIQUE |

---

## servicios

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| tipo_servicio_id | INTEGER | FK → tipo_servicio.id, NOT NULL |
| nombre | VARCHAR(50) | NOT NULL |
| descripcion | TEXT | |
| duracion | INTEGER | CHECK (duracion > 0) — en minutos |
| precio | DECIMAL(10,2) | CHECK (precio >= 0) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | |

---

## tipo_insumo

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| nombre | VARCHAR(50) | NOT NULL, UNIQUE |

---

## insumos

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| tipo_insumo_id | INTEGER | FK → tipo_insumo.id, NOT NULL |
| nombre | VARCHAR(50) | NOT NULL |
| descripcion | TEXT | |
| precio | DECIMAL(10,2) | CHECK (precio >= 0) |
| codigo_barra | INTEGER | UNIQUE |
| fecha_vencimiento | DATE | |
| stock | INTEGER | NOT NULL, DEFAULT 0, CHECK (stock >= 0) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | |

---

## tipo_pagos

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| nombre | VARCHAR(30) | NOT NULL, UNIQUE |

---

## turnos

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| cliente_id | INTEGER | FK → clientes.id, NOT NULL |
| profesional_id | INTEGER | FK → profesionales.id, NOT NULL |
| tipo_pago_id | INTEGER | FK → tipo_pagos.id, NOT NULL |
| fecha | DATETIME | NOT NULL |
| hora_inicio | TIME | |
| hora_fin | TIME | CHECK (hora_fin > hora_inicio) |
| precio_final | DECIMAL(10,2) | CHECK (precio_final >= 0) |
| estado | VARCHAR(20) | NOT NULL, DEFAULT 'pendiente' — valores esperados: pendiente / confirmado / completado / cancelado |
| notas | TEXT | |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | |

---

## turno_servicios

*Tabla intermedia — resuelve la relación N a N entre `turnos` y `servicios` (un turno puede incluir varios servicios).*

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| turno_id | INTEGER | FK → turnos.id, NOT NULL |
| servicio_id | INTEGER | FK → servicios.id, NOT NULL |

Restricción adicional recomendada: `UNIQUE (turno_id, servicio_id)` — evita cargar el mismo servicio dos veces en el mismo turno.

---

## servicio_insumo

*Tabla intermedia — resuelve la relación N a N entre `servicios` e `insumos` (qué insumos, y en qué cantidad, consume cada servicio).*

| Columna | Tipo | Restricciones |
|---|---|---|
| id | INTEGER | PK, autoincremental |
| servicio_id | INTEGER | FK → servicios.id, NOT NULL |
| insumo_id | INTEGER | FK → insumos.id, NOT NULL |
| cantidad | INTEGER | NOT NULL, CHECK (cantidad > 0) |

Restricción adicional recomendada: `UNIQUE (servicio_id, insumo_id)` — evita duplicar la misma línea de receta.

---

## Resumen de relaciones

| Tabla origen (N) | Tabla destino (1) | Columna FK |
|---|---|---|
| turnos | clientes | cliente_id |
| turnos | profesionales | profesional_id |
| turnos | tipo_pagos | tipo_pago_id |
| servicios | tipo_servicio | tipo_servicio_id |
| insumos | tipo_insumo | tipo_insumo_id |
| turno_servicios | turnos | turno_id |
| turno_servicios | servicios | servicio_id |
| servicio_insumo | servicios | servicio_id |
| servicio_insumo | insumos | insumo_id |
