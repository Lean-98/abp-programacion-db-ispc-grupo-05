"""
ABM de clientes.

Esta es la pantalla patrón: listado con búsqueda a la izquierda,
formulario a la derecha, botones Nuevo / Guardar / Eliminar. Sirve de
modelo para las pantallas de Profesionales, Servicios e Insumos (mismo
esqueleto, cambiando columnas y campos).

Hito 2: solo interfaz visual, sin conexión a la base ni datos de prueba.
El Treeview arranca vacío; se completa en el Hito 3 con
datos.listar_clientes() / datos.buscar_clientes(texto). Guardar y
Eliminar están simulados, no persisten nada todavía.

Responsable: Leandro Piazza (Interfaz).
"""
import tkinter as tk
from tkinter import ttk, messagebox

from ui.widgets_comunes import campo_formulario, crear_treeview


COLUMNAS = [
    ("nombre", "Nombre", 120),
    ("apellido", "Apellido", 120),
    ("dni", "DNI", 90),
    ("telefono", "Teléfono", 100),
]

CAMPOS_FORMULARIO = (
    "entry_nombre",
    "entry_apellido",
    "entry_dni",
    "entry_telefono",
    "entry_direccion",
    "entry_mail",
    "entry_rol",
)


class AbmClientes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.cliente_seleccionado_id = None

        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True, padx=8, pady=8)
        contenedor.columnconfigure(0, weight=2)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self._armar_listado(contenedor)
        self._armar_formulario(contenedor)

    # --- Listado (izquierda) ---

    def _armar_listado(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        frame_busqueda = ttk.Frame(frame)
        frame_busqueda.pack(fill="x", pady=(0, 4))

        ttk.Label(frame_busqueda, text="Buscar:").pack(side="left")
        self.entry_busqueda = ttk.Entry(frame_busqueda)
        self.entry_busqueda.pack(side="left", fill="x", expand=True, padx=(4, 4))
        ttk.Button(frame_busqueda, text="Buscar", command=self._buscar).pack(side="left")

        contenedor_tree, self.tree = crear_treeview(frame, COLUMNAS)
        contenedor_tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_seleccionar)

    # --- Formulario (derecha) ---

    def _armar_formulario(self, parent):
        frame = ttk.LabelFrame(parent, text="Datos del cliente")
        frame.grid(row=0, column=1, sticky="nsew")

        self.entry_nombre = campo_formulario(frame, 0, "Nombre:")
        self.entry_apellido = campo_formulario(frame, 1, "Apellido:")
        self.entry_dni = campo_formulario(frame, 2, "DNI:")
        self.entry_telefono = campo_formulario(frame, 3, "Teléfono:")
        self.entry_direccion = campo_formulario(frame, 4, "Dirección:")
        self.entry_mail = campo_formulario(frame, 5, "Mail:")
        self.entry_rol = campo_formulario(frame, 6, "Rol:")

        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        ttk.Button(frame_botones, text="Nuevo", command=self._nuevo).pack(side="left")
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(
            side="left", padx=(4, 0)
        )
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar).pack(
            side="left", padx=(4, 0)
        )

    # --- Acciones (simuladas en Hito 2, sin persistencia real) ---

    def _buscar(self):
        # Hito 3: reemplazar por datos.buscar_clientes(self.entry_busqueda.get())
        messagebox.showinfo("Buscar", "Sin datos todavía: se completa en el Hito 3.")

    def _on_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        self.cliente_seleccionado_id = seleccion[0]
        # Hito 3: completar los entry con datos.obtener_cliente(id) acá.

    def _nuevo(self):
        self.cliente_seleccionado_id = None
        for nombre_campo in CAMPOS_FORMULARIO:
            getattr(self, nombre_campo).delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def _guardar(self):
        errores = self._validar()
        if errores:
            messagebox.showerror("Datos inválidos", "\n".join(errores))
            return

        # Hito 3: acá va datos.crear_cliente(...) / datos.actualizar_cliente(...)
        messagebox.showinfo(
            "Guardar cliente", "Cliente guardado (simulado, sin persistencia todavía)."
        )

    def _eliminar(self):
        if not self.cliente_seleccionado_id:
            messagebox.showwarning("Eliminar cliente", "Seleccioná un cliente de la lista.")
            return

        nombre = self.entry_nombre.get().strip() or "el cliente seleccionado"
        if messagebox.askyesno(
            "Eliminar cliente", f"¿Confirmás que querés eliminar a {nombre}?"
        ):
            # Hito 3: acá va datos.eliminar_cliente(self.cliente_seleccionado_id)
            self.tree.delete(self.cliente_seleccionado_id)
            self._nuevo()
            messagebox.showinfo("Eliminar cliente", "Cliente eliminado (simulado).")

    def _validar(self):
        """Validaciones mínimas de formulario.

        Hito 3: reemplazar por validaciones.py (Tomás) cuando esté
        disponible, para reutilizar la misma lógica en todos los ABM.
        """
        errores = []

        if not self.entry_nombre.get().strip():
            errores.append("El nombre es obligatorio.")
        if not self.entry_apellido.get().strip():
            errores.append("El apellido es obligatorio.")

        dni = self.entry_dni.get().strip()
        if not dni:
            errores.append("El DNI es obligatorio.")
        elif not dni.isdigit():
            errores.append("El DNI debe ser numérico.")

        return errores
