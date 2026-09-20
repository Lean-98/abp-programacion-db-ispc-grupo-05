"""
Agenda de turnos: listado con filtros.

Hito 2: solo interfaz visual, sin conexión a la base ni datos de prueba.
El Treeview se arma vacío; se completa en el Hito 3 con
datos.listar_turnos_detalle() (el SELECT con los JOIN a clientes,
profesionales, tipo_pagos, turno_servicios y servicios). Esta pantalla
no debe mostrar IDs, solo nombres — es el requisito de la consulta
combinada que pide la consigna.

Responsable: Nicolás Rivero (Interfaz).
"""
import tkinter as tk
from tkinter import ttk, messagebox

from ui.widgets_comunes import crear_treeview


COLUMNAS = [
    ("fecha", "Fecha", 90),
    ("hora_inicio", "Hora", 60),
    ("cliente", "Cliente", 160),
    ("profesional", "Profesional", 140),
    ("servicios", "Servicios", 200),
    ("estado", "Estado", 100),
    ("precio_final", "Precio", 80),
]


class AgendaTurnos(ttk.Frame):
    def __init__(self, parent, on_nuevo_turno=None, on_editar_turno=None):
        super().__init__(parent)
        self.on_nuevo_turno = on_nuevo_turno
        self.on_editar_turno = on_editar_turno

        self._armar_filtros()
        self._armar_treeview()
        self._armar_botones()

    def _armar_filtros(self):
        frame_filtros = ttk.Frame(self)
        frame_filtros.pack(fill="x", padx=8, pady=(8, 4))

        ttk.Label(frame_filtros, text="Fecha:").pack(side="left")
        self.entry_fecha = ttk.Entry(frame_filtros, width=12)
        self.entry_fecha.pack(side="left", padx=(4, 16))

        ttk.Label(frame_filtros, text="Cliente:").pack(side="left")
        self.entry_cliente = ttk.Entry(frame_filtros, width=20)
        self.entry_cliente.pack(side="left", padx=(4, 16))

        ttk.Button(frame_filtros, text="Filtrar", command=self._filtrar).pack(side="left")
        ttk.Button(
            frame_filtros, text="Limpiar filtro", command=self._limpiar_filtro
        ).pack(side="left", padx=(4, 0))

    def _armar_treeview(self):
        contenedor, self.tree = crear_treeview(self, COLUMNAS)
        contenedor.pack(fill="both", expand=True, padx=8, pady=4)

    def _armar_botones(self):
        frame_botones = ttk.Frame(self)
        frame_botones.pack(fill="x", padx=8, pady=(4, 8))

        ttk.Button(frame_botones, text="Nuevo turno", command=self._nuevo_turno).pack(side="left")
        ttk.Button(frame_botones, text="Editar", command=self._editar_turno).pack(
            side="left", padx=(4, 0)
        )
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar_turno).pack(
            side="left", padx=(4, 0)
        )

    # --- Acciones (simuladas en Hito 2, sin persistencia real) ---

    def _filtrar(self):
        # Hito 3: reemplazar por datos.listar_turnos_detalle(fecha=..., cliente=...)
        messagebox.showinfo("Filtro", "Sin datos todavía: se completa en el Hito 3.")

    def _limpiar_filtro(self):
        self.entry_fecha.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)

    def _nuevo_turno(self):
        if self.on_nuevo_turno:
            self.on_nuevo_turno()

    def _editar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Editar turno", "Seleccioná un turno de la lista.")
            return
        if self.on_editar_turno:
            self.on_editar_turno(seleccion[0])

    def _eliminar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar turno", "Seleccioná un turno de la lista.")
            return
        if messagebox.askyesno(
            "Eliminar turno", "¿Confirmás que querés eliminar el turno seleccionado?"
        ):
            self.tree.delete(seleccion[0])
            messagebox.showinfo("Eliminar turno", "Turno eliminado (simulado).")
