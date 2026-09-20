"""
Formulario de alta/edición de turno.

Hito 2: solo interfaz visual, sin conexión a la base ni datos de prueba.
Los combos de cliente / profesional / tipo de pago, y el combo de servicios,
quedan vacíos a propósito: se completan en el Hito 3 desde datos.py
(listar_clientes(), listar_profesionales(), listar_tipos_pago(),
listar_servicios()).

Responsable: Leandro Piazza (Interfaz).
"""
import tkinter as tk
from tkinter import ttk, messagebox

from ui.widgets_comunes import campo_formulario, combo_formulario, crear_treeview


# Estados posibles de un turno (valor de dominio fijo, no es mockdata de la app).
ESTADOS = ["pendiente", "confirmado", "completado", "cancelado"]

COLUMNAS_SERVICIOS_AGREGADOS = [
    ("nombre", "Servicio", 160),
    ("duracion", "Duración", 80),
    ("precio", "Precio", 80),
]


class FormTurno(ttk.Frame):
    def __init__(self, parent, turno=None):
        """
        parent: ventana (Toplevel) donde se embebe el formulario.
        turno: dict con los datos de un turno existente (edición), o None (alta).
        """
        super().__init__(parent)
        self.parent = parent
        self.turno = turno
        self.pack(fill="both", expand=True, padx=12, pady=12)

        self._armar_datos_turno()
        self._armar_servicios()
        self._armar_botones()

        if self.turno:
            self._cargar_turno(self.turno)

    def _armar_datos_turno(self):
        frame = ttk.LabelFrame(self, text="Datos del turno")
        frame.pack(fill="x", pady=(0, 8))

        # Hito 3: values = [f"{c['nombre']} {c['apellido']}" for c in datos.listar_clientes()]
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
        # Hito 3: values = [s["nombre"] for s in datos.listar_servicios()]
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

    # --- Acciones (simuladas en Hito 2, sin persistencia real) ---

    def _agregar_servicio(self):
        if not self.combo_servicio.get():
            messagebox.showwarning("Agregar servicio", "Elegí un servicio de la lista.")
            return
        # Hito 3: buscar el servicio elegido en datos.py (por nombre o id guardado
        # en un diccionario paralelo) e insertarlo en self.tree_servicios.
        messagebox.showinfo(
            "Agregar servicio", "Sin datos todavía: se completa en el Hito 3."
        )

    def _quitar_servicio(self):
        seleccion = self.tree_servicios.selection()
        if not seleccion:
            messagebox.showwarning("Quitar servicio", "Seleccioná un servicio de la lista.")
            return
        self.tree_servicios.delete(seleccion[0])

    def _cargar_turno(self, turno):
        """Completa el formulario con los datos de un turno existente (para editar)."""
        # Hito 3: turno es un dict devuelto por datos.py; acá se vuelcan sus valores
        # en cada combo/entry y se listan sus servicios en self.tree_servicios.
        pass

    def _guardar(self):
        # Hito 3: acá van las validaciones (validaciones.py) y el guardado real
        # vía datos.crear_turno(...) / datos.actualizar_turno(...).
        messagebox.showinfo(
            "Guardar turno", "Turno guardado (simulado, sin persistencia todavía)."
        )
        self.parent.destroy()

    def _cancelar(self):
        self.parent.destroy()
