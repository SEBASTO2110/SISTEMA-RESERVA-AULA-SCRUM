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
        # Título
        titulo = tk.Label(
        self.root,
        text="📋 SISTEMA DE RESERVAS",
        font=("Arial", 20, "bold"),
        bg=self.bg_color,
        fg="#2c3e50"
        )
        titulo.pack(pady=15)
    
        # Subtítulo
        subtitulo = tk.Label(
        self.root,
        text="de Salas y Aulas",
        font=("Arial", 12),
        bg=self.bg_color,
        fg="#7f8c8d"
        )
        subtitulo.pack(pady=5)
    
        # Separador
        separador = tk.Frame(self.root, height=2, bg="#bdc3c7")
        separador.pack(fill=tk.X, pady=15)
        # Frame de botones
        frame_botones = tk.Frame(self.root, bg=self.bg_color)
        frame_botones.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # BOTÓN 1: Registrar
        btn_registrar = tk.Button(
        frame_botones,
        text="➕ Registrar Nueva Reserva",
        font=("Arial", 11, "bold"),
        bg="#27ae60",
        fg="white",
        height=2,
        cursor="hand2",
        command=self.registrar_reserva
        )
        btn_registrar.pack(fill=tk.X, pady=8)
    
        # BOTÓN 2: Consultar
        btn_consultar = tk.Button(
        frame_botones,
        text="🔍 Consultar Reservas por Fecha",
        font=("Arial", 11, "bold"),
        bg="#3498db",
        fg="white",
        height=2,
        cursor="hand2",
        command=self.consultar_reservas
        )
        btn_consultar.pack(fill=tk.X, pady=8)
    
        # BOTÓN 3: Ver detalles
        btn_detalles = tk.Button(
        frame_botones,
        text="📄 Ver Detalles de Reserva",
        font=("Arial", 11, "bold"),
        bg="#9b59b6",
        fg="white",
        height=2,
        cursor="hand2",
        command=self.ver_detalles
        )
        btn_detalles.pack(fill=tk.X, pady=8)

        # BOTÓN 4: Modificar
        btn_modificar = tk.Button(
        frame_botones,
        text="✏️ Modificar Reserva",
        font=("Arial", 11, "bold"),
        bg="#f39c12",
        fg="white",
        height=2,
        cursor="hand2",
        command=self.modificar_reserva
        )
        btn_modificar.pack(fill=tk.X, pady=8)
    
        # BOTÓN 5: Cancelar
        btn_cancelar = tk.Button(
        frame_botones,
        text="❌ Cancelar Reserva",
        font=("Arial", 11, "bold"),
        bg="#e74c3c",
        fg="white",
        height=2,
        cursor="hand2",
        command=self.cancelar_reserva
        )
        btn_cancelar.pack(fill=tk.X, pady=8)
    
        # BOTÓN 6: Gestionar salas
        btn_salas = tk.Button(
        frame_botones,
        text="🏢 Gestionar Salas",
        font=("Arial", 11, "bold"),
        bg="#1abc9c",
        fg="white",
        height=2,
        cursor="hand2",
        command=self.gestionar_salas
        )
        btn_salas.pack(fill=tk.X, pady=8)

        # Frame inferior para botón Salir
        frame_inferior = tk.Frame(self.root, bg=self.bg_color)
        frame_inferior.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
        
        # BOTÓN Salir
        btn_salir = tk.Button(
        frame_inferior,
        text="🚪 Salir",
        font=("Arial", 11, "bold"),
        bg="#34495e",
        fg="white",
        height=2,
        cursor="hand2",
        command=self.salir,
        )
        btn_salir.pack(fill=tk.X)
    def registrar_reserva(self):
        """Abre la pantalla de registro de reserva"""
        messagebox.showinfo("En construcción", "Pantalla de Registro\n\nJunior está trabajando en esto")
    
    def consultar_reservas(self):
        """Abre la pantalla de consulta por fecha"""
        messagebox.showinfo("En construcción", "Pantalla de Consulta\n\nSantiago está trabajando en esto")
    
    def ver_detalles(self):
        """Abre la pantalla de detalles de una reserva"""
        messagebox.showinfo("En construcción", "Ver Detalles\n\nProximamente disponible")
    
    def modificar_reserva(self):
        """Abre la pantalla de modificación de reserva"""
        messagebox.showinfo("En construcción", "Modificar Reserva\n\nProximamente disponible")
    
    def cancelar_reserva(self):
        """Abre la pantalla de cancelación de reserva"""
        messagebox.showinfo("En construcción", "Cancelar Reserva\n\nSantiago está trabajando en esto")
    
    def gestionar_salas(self):
        """Abre la pantalla de gestión de salas"""
        messagebox.showinfo("Gestionar Salas", "Salas disponibles:\n\n  Aula 101 (30 personas)\n• Aula 102 (40 personas)\n• Sala de Juntas (15 personas)")
    
    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.root.quit()