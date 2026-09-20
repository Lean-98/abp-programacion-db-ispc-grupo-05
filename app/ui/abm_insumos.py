"""
ABM de insumos.

Mismo patrón que ui/abm_clientes.py: listado con búsqueda a la izquierda,
formulario a la derecha, botones Nuevo / Guardar / Eliminar.

Hito 2: solo interfaz visual, sin conexión a la base ni datos de prueba.
El Treeview arranca vacío; se completa en el Hito 3 con
datos.listar_insumos() / datos.buscar_insumos(texto). El combo de tipo
de insumo se completa en el Hito 3 con datos.listar_tipo_insumo().
Guardar y Eliminar están simulados, no persisten nada todavía.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from ui.widgets_comunes import campo_formulario, combo_formulario, crear_treeview


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
        frame = ttk.LabelFrame(parent, text="Datos del insumo")
        frame.grid(row=0, column=1, sticky="nsew")

        # Hito 3: values = [t["nombre"] for t in datos.listar_tipo_insumo()]
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

    # --- Acciones (simuladas en Hito 2, sin persistencia real) ---

    def _buscar(self):
        # Hito 3: reemplazar por datos.buscar_insumos(self.entry_busqueda.get())
        messagebox.showinfo("Buscar", "Sin datos todavía: se completa en el Hito 3.")

    def _on_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        self.insumo_seleccionado_id = seleccion[0]
        # Hito 3: completar los campos con datos.obtener_insumo(id) acá.

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
        errores = self._validar()
        if errores:
            messagebox.showerror("Datos inválidos", "\n".join(errores))
            return

        # Hito 3: acá va datos.crear_insumo(...) / datos.actualizar_insumo(...)
        messagebox.showinfo(
            "Guardar insumo", "Insumo guardado (simulado, sin persistencia todavía)."
        )

    def _eliminar(self):
        if not self.insumo_seleccionado_id:
            messagebox.showwarning("Eliminar insumo", "Seleccioná un insumo de la lista.")
            return

        nombre = self.entry_nombre.get().strip() or "el insumo seleccionado"
        if messagebox.askyesno(
            "Eliminar insumo", f"¿Confirmás que querés eliminar {nombre}?"
        ):
            # Hito 3: acá va datos.eliminar_insumo(self.insumo_seleccionado_id)
            self.tree.delete(self.insumo_seleccionado_id)
            self._nuevo()
            messagebox.showinfo("Eliminar insumo", "Insumo eliminado (simulado).")

    def _validar(self):
        """Validaciones mínimas de formulario.

        Hito 3: reemplazar por validaciones.py (Tomás) cuando esté
        disponible, para reutilizar la misma lógica en todos los ABM.
        """
        errores = []

        if not self.entry_nombre.get().strip():
            errores.append("El nombre es obligatorio.")
        if not self.combo_tipo_insumo.get().strip():
            errores.append("El tipo de insumo es obligatorio.")

        precio = self.entry_precio.get().strip()
        if not precio:
            errores.append("El precio es obligatorio.")
        else:
            try:
                if float(precio) < 0:
                    errores.append("El precio no puede ser negativo.")
            except ValueError:
                errores.append("El precio debe ser un número.")

        stock = self.entry_stock.get().strip()
        if stock and (not stock.isdigit()):
            errores.append("El stock debe ser un número entero.")

        codigo_barra = self.entry_codigo_barra.get().strip()
        if codigo_barra and not codigo_barra.isdigit():
            errores.append("El código de barras debe ser numérico.")

        return errores
