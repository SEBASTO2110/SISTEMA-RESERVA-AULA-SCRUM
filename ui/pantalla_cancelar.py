"""
Pantalla de Cancelación de Reservas
"""
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class PantallaCancelar:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Cancelar Reserva")
        self.ventana.geometry("600x500")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4f8")
        self.ventana.grab_set()
        
        # Centrar ventana
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - 300
        y = (self.ventana.winfo_screenheight() // 2) - 250
        self.ventana.geometry(f"600x500+{x}+{y}")
        
        self.crear_interfaz()
        self.cargar_reservas()
    
    def crear_interfaz(self):
        # Título
        tk.Label(
            self.ventana,
            text="❌ Cancelar Reserva",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1a237e"
        ).pack(pady=(15, 5))
        
        tk.Label(
            self.ventana,
            text="Selecciona una reserva para cancelarla",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#666"
        ).pack(pady=(0, 10))
        
        # Frame principal
        frame = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Campo: Buscar por fecha
        tk.Label(frame, text="Buscar reservas por fecha (YYYY-MM-DD):", 
                font=("Arial", 10, "bold"), bg="#ffffff", anchor="w").pack(fill="x", pady=(0, 5))
        
        self.var_fecha_busqueda = tk.StringVar()
        entry_fecha = tk.Entry(frame, textvariable=self.var_fecha_busqueda, width=40, font=("Arial", 10))
        entry_fecha.pack(fill="x", pady=(0, 10))
        
        tk.Button(frame, text="🔍 Buscar", bg="#3498db", fg="white", 
                 font=("Arial", 10, "bold"), command=self.cargar_reservas).pack(pady=(0, 10))
        
        # Tabla de reservas
        tk.Label(frame, text="Reservas disponibles:", font=("Arial", 10, "bold"), 
                bg="#ffffff", anchor="w").pack(fill="x", pady=(10, 5))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox = tk.Listbox(frame, font=("Arial", 9), height=12, yscrollcommand=scrollbar.set)
        self.listbox.pack(fill="both", expand=True, pady=(0, 10))
        scrollbar.config(command=self.listbox.yview)
        
        # Botones
        frame_botones = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_botones.pack(pady=15)
        
        tk.Button(
            frame_botones,
            text="🗑️  Cancelar Seleccionada",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            cursor="hand2",
            relief="flat",
            command=self.cancelar_reserva
        ).pack(side="left", padx=10)
        
        tk.Button(
            frame_botones,
            text="✖  Cerrar",
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12,
            cursor="hand2",
            relief="flat",
            command=self.ventana.destroy
        ).pack(side="left", padx=10)
    
    def cargar_reservas(self):
        """Carga las reservas de una fecha específica"""
        self.listbox.delete(0, "end")
        
        fecha = self.var_fecha_busqueda.get().strip()
        
        if not fecha:
            self.listbox.insert(0, "Ingresa una fecha para buscar")
            return
        
        try:
            # Validar formato de fecha
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            self.listbox.insert(0, "Formato incorrecto. Usa YYYY-MM-DD")
            return
        
        # Obtener reservas de la BD
        reservas = self.db.obtener_reservas_por_fecha(fecha)
        
        if not reservas:
            self.listbox.insert(0, "No hay reservas para esta fecha")
        else:
            for reserva in reservas:
                texto = f"ID: {reserva['id']} | Sala: {reserva['sala_nombre']} | {reserva['hora_inicio']} - {reserva['hora_fin']} | Responsable: {reserva['responsable']}"
                self.listbox.insert("end", texto)
    
    def cancelar_reserva(self):
        """Cancela la reserva seleccionada"""
        seleccion = self.listbox.curselection()
        
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una reserva para cancelar", parent=self.ventana)
            return
        
        # Obtener texto seleccionado y extraer ID
        texto_seleccionado = self.listbox.get(seleccion[0])
        try:
            id_reserva = int(texto_seleccionado.split("|")[0].replace("ID: ", "").strip())
        except:
            messagebox.showerror("Error", "No se pudo obtener el ID de la reserva", parent=self.ventana)
            return
        
        # Confirmar cancelación
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cancelar esta reserva?", parent=self.ventana):
            try:
                self.db.eliminar_reserva(id_reserva)
                messagebox.showinfo("Éxito", "✅ Reserva cancelada exitosamente", parent=self.ventana)
                self.cargar_reservas()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar: {str(e)}", parent=self.ventana)