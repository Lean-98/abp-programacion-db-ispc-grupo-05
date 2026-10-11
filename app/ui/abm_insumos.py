"""
ABM de insumos — conectado a PostgreSQL vía datos.py.

Mismo patrón que ui/abm_clientes.py: listado con búsqueda a la izquierda,
formulario a la derecha, botones Nuevo / Guardar / Eliminar.

Validación de formulario centralizada en validaciones.py (Tomás). El
formato de la fecha se controla acá mismo (no es una regla de negocio,
es evitar que un texto mal escrito rompa la conversión).

Responsable: Nicolás Rivero (Interfaz).
"""
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

import datos
from ui.widgets_comunes import campo_formulario, combo_formulario, crear_treeview

from ui.validaciones import campo_obligatorio, numero_decimal_positivo, numero_entero_positivo, campo_numerico, validar_longitud_max

COLUMNAS = [
    ("nombre", "Nombre", 150),
    ("tipo_insumo", "Tipo", 120),
    ("stock", "Stock", 70),
    ("precio", "Precio", 90),
]


class AbmInsumos(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.insumo_seleccionado_id = None
        self.tipos_insumo = {}  # nombre -> id, para resolver el combo

        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True, padx=8, pady=8)
        contenedor.columnconfigure(0, weight=2)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self._armar_listado(contenedor)
        self._armar_formulario(contenedor)
        self._cargar_tipos_insumo()
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
        frame = ttk.LabelFrame(parent, text="Datos del insumo")
        frame.grid(row=0, column=1, sticky="nsew")

        self.combo_tipo_insumo = combo_formulario(frame, 0, "Tipo de insumo:", valores=[])

        self.entry_nombre = campo_formulario(frame, 1, "Nombre:")

        ttk.Label(frame, text="Descripción:").grid(row=2, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.text_descripcion = tk.Text(frame, height=3, width=25)
        self.text_descripcion.grid(row=2, column=1, sticky="ew", pady=4)

        self.entry_precio = campo_formulario(frame, 3, "Precio:")
        self.entry_codigo_barra = campo_formulario(frame, 4, "Código de barras:")
        self.entry_fecha_vencimiento = campo_formulario(frame, 5, "Vencimiento (DD/MM/AAAA):")
        self.entry_stock = campo_formulario(frame, 6, "Stock:")

        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        ttk.Button(frame_botones, text="Nuevo", command=self._nuevo).pack(side="left")
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(
            side="left", padx=(4, 0)
        )
        ttk.Button(frame_botones, text="Eliminar", command=self._eliminar).pack(
            side="left", padx=(4, 0)
        )

    # --- Catálogo y listado: traer datos reales ---
    
    def _cargar_tipos_insumo(self):
        try:
            tipos = datos.listar_tipo_insumo()
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror(
                "Error de conexión", f"No se pudieron cargar los tipos de insumo:\n{e}"
            )
            return
        self.tipos_insumo = {tipo["nombre"]: tipo["id"] for tipo in tipos}
        self.combo_tipo_insumo["values"] = list(self.tipos_insumo.keys())

    def _refrescar_listado(self, filas=None):
        self.tree.delete(*self.tree.get_children())
        try:
            if filas is None:
                filas = datos.listar_insumos()
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
                    fila["tipo_insumo"],
                    fila["stock"],
                    fila["precio"],
                ),
            )
    
    # --- Acciones ---

    def _buscar(self):
        texto = self.entry_busqueda.get().strip()
        try:
            filas = datos.buscar_insumos(texto) if texto else datos.listar_insumos()
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("Error de conexión", f"No se pudo buscar:\n{e}")
            return
        self._refrescar_listado(filas)

    def _on_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        insumo_id = int(seleccion[0])
        try:
            insumo = datos.obtener_insumo(insumo_id)
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("Error de conexión", f"No se pudo leer el insumo:\n{e}")
            return
        if insumo is None:
            return

        self.insumo_seleccionado_id = insumo_id
        self.combo_tipo_insumo.set(insumo["tipo_insumo"])
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, insumo["nombre"] or "")
        self.text_descripcion.delete("1.0", tk.END)
        self.text_descripcion.insert("1.0", insumo["descripcion"] or "")
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, str(insumo["precio"]) if insumo["precio"] is not None else "")
        self.entry_codigo_barra.delete(0, tk.END)
        self.entry_codigo_barra.insert(0, insumo["codigo_barra"] or "")
        self.entry_fecha_vencimiento.delete(0, tk.END)
        fecha = insumo["fecha_vencimiento"]
        self.entry_fecha_vencimiento.insert(0, fecha.strftime("%d/%m/%Y") if fecha else "")
        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, str(insumo["stock"]) if insumo["stock"] is not None else "")

    def _nuevo(self):
        self.insumo_seleccionado_id = None
        self.combo_tipo_insumo.set("")
        self.entry_nombre.delete(0, tk.END)
        self.text_descripcion.delete("1.0", tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_codigo_barra.delete(0, tk.END)
        self.entry_fecha_vencimiento.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def _guardar(self):
        errores = []

        try:
            campo_obligatorio(self.combo_tipo_insumo.get(), "Tipo de insumo")
        except ValueError as e:
            errores.append(f"• {e}")

        try:
            campo_obligatorio(self.entry_nombre.get(), "Nombre")
        except ValueError as e:
            errores.append(f"• {e}")

        try:
            validar_longitud_max(self.entry_nombre.get(), "Nombre", 50)
        except ValueError as e:
            errores.append(f"• {e}")

        # Código de barras es opcional (columna nullable en la base),
        # así que solo se valida si se cargó algo.
        codigo_barra_texto = self.entry_codigo_barra.get().strip()
        if codigo_barra_texto:
            try:
                campo_numerico(codigo_barra_texto, "Código de barra")
            except ValueError as e:
                errores.append(f"• {e}")

            try:
                validar_longitud_max(codigo_barra_texto, "Código de barra", 20)
            except ValueError as e:
                errores.append(f"• {e}")

        stock_validado = None
        try:
            stock_validado = numero_entero_positivo(self.entry_stock.get(), "Stock")
        except ValueError as e:
            errores.append(f"• {e}")

        precio_validado = None
        try:
            precio_validado = numero_decimal_positivo(self.entry_precio.get(), "Precio")
        except ValueError as e:
            errores.append(f"• {e}")

        fecha_texto = self.entry_fecha_vencimiento.get().strip()
        fecha_vencimiento = None
        if fecha_texto:
            try:
                fecha_vencimiento = datetime.strptime(fecha_texto, "%d/%m/%Y").date()
            except ValueError:
                errores.append("• La fecha de vencimiento debe tener el formato DD/MM/AAAA.")

        if errores:
            mensaje_final = "\n".join(errores)
            messagebox.showerror(
                "Errores en el formulario", f"Por favor, corregí lo siguiente:\n\n{mensaje_final}"
            )
            return

        tipo_insumo_id = self.tipos_insumo.get(self.combo_tipo_insumo.get())
        nombre = self.entry_nombre.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip() or None
        codigo_barra = codigo_barra_texto or None

        try:
            if self.insumo_seleccionado_id is None:
                datos.crear_insumo(
                    tipo_insumo_id, nombre, descripcion, precio_validado,
                    codigo_barra, fecha_vencimiento, stock_validado,
                )
                mensaje = "Insumo creado correctamente."
            else:
                datos.actualizar_insumo(
                    self.insumo_seleccionado_id, tipo_insumo_id, nombre, descripcion,
                    precio_validado, codigo_barra, fecha_vencimiento, stock_validado,
                )
                mensaje = "Insumo actualizado correctamente."
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("No se pudo guardar", f"Error al guardar el insumo:\n{e}")
            return

        messagebox.showinfo("Guardar insumo", mensaje)
        self._nuevo()
        self._refrescar_listado()

    def _eliminar(self):
        if not self.insumo_seleccionado_id:
            messagebox.showwarning("Eliminar insumo", "Seleccioná un insumo de la lista.")
            return

        nombre = self.entry_nombre.get().strip() or "el insumo seleccionado"
        if not messagebox.askyesno(
            "Eliminar insumo", f"¿Confirmás que querés eliminar {nombre}?"
        ):
            return

        try:
            datos.eliminar_insumo(self.insumo_seleccionado_id)
        except datos.ErrorBaseDeDatos as e:
            if "foreign key" in str(e).lower():
                messagebox.showerror(
                    "No se pudo eliminar",
                    "Ese insumo está en uso en algún servicio, no se puede eliminar.",
                )
            else:
                messagebox.showerror("No se pudo eliminar", f"Error al eliminar:\n{e}")
            return

        messagebox.showinfo("Eliminar insumo", "Insumo eliminado correctamente.")
        self._nuevo()
        self._refrescar_listado()
