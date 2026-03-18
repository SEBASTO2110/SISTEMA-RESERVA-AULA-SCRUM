"""
Sistema de Reservas de Salas
Punto de entrada de la aplicación
"""
import tkinter as tk
from ui.interfaz import DashboardModerno

def main():
    # Crear ventana principal
    root = tk.Tk()
    
    # Iniciar la aplicación con el nuevo dashboard
    app = DashboardModerno(root)
    
    # Iniciar el loop de eventos
    root.mainloop()

if __name__ == "__main__":
    main()