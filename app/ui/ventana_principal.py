"""
Ventana principal: arma el Notebook con las pestañas de navegación.

App Tkinter conectada a PostgreSQL.
"""
import tkinter as tk
from tkinter import ttk, messagebox

import datos
from ui.abm_clientes import AbmClientes
from ui.abm_insumos import AbmInsumos
from ui.abm_profesionales import AbmProfesionales
from ui.abm_servicios import AbmServicios
from ui.agenda_turnos import AgendaTurnos
from ui.form_turno import FormTurno


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self._agregar_pestana_turnos()
        self._agregar_pestana_clientes()
        self._agregar_pestana_profesionales()
        self._agregar_pestana_servicios()
        self._agregar_pestana_insumos()

    def _agregar_pestana_turnos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Turnos")

        self.agenda = AgendaTurnos(
            frame, on_nuevo_turno=self._abrir_form_turno, on_editar_turno=self._abrir_form_turno
        )
        self.agenda.pack(fill="both", expand=True)

    def _agregar_pestana_clientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Clientes")

        abm = AbmClientes(frame)
        abm.pack(fill="both", expand=True)

    def _agregar_pestana_profesionales(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Profesionales")

        abm = AbmProfesionales(frame)
        abm.pack(fill="both", expand=True)

    def _agregar_pestana_servicios(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Servicios")

        abm = AbmServicios(frame)
        abm.pack(fill="both", expand=True)

    def _agregar_pestana_insumos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Insumos")

        abm = AbmInsumos(frame)
        abm.pack(fill="both", expand=True)

    def _abrir_form_turno(self, turno_id=None):
        """Abre el formulario de alta/edición de turno como ventana modal.

        turno_id: id del turno a editar, o None para dar de alta uno nuevo.
        """
        turno = None
        if turno_id is not None:
            try:
                turno = datos.obtener_turno(turno_id)
            except datos.ErrorBaseDeDatos as e:
                messagebox.showerror("Error de conexión", f"No se pudo leer el turno:\n{e}")
                return

        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo turno" if turno is None else "Editar turno")
        ventana.transient(self.root)
        ventana.grab_set()
        FormTurno(ventana, turno=turno, on_guardado=self.agenda._refrescar_listado)
