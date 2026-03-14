"""
Interfaz principal del sistema
Menú con acceso a todas las funcionalidades
"""
import tkinter as tk
from tkinter import messagebox

class VentanaMain:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas de Salas")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Colores
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea el menú principal con todos los botones"""
        # Por ahora solo estructura
        pass
    
    def registrar_reserva(self):
        """Abre la pantalla de registro de reserva"""
        messagebox.showinfo("En construcción", "Pantalla de Registro")
    
    def consultar_reservas(self):
        """Abre la pantalla de consulta por fecha"""
        messagebox.showinfo("En construcción", "Pantalla de Consulta")
    
    def ver_detalles(self):
        """Abre la pantalla de detalles de una reserva"""
        messagebox.showinfo("En construcción", "Ver Detalles")
    
    def modificar_reserva(self):
        """Abre la pantalla de modificación de reserva"""
        messagebox.showinfo("En construcción", "Modificar Reserva")
    
    def cancelar_reserva(self):
        """Abre la pantalla de cancelación de reserva"""
        messagebox.showinfo("En construcción", "Cancelar Reserva")
    
    def gestionar_salas(self):
        """Abre la pantalla de gestión de salas"""
        messagebox.showinfo("Gestionar Salas", "Gestión de salas")
    
    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.root.quit()