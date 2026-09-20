"""
ABM de servicios.

Mismo patrón que ui/abm_clientes.py: listado con búsqueda a la izquierda,
formulario a la derecha, botones Nuevo / Guardar / Eliminar.

Hito 2: solo interfaz visual, sin conexión a la base ni datos de prueba.
El Treeview arranca vacío; se completa en el Hito 3 con
datos.listar_servicios() / datos.buscar_servicios(texto). El combo de
tipo de servicio se completa en el Hito 3 con datos.listar_tipo_servicio().
Guardar y Eliminar están simulados, no persisten nada todavía.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from ui.widgets_comunes import campo_formulario, combo_formulario, crear_treeview


COLUMNAS = [
    ("nombre", "Nombre", 150),
    ("tipo_servicio", "Tipo", 120),
    ("duracion", "Duración (min)", 100),
    ("precio", "Precio", 90),
]


class AbmServicios(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.servicio_seleccionado_id = None

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
        frame = ttk.LabelFrame(parent, text="Datos del servicio")
        frame.grid(row=0, column=1, sticky="nsew")

        # Hito 3: values = [t["nombre"] for t in datos.listar_tipo_servicio()]
        self.combo_tipo_servicio = combo_formulario(frame, 0, "Tipo de servicio:", valores=[])

        self.entry_nombre = campo_formulario(frame, 1, "Nombre:")

        ttk.Label(frame, text="Descripción:").grid(row=2, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.text_descripcion = tk.Text(frame, height=3, width=25)
        self.text_descripcion.grid(row=2, column=1, sticky="ew", pady=4)

        self.entry_duracion = campo_formulario(frame, 3, "Duración (min):")
        self.entry_precio = campo_formulario(frame, 4, "Precio:")

        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        ttk.Button(frame_botones, text="Nuevo", command=self._nuevo).pack(side="left")
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(
            side="left", padx=(4, 0)
        )
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar).pack(
            side="left", padx=(4, 0)
        )

    # --- Acciones (simuladas en Hito 2, sin persistencia real) ---

    def _buscar(self):
        # Hito 3: reemplazar por datos.buscar_servicios(self.entry_busqueda.get())
        messagebox.showinfo("Buscar", "Sin datos todavía: se completa en el Hito 3.")

    def _on_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        self.servicio_seleccionado_id = seleccion[0]
        # Hito 3: completar los campos con datos.obtener_servicio(id) acá.

    def _nuevo(self):
        self.servicio_seleccionado_id = None
        self.combo_tipo_servicio.set("")
        self.entry_nombre.delete(0, tk.END)
        self.text_descripcion.delete("1.0", tk.END)
        self.entry_duracion.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def _guardar(self):
        errores = self._validar()
        if errores:
            messagebox.showerror("Datos inválidos", "\n".join(errores))
            return

        # Hito 3: acá va datos.crear_servicio(...) / datos.actualizar_servicio(...)
        messagebox.showinfo(
            "Guardar servicio", "Servicio guardado (simulado, sin persistencia todavía)."
        )

    def _eliminar(self):
        if not self.servicio_seleccionado_id:
            messagebox.showwarning("Eliminar servicio", "Seleccioná un servicio de la lista.")
            return

        nombre = self.entry_nombre.get().strip() or "el servicio seleccionado"
        if messagebox.askyesno(
            "Eliminar servicio", f"¿Confirmás que querés eliminar {nombre}?"
        ):
            # Hito 3: acá va datos.eliminar_servicio(self.servicio_seleccionado_id)
            self.tree.delete(self.servicio_seleccionado_id)
            self._nuevo()
            messagebox.showinfo("Eliminar servicio", "Servicio eliminado (simulado).")

    def _validar(self):
        """Validaciones mínimas de formulario.

        Hito 3: reemplazar por validaciones.py (Tomás) cuando esté
        disponible, para reutilizar la misma lógica en todos los ABM.
        """
        errores = []

        if not self.entry_nombre.get().strip():
            errores.append("El nombre es obligatorio.")
        if not self.combo_tipo_servicio.get().strip():
            errores.append("El tipo de servicio es obligatorio.")

        duracion = self.entry_duracion.get().strip()
        if not duracion:
            errores.append("La duración es obligatoria.")
        elif not duracion.isdigit() or int(duracion) <= 0:
            errores.append("La duración debe ser un número entero mayor a 0.")

        precio = self.entry_precio.get().strip()
        if not precio:
            errores.append("El precio es obligatorio.")
        else:
            try:
                if float(precio) < 0:
                    errores.append("El precio no puede ser negativo.")
            except ValueError:
                errores.append("El precio debe ser un número.")

        return errores
