"""
Pantalla de Registro de Reservas
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
 
class PantallaRegistro:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Nueva Reserva")
        self.ventana.geometry("500x560")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4f8")
        self.ventana.grab_set()
        
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - 250
        y = (self.ventana.winfo_screenheight() // 2) - 280
        self.ventana.geometry(f"500x560+{x}+{y}")
        
        self.crear_formulario()
    
    def crear_formulario(self):
        tk.Label(
            self.ventana,
            text="📋 Nueva Reserva",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1a237e",
        ).pack(pady=(15, 5))
        
        tk.Label(
            self.ventana,
            text="Complete todos los campos para registrar una reserva",
            font=("Arial", 9),
            bg="#f0f4f8",
            fg="#666",
        ).pack(pady=(0, 10))
        
        frame = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief="solid", padx=25, pady=20)
        frame.pack(fill="both", expand=True, padx=20, pady=5)
        
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
            width=34,
            font=("Arial", 10),
        )
        self.combo_sala.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.salas_dict = {s['nombre']: s['id'] for s in salas}
        
        # Fecha
        tk.Label(frame, text="Fecha * (YYYY-MM-DD)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=2, column=0, sticky="w", pady=(8, 2))
        self.var_fecha = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_fecha, width=37,
                 font=("Arial", 10)).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        
        # Horas
        frame_horas = tk.Frame(frame, bg="#ffffff")
        frame_horas.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        
        tk.Label(frame_horas, text="Hora Inicio * (HH:MM)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10))
        tk.Label(frame_horas, text="Hora Fin * (HH:MM)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=1, sticky="w")
        
        self.var_hora_inicio = tk.StringVar()
        tk.Entry(frame_horas, textvariable=self.var_hora_inicio, width=17,
                 font=("Arial", 10)).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(2, 8))
        
        self.var_hora_fin = tk.StringVar()
        tk.Entry(frame_horas, textvariable=self.var_hora_fin, width=17,
                 font=("Arial", 10)).grid(row=1, column=1, sticky="ew", pady=(2, 8))
        
        # Responsable
        tk.Label(frame, text="Responsable *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=5, column=0, sticky="w", pady=(8, 2))
        self.var_responsable = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_responsable, width=37,
                 font=("Arial", 10)).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        
        # Descripción
        tk.Label(frame, text="Descripción *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=7, column=0, sticky="w", pady=(8, 2))
        self.txt_descripcion = tk.Text(frame, width=37, height=4, font=("Arial", 10))
        self.txt_descripcion.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        
        # Botones
        frame_botones = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_botones.pack(pady=15)
        
        tk.Button(
            frame_botones,
            text="💾  Guardar Reserva",
            bg="#2e7d32",
            fg="white",
            font=("Arial", 11, "bold"),
            width=18,
            cursor="hand2",
            relief="flat",
            command=self.guardar_reserva,
        ).pack(side="left", padx=10)
        
        tk.Button(
            frame_botones,
            text="✖  Cancelar",
            bg="#c62828",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12,
            cursor="hand2",
            relief="flat",
            command=self.ventana.destroy,
        ).pack(side="left", padx=10)
    
    def validar_formulario(self):
        sala = self.var_sala.get().strip()
        fecha = self.var_fecha.get().strip()
        hora_inicio = self.var_hora_inicio.get().strip()
        hora_fin = self.var_hora_fin.get().strip()
        responsable = self.var_responsable.get().strip()
        descripcion = self.txt_descripcion.get("1.0", "end").strip()
        
        if not all([sala, fecha, hora_inicio, hora_fin, responsable, descripcion]):
            messagebox.showerror(
                "Campo vacío",
                "❌ Completa todos los campos.\nNingún campo puede quedar vacío.",
                parent=self.ventana,
            )
            return False
        
        try:
            t_inicio = datetime.strptime(hora_inicio, "%H:%M")
            t_fin = datetime.strptime(hora_fin, "%H:%M")
        except ValueError:
            messagebox.showerror(
                "Formato incorrecto",
                "❌ Formato de hora incorrecto.\nUsa el formato HH:MM (ejemplo: 09:00)",
                parent=self.ventana,
            )
            return False
        
        if t_fin <= t_inicio:
            messagebox.showerror(
                "Error de horario",
                "❌ La hora fin debe ser mayor que la hora inicio.",
                parent=self.ventana,
            )
            return False
        
        sala_id = self.salas_dict[sala]
        if self.db.validar_solapamiento(sala_id, fecha, hora_inicio, hora_fin):
            messagebox.showerror(
                "Horario no disponible",
                f"❌ La sala '{sala}' ya tiene una reserva en ese horario.\n\nPor favor elige otro horario o sala.",
                parent=self.ventana,
            )
            return False
        
        return True
    
    def guardar_reserva(self):
        if self.validar_formulario():
            sala = self.var_sala.get().strip()
            fecha = self.var_fecha.get().strip()
            hora_inicio = self.var_hora_inicio.get().strip()
            hora_fin = self.var_hora_fin.get().strip()
            responsable = self.var_responsable.get().strip()
            descripcion = self.txt_descripcion.get("1.0", "end").strip()
            
            sala_id = self.salas_dict[sala]
            
            try:
                self.db.insertar_reserva(sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion)
                messagebox.showinfo(
                    "Reserva guardada",
                    f"✅ Reserva guardada exitosamente.\n\n"
                    f"Sala: {sala}\n"
                    f"Fecha: {fecha}\n"
                    f"Horario: {hora_inicio} - {hora_fin}\n"
                    f"Responsable: {responsable}",
                    parent=self.ventana,
                )
                self.limpiar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}", parent=self.ventana)
    
    def limpiar_formulario(self):
        self.var_sala.set("")
        self.var_fecha.set("")
        self.var_hora_inicio.set("")
        self.var_hora_fin.set("")
        self.var_responsable.set("")
        self.txt_descripcion.delete("1.0", "end")