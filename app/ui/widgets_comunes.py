"""
Widgets y helpers reutilizables para las pantallas de la aplicación.

Regla: este archivo no debe importar sqlite3 ni nada de acceso a datos.
Solo arma componentes visuales genéricos que las pantallas reutilizan.
"""
import tkinter as tk
from tkinter import ttk


def crear_treeview(parent, columnas):
    """
    Arma un Treeview con scrollbar vertical dentro de un Frame.

    columnas: lista de tuplas (id_columna, texto_encabezado, ancho_px).
    Devuelve (frame_contenedor, treeview). Falta empaquetar/gridear
    frame_contenedor en el layout de quien lo llama.
    """
    contenedor = ttk.Frame(parent)

    ids = [col_id for col_id, _, _ in columnas]
    tree = ttk.Treeview(contenedor, columns=ids, show="headings", selectmode="browse")

    for col_id, texto, ancho in columnas:
        tree.heading(col_id, text=texto)
        tree.column(col_id, width=ancho, anchor="w")

    scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    contenedor.rowconfigure(0, weight=1)
    contenedor.columnconfigure(0, weight=1)

    return contenedor, tree


def campo_formulario(parent, fila, etiqueta, widget_factory=None, **widget_kwargs):
    """
    Arma una fila de formulario: etiqueta a la izquierda + widget a la derecha,
    usando grid sobre `parent`.

    widget_factory: callable(parent, **kwargs) -> widget. Por defecto ttk.Entry.
    Devuelve el widget creado, para guardar la referencia y leer/escribir su valor.
    """
    if widget_factory is None:
        widget_factory = ttk.Entry

    etiqueta_widget = ttk.Label(parent, text=etiqueta)
    etiqueta_widget.grid(row=fila, column=0, sticky="e", padx=(0, 8), pady=4)

    widget = widget_factory(parent, **widget_kwargs)
    widget.grid(row=fila, column=1, sticky="ew", pady=4)

    parent.columnconfigure(1, weight=1)
    return widget


def combo_formulario(parent, fila, etiqueta, valores=None, **kwargs):
    """Atajo de campo_formulario para un ttk.Combobox de solo lectura."""
    return campo_formulario(
        parent,
        fila,
        etiqueta,
        widget_factory=ttk.Combobox,
        values=valores or [],
        state="readonly",
        **kwargs,
    )
