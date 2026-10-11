"""
ABM de clientes — conectado a PostgreSQL vía datos.py.

Esta es la pantalla patrón: listado con búsqueda a la izquierda,
formulario a la derecha, botones Nuevo / Guardar / Eliminar. Sirve de
modelo para las pantallas de Profesionales, Servicios e Insumos (mismo
esqueleto, cambiando columnas y campos).

Sin validación de formulario a propósito: eso lo centraliza Tomás en
validaciones.py y se enchufa acá cuando esté listo (ver _guardar).

Responsable: Leandro Piazza (Interfaz).
"""
import tkinter as tk
from tkinter import ttk, messagebox

import datos
from ui.widgets_comunes import campo_formulario, crear_treeview

from ui.validaciones import campo_obligatorio, campo_numerico, validar_longitud_max


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

    # --- Listado: traer datos reales ---

    def _refrescar_listado(self, filas=None):
        """Vuelve a llenar el Treeview. Si no le pasan filas, trae todos
        los clientes de la base."""
        self.tree.delete(*self.tree.get_children())
        try:
            if filas is None:
                filas = datos.listar_clientes()
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
                    fila["dni"],
                    fila["telefono"] or "",
                ),
            )

    # --- Acciones ---

    def _buscar(self):
        texto = self.entry_busqueda.get().strip()
        try:
            filas = datos.buscar_clientes(texto) if texto else datos.listar_clientes()
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("Error de conexión", f"No se pudo buscar:\n{e}")
            return
        self._refrescar_listado(filas)

    def _on_seleccionar(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        cliente_id = int(seleccion[0])
        try:
            cliente = datos.obtener_cliente(cliente_id)
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("Error de conexión", f"No se pudo leer el cliente:\n{e}")
            return
        if cliente is None:
            return

        self.cliente_seleccionado_id = cliente_id
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, cliente["nombre"] or "")
        self.entry_apellido.delete(0, tk.END)
        self.entry_apellido.insert(0, cliente["apellido"] or "")
        self.entry_dni.delete(0, tk.END)
        self.entry_dni.insert(0, cliente["dni"] or "")
        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, cliente["telefono"] or "")
        self.entry_direccion.delete(0, tk.END)
        self.entry_direccion.insert(0, cliente["direccion"] or "")
        self.entry_mail.delete(0, tk.END)
        self.entry_mail.insert(0, cliente["mail"] or "")
        self.entry_rol.delete(0, tk.END)
        self.entry_rol.insert(0, cliente["rol"] or "")

    def _nuevo(self):
        self.cliente_seleccionado_id = None
        for nombre_campo in CAMPOS_FORMULARIO:
            getattr(self, nombre_campo).delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        dni = self.entry_dni.get().strip()
        telefono = self.entry_telefono.get().strip() or None
        direccion = self.entry_direccion.get().strip() or None
        mail = self.entry_mail.get().strip() or None
        rol = self.entry_rol.get().strip() or None

        errores = []
                
        try:
            campo_obligatorio(self.entry_nombre.get(), "Nombre")
        except ValueError as e:
            errores.append(f"• {e}")
        
        try:
            validar_longitud_max(self.entry_nombre.get(), "Nombre", 50)
        except ValueError as e:
            errores.append(f"• {e}")  
                
        try:
            campo_obligatorio(self.entry_apellido.get(), "Apellido")
        except ValueError as e:
            errores.append(f"• {e}")
        
        try:
            validar_longitud_max(self.entry_apellido.get(), "Apellido", 50)
        except ValueError as e:
            errores.append(f"• {e}")  
        
        try:
            campo_obligatorio(self.entry_dni.get(), "Dni")
        except ValueError as e:
            errores.append(f"• {e}")
        
        try:
            validar_longitud_max(self.entry_dni.get(), "Dni", 10)
        except ValueError as e:
            errores.append(f"• {e}")  
        
        try:
            campo_numerico(self.entry_dni.get(), "Dni")
        except ValueError as e:
            errores.append(f"• {e}")
                
        
        if errores:
                mensaje_final = "\n".join(errores)
                messagebox.showerror("Errores en el Formulario", f"Por favor, corrige lo siguiente:\n\n{mensaje_final}")
                return
        

        try:
            if self.cliente_seleccionado_id is None:
                datos.crear_cliente(nombre, apellido, dni, telefono, direccion, mail, rol)
                mensaje = "Cliente creado correctamente."
            else:
                datos.actualizar_cliente(
                    self.cliente_seleccionado_id, nombre, apellido, dni,
                    telefono, direccion, mail, rol,
                )
                mensaje = "Cliente actualizado correctamente."
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("No se pudo guardar", f"Error al guardar el cliente:\n{e}")
            return

        
        messagebox.showinfo("Guardar cliente", mensaje)
        self._nuevo()
        self._refrescar_listado()

    def _eliminar(self):
        if not self.cliente_seleccionado_id:
            messagebox.showwarning("Eliminar cliente", "Seleccioná un cliente de la lista.")
            return

        nombre = self.entry_nombre.get().strip() or "el cliente seleccionado"
        if not messagebox.askyesno(
            "Eliminar cliente", f"¿Confirmás que querés eliminar a {nombre}?"
        ):
            return

        try:
            datos.eliminar_cliente(self.cliente_seleccionado_id)
        except datos.ErrorBaseDeDatos as e:
            # ON DELETE RESTRICT: no se puede borrar un cliente con turnos
            # asociados. Mismo patrón reutilizable para los demás ABM.
            if "foreign key" in str(e).lower():
                messagebox.showerror(
                    "No se pudo eliminar",
                    "Ese cliente tiene turnos asociados, no se puede eliminar.",
                )
            else:
                messagebox.showerror("No se pudo eliminar", f"Error al eliminar:\n{e}")
            return

        messagebox.showinfo("Eliminar cliente", "Cliente eliminado correctamente.")
        self._nuevo()
        self._refrescar_listado()
