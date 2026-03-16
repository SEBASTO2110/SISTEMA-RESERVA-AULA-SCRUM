"""
Interfaz principal del sistema
Menú con acceso a todas las funcionalidades
"""
import tkinter as tk
from tkinter import messagebox
from models.database import BaseDatos
from ui.pantalla_registro import PantallaRegistro
from ui.pantalla_consulta import PantallaConsulta

class VentanaMain:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas de Salas")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)

        self.db = BaseDatos()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        titulo = tk.Label(self.root, text="📋 SISTEMA DE RESERVAS", font=("Arial", 20, "bold"), bg=self.bg_color, fg="#2c3e50")
        titulo.pack(pady=15)
    
        subtitulo = tk.Label(self.root, text="de Salas y Aulas", font=("Arial", 12), bg=self.bg_color, fg="#7f8c8d")
        subtitulo.pack(pady=5)
    
        separador = tk.Frame(self.root, height=2, bg="#bdc3c7")
        separador.pack(fill=tk.X, pady=15)
        
        frame_botones = tk.Frame(self.root, bg=self.bg_color)
        frame_botones.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        btn_registrar = tk.Button(frame_botones, text="➕ Registrar Nueva Reserva", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", height=2, cursor="hand2", command=self.registrar_reserva)
        btn_registrar.pack(fill=tk.X, pady=8)
    
        btn_consultar = tk.Button(frame_botones, text="🔍 Consultar Reservas por Fecha", font=("Arial", 11, "bold"), bg="#3498db", fg="white", height=2, cursor="hand2", command=self.consultar_reservas)
        btn_consultar.pack(fill=tk.X, pady=8)
    
        btn_detalles = tk.Button(frame_botones, text="📄 Ver Detalles de Reserva", font=("Arial", 11, "bold"), bg="#9b59b6", fg="white", height=2, cursor="hand2", command=self.ver_detalles)
        btn_detalles.pack(fill=tk.X, pady=8)

        btn_modificar = tk.Button(frame_botones, text="✏️ Modificar Reserva", font=("Arial", 11, "bold"), bg="#f39c12", fg="white", height=2, cursor="hand2", command=self.modificar_reserva)
        btn_modificar.pack(fill=tk.X, pady=8)
    
        btn_cancelar = tk.Button(frame_botones, text="❌ Cancelar Reserva", font=("Arial", 11, "bold"), bg="#e74c3c", fg="white", height=2, cursor="hand2", command=self.cancelar_reserva)
        btn_cancelar.pack(fill=tk.X, pady=8)
    
        btn_salas = tk.Button(frame_botones, text="🏢 Gestionar Salas", font=("Arial", 11, "bold"), bg="#1abc9c", fg="white", height=2, cursor="hand2", command=self.gestionar_salas)
        btn_salas.pack(fill=tk.X, pady=8)

        frame_inferior = tk.Frame(self.root, bg=self.bg_color)
        frame_inferior.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
        
        btn_salir = tk.Button(frame_inferior, text="🚪 Salir", font=("Arial", 11, "bold"), bg="#34495e", fg="white", height=2, cursor="hand2", command=self.salir)
        btn_salir.pack(fill=tk.X)
    
    def registrar_reserva(self):
        """Abre la pantalla de registro de reserva"""
        ventana = tk.Toplevel(self.root)
        app = PantallaRegistro(ventana, self.db)
    
    def consultar_reservas(self):
        """Abre la pantalla de consulta por fecha"""
        ventana = tk.Toplevel(self.root)
        app = PantallaConsulta(ventana, self.db)
    
    def ver_detalles(self):
        """Abre la pantalla de detalles de una reserva"""
        messagebox.showinfo("En construcción", "Ver Detalles\n\nProximamente disponible")
    
    def modificar_reserva(self):
        """Abre la pantalla de modificación de reserva"""
        messagebox.showinfo("En construcción", "Modificar Reserva\n\nProximamente disponible")
    
    def cancelar_reserva(self):
        """Abre la pantalla de cancelación de reserva"""
        ventana = tk.Toplevel(self.root)
        app = PantallaCancelar(ventana, self.db)
    
    def gestionar_salas(self):
        """Abre la pantalla de gestión de salas"""
        salas = self.db.obtener_salas()
        mensaje = "Salas disponibles:\n\n"
        for sala in salas:
            mensaje += f"• {sala['nombre']} ({sala['capacidad']} personas)\n"
        messagebox.showinfo("Gestionar Salas", mensaje)
    
    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.root.quit()