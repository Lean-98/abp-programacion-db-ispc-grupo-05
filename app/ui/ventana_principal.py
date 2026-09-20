"""
Ventana principal: arma el Notebook con las pestañas de navegación.

Hito 2: la pantalla de Clientes ya está armada (ui/abm_clientes.py) como
patrón. Profesionales / Servicios / Insumos las construye Nicolás
replicando ese mismo esqueleto, y por ahora quedan como placeholders.
"""
import tkinter as tk
from tkinter import ttk

from ui.abm_clientes import AbmClientes
from ui.agenda_turnos import AgendaTurnos
from ui.form_turno import FormTurno


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self._agregar_pestana_turnos()
        self._agregar_pestana_clientes()
        self._agregar_pestana_placeholder("Profesionales")
        self._agregar_pestana_placeholder("Servicios")
        self._agregar_pestana_placeholder("Insumos")

    def _agregar_pestana_turnos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Turnos")

        agenda = AgendaTurnos(frame, on_nuevo_turno=self._abrir_form_turno)
        agenda.pack(fill="both", expand=True)

    def _agregar_pestana_clientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Clientes")

        abm = AbmClientes(frame)
        abm.pack(fill="both", expand=True)

    def _agregar_pestana_placeholder(self, nombre):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=nombre)
        ttk.Label(
            frame,
            text=f"Pantalla de {nombre} — en construcción",
            font=("TkDefaultFont", 12),
        ).pack(expand=True)

    def _abrir_form_turno(self, turno=None):
        """Abre el formulario de alta/edición de turno como ventana modal."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo turno" if turno is None else "Editar turno")
        ventana.transient(self.root)
        ventana.grab_set()
        FormTurno(ventana, turno=turno)
