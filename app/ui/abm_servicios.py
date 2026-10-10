"""
ABM de servicios — conectado a PostgreSQL vía datos.py.

Mismo patrón que ui/abm_clientes.py: listado con búsqueda a la izquierda,
formulario a la derecha, botones Nuevo / Guardar / Eliminar.

Sin validación de formulario a propósito: eso lo centraliza Tomás en
validaciones.py y se enchufa acá cuando esté listo. El único control que
queda es evitar que un texto no numérico en duración/precio rompa la
conversión antes de llegar a la base (no es una regla de negocio).

Responsable: Nicolás Rivero (Interfaz).
"""
import tkinter as tk
from tkinter import ttk, messagebox

import datos
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
        self.tipos_servicio = {}  # nombre -> id, para resolver el combo

        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True, padx=8, pady=8)
        contenedor.columnconfigure(0, weight=2)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self._armar_listado(contenedor)
        self._armar_formulario(contenedor)
        self._cargar_tipos_servicio()
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
        frame = ttk.LabelFrame(parent, text="Datos del servicio")
        frame.grid(row=0, column=1, sticky="nsew")

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

    # --- Catálogo y listado: traer datos reales ---

    def _cargar_tipos_servicio(self):
        try:
            tipos = datos.listar_tipo_servicio()
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror(
                "Error de conexión", f"No se pudieron cargar los tipos de servicio:\n{e}"
            )
            return
        self.tipos_servicio = {tipo["nombre"]: tipo["id"] for tipo in tipos}
        self.combo_tipo_servicio["values"] = list(self.tipos_servicio.keys())

    def _refrescar_listado(self, filas=None):
        self.tree.delete(*self.tree.get_children())
        try:
            if filas is None:
                filas = datos.listar_servicios()
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
                    fila["tipo_servicio"],
                    fila["duracion"] if fila["duracion"] is not None else "",
                    fila["precio"],
                ),
            )

    # --- Acciones (simuladas en Hito 2, sin persistencia real) ---

    def _buscar(self):
        texto = self.entry_busqueda.get().strip()
        try:
            filas = datos.buscar_servicios(texto) if texto else datos.listar_servicios()
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("Error de conexión", f"No se pudo buscar:\n{e}")
            return
        self._refrescar_listado(filas)

    def _on_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        servicio_id = int(seleccion[0])
        try:
            servicio = datos.obtener_servicio(servicio_id)
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("Error de conexión", f"No se pudo leer el servicio:\n{e}")
            return
        if servicio is None:
            return

        self.servicio_seleccionado_id = servicio_id
        self.combo_tipo_servicio.set(servicio["tipo_servicio"])
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, servicio["nombre"] or "")
        self.text_descripcion.delete("1.0", tk.END)
        self.text_descripcion.insert("1.0", servicio["descripcion"] or "")
        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, str(servicio["duracion"]) if servicio["duracion"] is not None else "")
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, str(servicio["precio"]) if servicio["precio"] is not None else "")

    def _nuevo(self):
        self.servicio_seleccionado_id = None
        self.combo_tipo_servicio.set("")
        self.entry_nombre.delete(0, tk.END)
        self.text_descripcion.delete("1.0", tk.END)
        self.entry_duracion.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def _guardar(self):
        # Sin validación de formulario a propósito (ver docstring del
        # módulo) — acá se engancha validaciones.py cuando esté listo.
        tipo_servicio_id = self.tipos_servicio.get(self.combo_tipo_servicio.get())
        nombre = self.entry_nombre.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip() or None
        duracion_texto = self.entry_duracion.get().strip()
        precio_texto = self.entry_precio.get().strip()

        try:
            duracion = int(duracion_texto) if duracion_texto else None
            precio = float(precio_texto) if precio_texto else None
        except ValueError:
            messagebox.showerror("Datos inválidos", "Duración y precio deben ser números.")
            return

        try:
            if self.servicio_seleccionado_id is None:
                datos.crear_servicio(tipo_servicio_id, nombre, descripcion, duracion, precio)
                mensaje = "Servicio creado correctamente."
            else:
                datos.actualizar_servicio(
                    self.servicio_seleccionado_id, tipo_servicio_id, nombre,
                    descripcion, duracion, precio,
                )
                mensaje = "Servicio actualizado correctamente."
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("No se pudo guardar", f"Error al guardar el servicio:\n{e}")
            return

        messagebox.showinfo("Guardar servicio", mensaje)
        self._nuevo()
        self._refrescar_listado()

    def _eliminar(self):
        if not self.servicio_seleccionado_id:
            messagebox.showwarning("Eliminar servicio", "Seleccioná un servicio de la lista.")
            return

        nombre = self.entry_nombre.get().strip() or "el servicio seleccionado"
        if not messagebox.askyesno(
            "Eliminar servicio", f"¿Confirmás que querés eliminar {nombre}?"
        ):
            return

        try:
            datos.eliminar_servicio(self.servicio_seleccionado_id)
        except datos.ErrorBaseDeDatos as e:
            if "foreign key" in str(e).lower():
                messagebox.showerror(
                    "No se pudo eliminar",
                    "Ese servicio está en uso (turnos o insumos asociados), no se puede eliminar.",
                )
            else:
                messagebox.showerror("No se pudo eliminar", f"Error al eliminar:\n{e}")
            return

        messagebox.showinfo("Eliminar servicio", "Servicio eliminado correctamente.")
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
