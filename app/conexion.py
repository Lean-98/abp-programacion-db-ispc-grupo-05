"""
Conexión a la base de datos PostgreSQL.

host, puerto, usuario,contraseña ños valores por defecto coinciden con docker-compose.yml + docs/roles.sql,
así que funciona "out of the box" en desarrollo sin configurar nada. Se
puede sobrescribir cualquiera con una variable de entorno (útil si alguien
corre PostgreSQL con otro usuario/puerto).

Se conecta con el rol turnero_app (lectura y escritura), no con el
superusuario turnero — turnero_app es el rol pensado para que lo use
la aplicación en el uso normal del día a día (ver docs/roles.sql).
"""
import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras

# Re-exportamos la excepción base de psycopg2 con un nombre propio, para
# que las pantallas (ui/) puedan capturar errores de base de datos sin
# tener que importar psycopg2 directamente.
ErrorBaseDeDatos = psycopg2.Error

CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "turnero"),
    "user": os.environ.get("DB_USER", "turnero_app"),
    "password": os.environ.get("DB_PASSWORD", "app123"),
}


def obtener_conexion():
    """
    Abre y devuelve una nueva conexión a PostgreSQL.

    Las filas se devuelven como diccionarios (RealDictCursor), para que
    el resto del código lea columnas por nombre (fila["nombre"]) en vez
    de por posición.

    Lanza ErrorBaseDeDatos si no puede conectarse (base caída,
    credenciales incorrectas, etc.) — ver obtener_cursor() más abajo,
    que es lo que en la práctica usa datos.py.
    """
    return psycopg2.connect(
        host=CONFIG["host"],
        port=CONFIG["port"],
        dbname=CONFIG["dbname"],
        user=CONFIG["user"],
        password=CONFIG["password"],
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


@contextmanager
def obtener_cursor(commit=False):
    """
    Context manager que abre una conexión + cursor, y se encarga de
    hacer commit (si commit=True y no hubo errores), rollback (si hubo
    una excepción) y cerrar la conexión siempre, pase lo que pase.

    Uso típico en datos.py:

        with conexion.obtener_cursor() as cur:
            cur.execute("SELECT * FROM clientes")
            return cur.fetchall()

        with conexion.obtener_cursor(commit=True) as cur:
            cur.execute("INSERT INTO clientes (...) VALUES (...)")
    """
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
