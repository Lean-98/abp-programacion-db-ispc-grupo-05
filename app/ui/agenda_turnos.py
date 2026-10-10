"""
Agenda de turnos — conectada a PostgreSQL vía datos.py.

El Treeview se llena con datos.listar_turnos_detalle(), la consulta con
los JOIN a clientes, profesionales, turno_servicios y servicios. Esta
pantalla no muestra IDs, solo nombres — es el requisito de la consulta
combinada que pide la consigna.

Responsable: Nicolás Rivero (Interfaz).
"""
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

import datos
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
        self._refrescar_listado()

    def _armar_filtros(self):
        frame_filtros = ttk.Frame(self)
        frame_filtros.pack(fill="x", padx=8, pady=(8, 4))

        ttk.Label(frame_filtros, text="Fecha (DD/MM/AAAA):").pack(side="left")
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

    # --- Listado: traer datos reales ---

    def _refrescar_listado(self, filas=None, fecha=None, cliente=None):
        self.tree.delete(*self.tree.get_children())
        try:
            if filas is None:
                filas = datos.listar_turnos_detalle(fecha=fecha, cliente=cliente)
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror(
                "Error de conexión", f"No se pudo conectar a la base de datos:\n{e}"
            )
            return

        for fila in filas:
            self.tree.insert(
                "", "end", iid=str(fila["id"]),
                values=(
                    fila["fecha"].strftime("%d/%m/%Y") if fila["fecha"] else "",
                    fila["hora_inicio"].strftime("%H:%M") if fila["hora_inicio"] else "",
                    fila["cliente"],
                    fila["profesional"],
                    fila["servicios"] or "",
                    fila["estado"],
                    fila["precio_final"] if fila["precio_final"] is not None else "",
                ),
            )

    # --- Acciones ---

    def _filtrar(self):
        fecha_texto = self.entry_fecha.get().strip()
        cliente_texto = self.entry_cliente.get().strip() or None

        fecha = None
        if fecha_texto:
            try:
                fecha = datetime.strptime(fecha_texto, "%d/%m/%Y").date()
            except ValueError:
                messagebox.showerror(
                    "Fecha inválida", "La fecha debe tener el formato DD/MM/AAAA."
                )
                return

        self._refrescar_listado(fecha=fecha, cliente=cliente_texto)

    def _limpiar_filtro(self):
        self.entry_fecha.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self._refrescar_listado()

    def _nuevo_turno(self):
        if self.on_nuevo_turno:
            self.on_nuevo_turno()

    def _editar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Editar turno", "Seleccioná un turno de la lista.")
            return
        if self.on_editar_turno:
            self.on_editar_turno(int(seleccion[0]))

    def _eliminar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar turno", "Seleccioná un turno de la lista.")
            return

        if not messagebox.askyesno(
            "Eliminar turno", "¿Confirmás que querés eliminar el turno seleccionado?"
        ):
            return

        try:
            datos.eliminar_turno(int(seleccion[0]))
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("No se pudo eliminar", f"Error al eliminar el turno:\n{e}")
            return

        messagebox.showinfo("Eliminar turno", "Turno eliminado correctamente.")
        self._refrescar_listado()
