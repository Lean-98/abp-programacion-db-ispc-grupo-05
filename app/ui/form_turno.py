"""
Formulario de alta/edición de turno — conectado a PostgreSQL vía datos.py.

Sin validación de formulario a propósito: eso lo centraliza Tomás en
validaciones.py y se enchufa acá cuando esté listo. El único control que
queda es evitar que una fecha/hora/precio mal escritos rompan la
conversión antes de llegar a la base (no es una regla de negocio).

Responsable: Leandro Piazza (Interfaz).
"""
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

import datos
from ui.widgets_comunes import campo_formulario, combo_formulario, crear_treeview


# Estados posibles de un turno (valor de dominio fijo, no es mockdata de la app).
ESTADOS = ["pendiente", "confirmado", "completado", "cancelado"]

COLUMNAS_SERVICIOS_AGREGADOS = [
    ("nombre", "Servicio", 160),
    ("duracion", "Duración", 80),
    ("precio", "Precio", 80),
]


class FormTurno(ttk.Frame):
    def __init__(self, parent, turno=None, on_guardado=None):
        """
        parent: ventana (Toplevel) donde se embebe el formulario.
        turno: dict con los datos de un turno existente (edición, tal como
               lo devuelve datos.obtener_turno), o None (alta).
        on_guardado: callback opcional, se llama después de guardar con
               éxito (lo usa ventana_principal.py para refrescar la agenda).
        """
        super().__init__(parent)
        self.parent = parent
        self.turno = turno
        self.on_guardado = on_guardado

        # Catálogos para los combos: texto mostrado -> id real.
        self.clientes = {}
        self.profesionales = {}
        self.tipos_pago = {}
        self.servicios = {}  # texto mostrado -> fila completa (id, duracion, precio)
        self.servicios_por_id = {}

        self.pack(fill="both", expand=True, padx=12, pady=12)

        self._armar_datos_turno()
        self._armar_servicios()
        self._armar_botones()
        self._cargar_catalogos()

        if self.turno:
            self._cargar_turno(self.turno)

    def _armar_datos_turno(self):
        frame = ttk.LabelFrame(self, text="Datos del turno")
        frame.pack(fill="x", pady=(0, 8))

        self.combo_cliente = combo_formulario(frame, 0, "Cliente:", valores=[])
        self.combo_profesional = combo_formulario(frame, 1, "Profesional:", valores=[])
        self.combo_tipo_pago = combo_formulario(frame, 2, "Tipo de pago:", valores=[])

        self.entry_fecha = campo_formulario(frame, 3, "Fecha (DD/MM/AAAA):")
        self.entry_hora_inicio = campo_formulario(frame, 4, "Hora inicio (HH:MM):")
        self.entry_hora_fin = campo_formulario(frame, 5, "Hora fin (HH:MM):")

        self.combo_estado = combo_formulario(frame, 6, "Estado:", valores=ESTADOS)
        self.combo_estado.set(ESTADOS[0])

        self.entry_precio_final = campo_formulario(frame, 7, "Precio final:")

        ttk.Label(frame, text="Notas:").grid(row=8, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.text_notas = tk.Text(frame, height=3, width=30)
        self.text_notas.grid(row=8, column=1, sticky="ew", pady=4)

    def _armar_servicios(self):
        """Selector de servicios del turno (relación N a N vía turno_servicios)."""
        frame = ttk.LabelFrame(self, text="Servicios incluidos")
        frame.pack(fill="both", expand=True, pady=(0, 8))

        frame_agregar = ttk.Frame(frame)
        frame_agregar.pack(fill="x", padx=8, pady=8)

        ttk.Label(frame_agregar, text="Servicio:").pack(side="left")
        self.combo_servicio = ttk.Combobox(frame_agregar, values=[], state="readonly", width=25)
        self.combo_servicio.pack(side="left", padx=(4, 8))

        ttk.Button(frame_agregar, text="Agregar", command=self._agregar_servicio).pack(side="left")
        ttk.Button(
            frame_agregar, text="Quitar seleccionado", command=self._quitar_servicio
        ).pack(side="left", padx=(4, 0))

        contenedor, self.tree_servicios = crear_treeview(frame, COLUMNAS_SERVICIOS_AGREGADOS)
        contenedor.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _armar_botones(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x")

        ttk.Button(frame, text="Guardar", command=self._guardar).pack(side="right")
        ttk.Button(frame, text="Cancelar", command=self._cancelar).pack(side="right", padx=(0, 8))

    # --- Catálogos: traer datos reales para los combos ---

    def _cargar_catalogos(self):
        try:
            lista_clientes = datos.listar_clientes()
            lista_profesionales = datos.listar_profesionales()
            lista_tipos_pago = datos.listar_tipos_pago()
            lista_servicios = datos.listar_servicios()
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror(
                "Error de conexión", f"No se pudieron cargar los datos del formulario:\n{e}"
            )
            return

        # DNI entre paréntesis para no confundir clientes con el mismo nombre.
        self.clientes = {
            f"{c['nombre']} {c['apellido']} ({c['dni']})": c["id"] for c in lista_clientes
        }
        self.profesionales = {
            f"{p['nombre']} {p['apellido']}": p["id"] for p in lista_profesionales
        }
        self.tipos_pago = {t["nombre"]: t["id"] for t in lista_tipos_pago}
        self.servicios = {s["nombre"]: s for s in lista_servicios}
        self.servicios_por_id = {s["id"]: s for s in lista_servicios}

        self.combo_cliente["values"] = list(self.clientes.keys())
        self.combo_profesional["values"] = list(self.profesionales.keys())
        self.combo_tipo_pago["values"] = list(self.tipos_pago.keys())
        self.combo_servicio["values"] = list(self.servicios.keys())

    # --- Acciones ---

    def _agregar_servicio(self):
        nombre = self.combo_servicio.get()
        if not nombre:
            messagebox.showwarning("Agregar servicio", "Elegí un servicio de la lista.")
            return

        servicio = self.servicios.get(nombre)
        if servicio is None:
            return

        if str(servicio["id"]) in self.tree_servicios.get_children():
            messagebox.showwarning("Agregar servicio", "Ese servicio ya está agregado.")
            return

        self.tree_servicios.insert(
            "", "end", iid=str(servicio["id"]),
            values=(servicio["nombre"], servicio["duracion"], servicio["precio"]),
        )

    def _quitar_servicio(self):
        seleccion = self.tree_servicios.selection()
        if not seleccion:
            messagebox.showwarning("Quitar servicio", "Seleccioná un servicio de la lista.")
            return
        self.tree_servicios.delete(seleccion[0])

    def _cargar_turno(self, turno):
        """Completa el formulario con los datos de un turno existente (para editar)."""
        cliente_texto = next(
            (texto for texto, id_ in self.clientes.items() if id_ == turno["cliente_id"]), ""
        )
        profesional_texto = next(
            (texto for texto, id_ in self.profesionales.items() if id_ == turno["profesional_id"]),
            "",
        )
        tipo_pago_texto = next(
            (texto for texto, id_ in self.tipos_pago.items() if id_ == turno["tipo_pago_id"]), ""
        )

        self.combo_cliente.set(cliente_texto)
        self.combo_profesional.set(profesional_texto)
        self.combo_tipo_pago.set(tipo_pago_texto)

        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, turno["fecha"].strftime("%d/%m/%Y") if turno["fecha"] else "")
        self.entry_hora_inicio.delete(0, tk.END)
        self.entry_hora_inicio.insert(
            0, turno["hora_inicio"].strftime("%H:%M") if turno["hora_inicio"] else ""
        )
        self.entry_hora_fin.delete(0, tk.END)
        self.entry_hora_fin.insert(
            0, turno["hora_fin"].strftime("%H:%M") if turno["hora_fin"] else ""
        )

        self.combo_estado.set(turno["estado"])

        self.entry_precio_final.delete(0, tk.END)
        self.entry_precio_final.insert(
            0, str(turno["precio_final"]) if turno["precio_final"] is not None else ""
        )

        self.text_notas.delete("1.0", tk.END)
        self.text_notas.insert("1.0", turno["notas"] or "")

        self.tree_servicios.delete(*self.tree_servicios.get_children())
        for servicio_id in turno["servicios_ids"]:
            servicio = self.servicios_por_id.get(servicio_id)
            if servicio is None:
                continue
            self.tree_servicios.insert(
                "", "end", iid=str(servicio["id"]),
                values=(servicio["nombre"], servicio["duracion"], servicio["precio"]),
            )

    def _guardar(self):
        # Sin validación de formulario a propósito (ver docstring del
        # módulo) — acá se engancha validaciones.py cuando esté listo.
        cliente_id = self.clientes.get(self.combo_cliente.get())
        profesional_id = self.profesionales.get(self.combo_profesional.get())
        tipo_pago_id = self.tipos_pago.get(self.combo_tipo_pago.get())
        estado = self.combo_estado.get()
        notas = self.text_notas.get("1.0", tk.END).strip() or None
        precio_texto = self.entry_precio_final.get().strip()
        servicios_ids = [int(iid) for iid in self.tree_servicios.get_children()]

        fecha_texto = self.entry_fecha.get().strip()
        hora_inicio_texto = self.entry_hora_inicio.get().strip()
        hora_fin_texto = self.entry_hora_fin.get().strip()

        try:
            fecha = (
                datetime.strptime(f"{fecha_texto} {hora_inicio_texto}", "%d/%m/%Y %H:%M")
                if fecha_texto and hora_inicio_texto
                else None
            )
            hora_inicio = (
                datetime.strptime(hora_inicio_texto, "%H:%M").time() if hora_inicio_texto else None
            )
            hora_fin = (
                datetime.strptime(hora_fin_texto, "%H:%M").time() if hora_fin_texto else None
            )
            precio_final = float(precio_texto) if precio_texto else None
        except ValueError:
            messagebox.showerror(
                "Datos inválidos",
                "Revisá la fecha (DD/MM/AAAA), las horas (HH:MM) y el precio final.",
            )
            return

        try:
            if self.turno is None:
                datos.crear_turno(
                    cliente_id, profesional_id, tipo_pago_id, fecha,
                    hora_inicio, hora_fin, estado, notas, precio_final, servicios_ids,
                )
                mensaje = "Turno creado correctamente."
            else:
                datos.actualizar_turno(
                    self.turno["id"], cliente_id, profesional_id, tipo_pago_id, fecha,
                    hora_inicio, hora_fin, estado, notas, precio_final, servicios_ids,
                )
                mensaje = "Turno actualizado correctamente."
        except datos.ErrorBaseDeDatos as e:
            messagebox.showerror("No se pudo guardar", f"Error al guardar el turno:\n{e}")
            return

        messagebox.showinfo("Guardar turno", mensaje)
        if self.on_guardado:
            self.on_guardado()
        self.parent.destroy()

    def _cancelar(self):
        self.parent.destroy()
