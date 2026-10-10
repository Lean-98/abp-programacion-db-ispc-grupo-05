"""
ABM de profesionales — conectado a PostgreSQL vía datos.py.

Mismo patrón que ui/abm_clientes.py: listado con búsqueda a la izquierda,
formulario a la derecha, botones Nuevo / Guardar / Eliminar.

Sin validación de formulario a propósito: eso lo centraliza Tomás en
validaciones.py y se enchufa acá cuando esté listo.

Responsable: Nicolás Rivero (Interfaz).
"""
import tkinter as tk
from tkinter import ttk, messagebox

import datos
from ui.widgets_comunes import campo_formulario, crear_treeview


COLUMNAS = [
    ("nombre", "Nombre", 130),
    ("apellido", "Apellido", 130),
    ("especialidad", "Especialidad", 140),
    ("activo", "Activo", 70),
]


class AbmProfesionales(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.profesional_seleccionado_id = None

        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True, padx=8, pady=8)
        contenedor.columnconfigure(0, weight=2)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self._armar_listado(contenedor)
        self._armar_formulario(contenedor)
        self._refrescar_listado()

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
        frame = ttk.LabelFrame(parent, text="Datos del profesional")
        frame.grid(row=0, column=1, sticky="nsew")

        self.entry_nombre = campo_formulario(frame, 0, "Nombre:")
        self.entry_apellido = campo_formulario(frame, 1, "Apellido:")
        self.entry_especialidad = campo_formulario(frame, 2, "Especialidad:")

        self.var_activo = tk.BooleanVar(value=True)
        self.check_activo = campo_formulario(
            frame, 3, "Activo:", widget_factory=ttk.Checkbutton, variable=self.var_activo
        )

        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        ttk.Button(frame_botones, text="Nuevo", command=self._nuevo).pack(side="left")
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(
            side="left", padx=(4, 0)
        )
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar).pack(
            side="left", padx=(4, 0)
        )

    # --- Listado: traer datos reales ---

    def _refrescar_listado(self, filas=None):
        self.tree.delete(*self.tree.get_children())
        try:
            if filas is None:
                filas = datos.listar_profesionales()
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror(
                "Error de conexión", f"No se pudo conectar a la base de datos:\n{e}"
            )
            return

        for fila in filas:
            self.tree.insert(
                "", "end", iid=str(fila["id"]),
                values=(
                    fila["nombre"],
                    fila["apellido"],
                    fila["especialidad"] or "",
                    "Sí" if fila["activo"] else "No",
                ),
            )

    # --- Acciones ---

    def _buscar(self):
        texto = self.entry_busqueda.get().strip()
        try:
            filas = datos.buscar_profesionales(texto) if texto else datos.listar_profesionales()
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("Error de conexión", f"No se pudo buscar:\n{e}")
            return
        self._refrescar_listado(filas)

    def _on_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        profesional_id = int(seleccion[0])
        try:
            profesional = datos.obtener_profesional(profesional_id)
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("Error de conexión", f"No se pudo leer el profesional:\n{e}")
            return
        if profesional is None:
            return

        self.profesional_seleccionado_id = profesional_id
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, profesional["nombre"] or "")
        self.entry_apellido.delete(0, tk.END)
        self.entry_apellido.insert(0, profesional["apellido"] or "")
        self.entry_especialidad.delete(0, tk.END)
        self.entry_especialidad.insert(0, profesional["especialidad"] or "")
        self.var_activo.set(bool(profesional["activo"]))

    def _nuevo(self):
        self.profesional_seleccionado_id = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_especialidad.delete(0, tk.END)
        self.var_activo.set(True)
        self.tree.selection_remove(self.tree.selection())

    def _guardar(self):
        # Sin validación de formulario a propósito (ver docstring del
        # módulo) — acá se engancha validaciones.py cuando esté listo.
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        especialidad = self.entry_especialidad.get().strip() or None
        activo = self.var_activo.get()

        try:
            if self.profesional_seleccionado_id is None:
                datos.crear_profesional(nombre, apellido, especialidad, activo)
                mensaje = "Profesional creado correctamente."
            else:
                datos.actualizar_profesional(
                    self.profesional_seleccionado_id, nombre, apellido, especialidad, activo,
                )
                mensaje = "Profesional actualizado correctamente."
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("No se pudo guardar", f"Error al guardar el profesional:\n{e}")
            return

        messagebox.showinfo("Guardar profesional", mensaje)
        self._nuevo()
        self._refrescar_listado()

    def _eliminar(self):
        if not self.profesional_seleccionado_id:
            messagebox.showwarning(
                "Eliminar profesional", "Seleccioná un profesional de la lista."
            )
            return

        nombre = self.entry_nombre.get().strip() or "el profesional seleccionado"
        if not messagebox.askyesno(
            "Eliminar profesional", f"¿Confirmás que querés eliminar a {nombre}?"
        ):
            return

        try:
            datos.eliminar_profesional(self.profesional_seleccionado_id)
        except datos.ErrorBaseDeDatos as e:
            if "foreign key" in str(e).lower():
                messagebox.showerror(
                    "No se pudo eliminar",
                    "Ese profesional tiene turnos asociados, no se puede eliminar.",
                )
            else:
                messagebox.showerror("No se pudo eliminar", f"Error al eliminar:\n{e}")
            return

        messagebox.showinfo("Eliminar profesional", "Profesional eliminado correctamente.")
        self._nuevo()
        self._refrescar_listado()

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

        return errores
