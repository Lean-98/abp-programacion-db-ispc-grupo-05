"""
Acceso a datos: todas las sentencias SQL de la aplicación viven acá.

Regla: este es el ÚNICO archivo (junto con conexion.py) que ejecuta SQL.
Ninguna pantalla en ui/ debe escribir una sentencia SQL — solo llaman a
estas funciones.

Todas las sentencias usan parámetros (%s), nunca f-strings ni .format()
con datos del usuario, para evitar inyección SQL.

Sobre los errores: varias tablas tienen FOREIGN KEY ... ON DELETE RESTRICT
(ver docs/schema.sql), así que un eliminar_* puede fallar a propósito si
el registro todavía tiene referencias (ej. borrar un cliente que tiene
turnos). Eso llega como conexion.ErrorBaseDeDatos — las pantallas deben
capturarlo y mostrar un mensaje claro, no dejar que explote la app.

Alcance de este archivo: por ahora solo clientes y turnos (lo que usan
abm_clientes.py y form_turno.py). Profesionales, servicios, insumos y
sus catálogos (tipo_servicio, tipo_insumo, tipo_pagos) los agrega quien
conecte abm_profesionales.py / abm_servicios.py / abm_insumos.py /
agenda_turnos.py. Mientras tanto, los combos de profesional, servicio
y tipo de pago en form_turno.py quedan vacíos.
"""
from conexion import ErrorBaseDeDatos, obtener_cursor  # noqa: F401  (re-exportado para ui/)


# =================================================================
# Clientes
# =================================================================

def listar_clientes():
    with obtener_cursor() as cur:
        cur.execute("""
            SELECT id, nombre, apellido, dni, telefono, direccion, mail, rol
            FROM clientes
            ORDER BY apellido, nombre
        """)
        return cur.fetchall()


def buscar_clientes(texto):
    patron = f"%{texto}%"
    with obtener_cursor() as cur:
        cur.execute("""
            SELECT id, nombre, apellido, dni, telefono, direccion, mail, rol
            FROM clientes
            WHERE nombre ILIKE %s OR apellido ILIKE %s OR dni ILIKE %s
            ORDER BY apellido, nombre
        """, (patron, patron, patron))
        return cur.fetchall()


def obtener_cliente(cliente_id):
    with obtener_cursor() as cur:
        cur.execute("""
            SELECT id, nombre, apellido, dni, telefono, direccion, mail, rol
            FROM clientes WHERE id = %s
        """, (cliente_id,))
        return cur.fetchone()


def crear_cliente(nombre, apellido, dni, telefono, direccion, mail, rol):
    with obtener_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO clientes (nombre, apellido, dni, telefono, direccion, mail, rol)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (nombre, apellido, dni, telefono, direccion, mail, rol))
        return cur.fetchone()["id"]


def actualizar_cliente(cliente_id, nombre, apellido, dni, telefono, direccion, mail, rol):
    with obtener_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE clientes
            SET nombre = %s, apellido = %s, dni = %s, telefono = %s,
                direccion = %s, mail = %s, rol = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (nombre, apellido, dni, telefono, direccion, mail, rol, cliente_id))


def eliminar_cliente(cliente_id):
    with obtener_cursor(commit=True) as cur:
        cur.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))


# =================================================================
# Turnos (+ turno_servicios)
# =================================================================

def listar_turnos_detalle(fecha=None, cliente=None):
    """
    La consulta JOIN que pide la consigna: trae los turnos con los
    nombres de cliente, profesional y servicios ya resueltos, no IDs.
    Admite filtrar por fecha exacta y/o por nombre/apellido de cliente.
    """
    condiciones = []
    parametros = []

    if fecha:
        condiciones.append('t.fecha::date = %s')
        parametros.append(fecha)
    if cliente:
        condiciones.append('(c.nombre ILIKE %s OR c.apellido ILIKE %s)')
        patron = f"%{cliente}%"
        parametros.extend([patron, patron])

    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

    consulta = f"""
        SELECT
            t.id,
            t.fecha,
            t.hora_inicio,
            t.hora_fin,
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
        {where}
        GROUP BY t.id, c.nombre, c.apellido, p.nombre, p.apellido
        ORDER BY t.fecha, t.hora_inicio
    """
    with obtener_cursor() as cur:
        cur.execute(consulta, parametros)
        return cur.fetchall()


def obtener_turno(turno_id):
    """Trae el turno y la lista de ids de sus servicios (para editar)."""
    with obtener_cursor() as cur:
        cur.execute('SELECT * FROM turnos WHERE id = %s', (turno_id,))
        turno = cur.fetchone()
        if turno is None:
            return None

        cur.execute(
            'SELECT servicio_id FROM turno_servicios WHERE turno_id = %s',
            (turno_id,)
        )
        turno["servicios_ids"] = [fila["servicio_id"] for fila in cur.fetchall()]
        return turno


def crear_turno(cliente_id, profesional_id, tipo_pago_id, fecha, hora_inicio,
                 hora_fin, estado, notas, precio_final, servicios_ids):
    """
    servicios_ids: lista de ids de servicios elegidos en el formulario.
    El turno y sus turno_servicios se insertan en una sola transacción:
    si algo falla, no queda nada guardado a medias.
    """
    with obtener_cursor(commit=True) as cur:
        cur.execute("""
            INSERT INTO turnos (cliente_id, profesional_id, tipo_pago_id, fecha,
                                 hora_inicio, hora_fin, estado, notas, precio_final)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (cliente_id, profesional_id, tipo_pago_id, fecha, hora_inicio,
              hora_fin, estado, notas, precio_final))
        turno_id = cur.fetchone()["id"]

        for servicio_id in servicios_ids:
            cur.execute(
                'INSERT INTO turno_servicios (turno_id, servicio_id) VALUES (%s, %s)',
                (turno_id, servicio_id)
            )
        return turno_id


def actualizar_turno(turno_id, cliente_id, profesional_id, tipo_pago_id, fecha,
                      hora_inicio, hora_fin, estado, notas, precio_final, servicios_ids):
    with obtener_cursor(commit=True) as cur:
        cur.execute("""
            UPDATE turnos
            SET cliente_id = %s, profesional_id = %s, tipo_pago_id = %s, fecha = %s,
                hora_inicio = %s, hora_fin = %s, estado = %s, notas = %s,
                precio_final = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (cliente_id, profesional_id, tipo_pago_id, fecha, hora_inicio,
              hora_fin, estado, notas, precio_final, turno_id))

        # Se borra y se vuelve a armar la lista de servicios del turno,
        # más simple que calcular qué se agregó/sacó.
        cur.execute('DELETE FROM turno_servicios WHERE turno_id = %s', (turno_id,))
        for servicio_id in servicios_ids:
            cur.execute(
                'INSERT INTO turno_servicios (turno_id, servicio_id) VALUES (%s, %s)',
                (turno_id, servicio_id)
            )


def eliminar_turno(turno_id):
    with obtener_cursor(commit=True) as cur:
        # turno_servicios referencia a turnos con ON DELETE RESTRICT, así
        # que hay que borrar esas filas primero o la FK rechaza el DELETE.
        cur.execute('DELETE FROM turno_servicios WHERE turno_id = %s', (turno_id,))
        cur.execute('DELETE FROM turnos WHERE id = %s', (turno_id,))
