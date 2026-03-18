"""
Pantalla de Modificación de Reservas
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
 
class PantallaModificar:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.reserva_actual = None
        self.salas_dict = {}
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Modificar Reserva")
        self.ventana.geometry("700x600")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4f8")
        self.ventana.grab_set()
        
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - 350
        y = (self.ventana.winfo_screenheight() // 2) - 300
        self.ventana.geometry(f"700x600+{x}+{y}")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título
        tk.Label(
            self.ventana,
            text="✏️ Modificar Reserva",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1a237e"
        ).pack(pady=(15, 5))
        
        tk.Label(
            self.ventana,
            text="Busca y modifica una reserva existente",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#666"
        ).pack(pady=(0, 10))
        
        # Frame de búsqueda
        frame_busqueda = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_busqueda.pack(pady=10)
        
        tk.Label(frame_busqueda, text="ID Reserva:", font=("Arial", 10, "bold"), bg="#f0f4f8").pack(side="left", padx=5)
        
        self.var_id = tk.StringVar()
        tk.Entry(frame_busqueda, textvariable=self.var_id, width=10, font=("Arial", 10)).pack(side="left", padx=5)
        
        tk.Button(frame_busqueda, text="🔍 Buscar", bg="#3498db", fg="white", 
                 font=("Arial", 10, "bold"), command=self.buscar_reserva).pack(side="left", padx=5)
        
        # Frame del formulario
        frame = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief="solid", padx=20, pady=20)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sala
        tk.Label(frame, text="Sala *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", pady=(8, 2))
        self.var_sala = tk.StringVar()
        salas = self.db.obtener_salas()
        salas_nombres = [s['nombre'] for s in salas]
        self.combo_sala = ttk.Combobox(
            frame,
            textvariable=self.var_sala,
            values=salas_nombres,
            state="readonly",
            width=40,
            font=("Arial", 10),
        )
        self.combo_sala.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.salas_dict = {s['nombre']: s['id'] for s in salas}
        
        # Fecha
        tk.Label(frame, text="Fecha * (YYYY-MM-DD)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=2, column=0, sticky="w", pady=(8, 2))
        self.var_fecha = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_fecha, width=43,
                 font=("Arial", 10)).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        
        # Horas
        frame_horas = tk.Frame(frame, bg="#ffffff")
        frame_horas.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        
        tk.Label(frame_horas, text="Hora Inicio * (HH:MM)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10))
        tk.Label(frame_horas, text="Hora Fin * (HH:MM)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=1, sticky="w")
        
        self.var_hora_inicio = tk.StringVar()
        tk.Entry(frame_horas, textvariable=self.var_hora_inicio, width=19,
                 font=("Arial", 10)).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(2, 8))
        
        self.var_hora_fin = tk.StringVar()
        tk.Entry(frame_horas, textvariable=self.var_hora_fin, width=19,
                 font=("Arial", 10)).grid(row=1, column=1, sticky="ew", pady=(2, 8))
        
        # Responsable
        tk.Label(frame, text="Responsable *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=5, column=0, sticky="w", pady=(8, 2))
        self.var_responsable = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_responsable, width=43,
                 font=("Arial", 10)).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        
        # Descripción
        tk.Label(frame, text="Descripción *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=7, column=0, sticky="w", pady=(8, 2))
        self.txt_descripcion = tk.Text(frame, width=43, height=4, font=("Arial", 10))
        self.txt_descripcion.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        
        # Botones
        frame_botones = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_botones.pack(pady=15)
        
        tk.Button(
            frame_botones,
            text="💾  Guardar Cambios",
            bg="#f39c12",
            fg="white",
            font=("Arial", 11, "bold"),
            width=18,
            cursor="hand2",
            relief="flat",
            command=self.guardar_cambios,
        ).pack(side="left", padx=10)
        
        tk.Button(
            frame_botones,
            text="✖  Cancelar",
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12,
            cursor="hand2",
            relief="flat",
            command=self.ventana.destroy,
        ).pack(side="left", padx=10)
    
    def buscar_reserva(self):
        id_reserva = self.var_id.get().strip()
        
        if not id_reserva:
            messagebox.showerror("Error", "Ingresa un ID de reserva", parent=self.ventana)
            return
        
        try:
            id_reserva = int(id_reserva)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número", parent=self.ventana)
            return
        
        try:
            reserva = self.db.obtener_reserva_por_id(id_reserva)
            
            if reserva:
                self.reserva_actual = reserva
                self.var_sala.set(reserva['sala_nombre'])
                self.var_fecha.set(reserva['fecha'])
                self.var_hora_inicio.set(reserva['hora_inicio'])
                self.var_hora_fin.set(reserva['hora_fin'])
                self.var_responsable.set(reserva['responsable'])
                self.txt_descripcion.delete("1.0", "end")
                self.txt_descripcion.insert("1.0", reserva['descripcion'])
                
                messagebox.showinfo("Éxito", "Reserva cargada. Modifica los campos y guarda.", parent=self.ventana)
            else:
                messagebox.showerror("Error", "No se encontró la reserva", parent=self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar: {str(e)}", parent=self.ventana)
    
    def validar_formulario(self):
        if not self.reserva_actual:
            messagebox.showerror("Error", "Busca una reserva primero", parent=self.ventana)
            return None
        
        sala = self.var_sala.get().strip()
        fecha = self.var_fecha.get().strip()
        hora_inicio = self.var_hora_inicio.get().strip()
        hora_fin = self.var_hora_fin.get().strip()
        responsable = self.var_responsable.get().strip()
        descripcion = self.txt_descripcion.get("1.0", "end").strip()
        
        if not all([sala, fecha, hora_inicio, hora_fin, responsable, descripcion]):
            messagebox.showerror("Error", "Completa todos los campos", parent=self.ventana)
            return None
        
        try:
            fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d").date()
            t_inicio = datetime.strptime(hora_inicio, "%H:%M")
            t_fin = datetime.strptime(hora_fin, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto", parent=self.ventana)
            return None
        
        if t_fin <= t_inicio:
            messagebox.showerror("Error", "La hora fin debe ser mayor que la hora inicio", parent=self.ventana)
            return None
        
        sala_id = self.salas_dict[sala]
        
        return {
            "sala_id": sala_id,
            "fecha": fecha,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "responsable": responsable,
            "descripcion": descripcion,
        }
    
    def guardar_cambios(self):
        datos = self.validar_formulario()
        if datos is None:
            return
        
        try:
            self.db.actualizar_reserva(
                self.reserva_actual['id'],
                datos["sala_id"],
                datos["fecha"],
                datos["hora_inicio"],
                datos["hora_fin"],
                datos["responsable"],
                datos["descripcion"]
            )
            
            messagebox.showinfo("Éxito", "✅ Reserva modificada exitosamente", parent=self.ventana)
            self.ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}", parent=self.ventana)