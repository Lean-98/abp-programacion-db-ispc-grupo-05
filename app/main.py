"""
Punto de entrada de la aplicación.

Hito 2: arma la interfaz gráfica navegable, sin conexión a la base de datos.
La conexión real y el acceso a datos se incorporan en el Hito 3.
"""
import tkinter as tk

from ui.ventana_principal import VentanaPrincipal


def main():
    root = tk.Tk()
    root.title("Turnero - Centro estética")
    root.geometry("1000x600")
    root.minsize(800, 500)

    VentanaPrincipal(root)

    root.mainloop()


if __name__ == "__main__":
    main()
