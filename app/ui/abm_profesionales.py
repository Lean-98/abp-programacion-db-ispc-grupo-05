"""
ABM de profesionales.

Mismo patrón que ui/abm_clientes.py: listado con búsqueda a la izquierda,
formulario a la derecha, botones Nuevo / Guardar / Eliminar.

Hito 2: solo interfaz visual, sin conexión a la base ni datos de prueba.
El Treeview arranca vacío; se completa en el Hito 3 con
datos.listar_profesionales() / datos.buscar_profesionales(texto).
Guardar y Eliminar están simulados, no persisten nada todavía.
"""
import tkinter as tk
from tkinter import ttk, messagebox

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

    # --- Acciones (simuladas en Hito 2, sin persistencia real) ---

    def _buscar(self):
        # Hito 3: reemplazar por datos.buscar_profesionales(self.entry_busqueda.get())
        messagebox.showinfo("Buscar", "Sin datos todavía: se completa en el Hito 3.")

    def _on_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        self.profesional_seleccionado_id = seleccion[0]
        # Hito 3: completar los campos con datos.obtener_profesional(id) acá.

    def _nuevo(self):
        self.profesional_seleccionado_id = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_especialidad.delete(0, tk.END)
        self.var_activo.set(True)
        self.tree.selection_remove(self.tree.selection())

    def _guardar(self):
        errores = self._validar()
        if errores:
            messagebox.showerror("Datos inválidos", "\n".join(errores))
            return

        # Hito 3: acá va datos.crear_profesional(...) / datos.actualizar_profesional(...)
        messagebox.showinfo(
            "Guardar profesional",
            "Profesional guardado (simulado, sin persistencia todavía).",
        )

    def _eliminar(self):
        if not self.profesional_seleccionado_id:
            messagebox.showwarning(
                "Eliminar profesional", "Seleccioná un profesional de la lista."
            )
            return

        nombre = self.entry_nombre.get().strip() or "el profesional seleccionado"
        if messagebox.askyesno(
            "Eliminar profesional", f"¿Confirmás que querés eliminar a {nombre}?"
        ):
            # Hito 3: acá va datos.eliminar_profesional(self.profesional_seleccionado_id)
            self.tree.delete(self.profesional_seleccionado_id)
            self._nuevo()
            messagebox.showinfo("Eliminar profesional", "Profesional eliminado (simulado).")

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
