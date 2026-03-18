"""
Pantalla de Consulta de Reservas
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class PantallaConsulta:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Consultar Reservas")
        self.ventana.geometry("700x500")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4f8")
        self.ventana.grab_set()
        
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - 350
        y = (self.ventana.winfo_screenheight() // 2) - 250
        self.ventana.geometry(f"700x500+{x}+{y}")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título
        tk.Label(
            self.ventana,
            text="🔍 Consultar Reservas",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1a237e"
        ).pack(pady=(15, 5))
        
        tk.Label(
            self.ventana,
            text="Busca reservas por fecha",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#666"
        ).pack(pady=(0, 10))
        
        # Frame de búsqueda
        frame_busqueda = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_busqueda.pack(pady=10)
        
        tk.Label(frame_busqueda, text="Fecha (YYYY-MM-DD):", font=("Arial", 10, "bold"), bg="#f0f4f8").pack(side="left", padx=5)
        
        self.var_fecha = tk.StringVar()
        tk.Entry(frame_busqueda, textvariable=self.var_fecha, width=15, font=("Arial", 10)).pack(side="left", padx=5)
        
        tk.Button(frame_busqueda, text="🔍 Buscar", bg="#3498db", fg="white", 
                font=("Arial", 10, "bold"), command=self.buscar_reservas).pack(side="left", padx=5)
        
        # Frame para la tabla
        frame_tabla = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief="solid")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Columnas
        columnas = ("ID", "Sala", "Hora Inicio", "Hora Fin", "Responsable", "Descripción")
        
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Configurar columnas
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Sala", text="Sala")
        self.tabla.heading("Hora Inicio", text="Inicio")
        self.tabla.heading("Hora Fin", text="Fin")
        self.tabla.heading("Responsable", text="Responsable")
        self.tabla.heading("Descripción", text="Descripción")
        
        self.tabla.column("ID", width=30)
        self.tabla.column("Sala", width=100)
        self.tabla.column("Hora Inicio", width=80)
        self.tabla.column("Hora Fin", width=80)
        self.tabla.column("Responsable", width=100)
        self.tabla.column("Descripción", width=200)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame botones
        frame_botones = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="✖  Cerrar", bg="#95a5a6", fg="white", 
        font=("Arial", 11, "bold"), width=15, cursor="hand2", 
        relief="flat", command=self.ventana.destroy).pack(side="left", padx=10)
    
    def buscar_reservas(self):
        fecha = self.var_fecha.get().strip()
        
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        if not fecha:
            self.tabla.insert("", "end", values=("", "Ingresa una fecha", "", "", "", ""))
            return
        
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            self.tabla.insert("", "end", values=("", "Formato incorrecto (YYYY-MM-DD)", "", "", "", ""))
            return
        
        # Obtener reservas
        reservas = self.db.obtener_reservas_por_fecha(fecha)
        
        if not reservas:
            self.tabla.insert("", "end", values=("", "No hay reservas para esta fecha", "", "", "", ""))
        else:
            for reserva in reservas:
                self.tabla.insert("", "end", values=(
                    reserva['id'],
                    reserva['sala_nombre'],
                    reserva['hora_inicio'],
                    reserva['hora_fin'],
                    reserva['responsable'],
                    reserva['descripcion']
                ))