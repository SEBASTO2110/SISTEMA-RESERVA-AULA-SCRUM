"""
Pantalla de Detalles de Reserva
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
 
class PantallaDetalles:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Ver Detalles de Reserva")
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
            text="📄 Ver Detalles de Reserva",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1a237e"
        ).pack(pady=(15, 5))
        
        tk.Label(
            self.ventana,
            text="Busca una reserva por ID o fecha",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#666"
        ).pack(pady=(0, 10))
        
        # Frame de búsqueda
        frame_busqueda = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_busqueda.pack(pady=10)
        
        tk.Label(frame_busqueda, text="Buscar por Fecha (YYYY-MM-DD):", font=("Arial", 10, "bold"), bg="#f0f4f8").pack(side="left", padx=5)
        
        self.var_fecha = tk.StringVar()
        tk.Entry(frame_busqueda, textvariable=self.var_fecha, width=15, font=("Arial", 10)).pack(side="left", padx=5)
        
        tk.Button(frame_busqueda, text="🔍 Buscar", bg="#3498db", fg="white", 
                 font=("Arial", 10, "bold"), command=self.cargar_reservas).pack(side="left", padx=5)
        
        # Frame para la tabla
        frame_tabla = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief="solid")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Columnas
        columnas = ("ID", "Sala", "Fecha", "Inicio", "Fin", "Responsable")
        
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.column("ID", width=40)
        self.tabla.column("Sala", width=100)
        self.tabla.column("Fecha", width=100)
        self.tabla.column("Inicio", width=80)
        self.tabla.column("Fin", width=80)
        self.tabla.column("Responsable", width=200)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind para mostrar detalles al hacer click
        self.tabla.bind("<Double-1>", lambda e: self.mostrar_detalles())
        
        # Frame botones
        frame_botones = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="📋 Ver Detalles Completos", bg="#9b59b6", fg="white", 
                 font=("Arial", 11, "bold"), width=20, cursor="hand2", 
                 relief="flat", command=self.mostrar_detalles).pack(side="left", padx=10)
        
        tk.Button(frame_botones, text="✖  Cerrar", bg="#95a5a6", fg="white", 
                 font=("Arial", 11, "bold"), width=12, cursor="hand2", 
                 relief="flat", command=self.ventana.destroy).pack(side="left", padx=10)
    
    def cargar_reservas(self):
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
                    reserva['fecha'],
                    reserva['hora_inicio'],
                    reserva['hora_fin'],
                    reserva['responsable']
                ))
    
    def mostrar_detalles(self):
        seleccion = self.tabla.selection()
        
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una reserva para ver detalles", parent=self.ventana)
            return
        
        valores = self.tabla.item(seleccion[0])["values"]
        id_reserva = valores[0]
        
        # Obtener detalles completos
        try:
            reserva = self.db.obtener_reserva_por_id(id_reserva)
            
            if reserva:
                mensaje = f"""
📋 DETALLES DE RESERVA
 
ID: {reserva['id']}
Sala: {reserva['sala_nombre']}
Fecha: {reserva['fecha']}
Hora Inicio: {reserva['hora_inicio']}
Hora Fin: {reserva['hora_fin']}
Responsable: {reserva['responsable']}
Descripción: {reserva['descripcion']}
Estado: {reserva['estado']}
Fecha Creación: {reserva['fecha_creacion']}
                """
                messagebox.showinfo("Detalles de Reserva", mensaje.strip(), parent=self.ventana)
            else:
                messagebox.showerror("Error", "No se encontró la reserva", parent=self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener detalles: {str(e)}", parent=self.ventana)