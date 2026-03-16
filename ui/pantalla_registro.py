import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# ============================================================
#  IMPORTAR BASE DE DATOS REAL
# ============================================================
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import (
    crear_tablas,
    insertar_salas_prueba,
    obtener_salas,
    insertar_reserva,
    validar_solapamiento,
)

# Inicializar BD al arrancar
crear_tablas()
insertar_salas_prueba()


# ============================================================
#  HELPERS
# ============================================================

def cargar_salas_desde_bd():
    """Retorna lista de tuplas (id, nombre) solo de salas disponibles."""
    try:
        filas = obtener_salas()
        return [(fila[0], fila[1]) for fila in filas if fila[3]]
    except Exception as e:
        print(f"[ERROR] No se pudieron cargar salas: {e}")
        return []


# ============================================================
#  CLASE PRINCIPAL
# ============================================================

class PantallaRegistro:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.mapa_salas = {}  # {nombre_sala: id_sala}

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Nueva Reserva")
        self.ventana.geometry("500x580")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4f8")
        self.ventana.grab_set()

        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - 250
        y = (self.ventana.winfo_screenheight() // 2) - 290
        self.ventana.geometry(f"500x580+{x}+{y}")

        self.crear_formulario()
        self.cargar_salas()

    # ----------------------------------------------------------
    #  CARGAR SALAS REALES DESDE BD
    # ----------------------------------------------------------

    def cargar_salas(self):
        salas = cargar_salas_desde_bd()

        if not salas:
            messagebox.showwarning(
                "Sin salas",
                "No se encontraron salas en la base de datos.",
                parent=self.ventana,
            )
            return

        nombres = []
        for sala_id, sala_nombre in salas:
            self.mapa_salas[sala_nombre] = sala_id
            nombres.append(sala_nombre)

        self.combo_sala["values"] = nombres
        print(f"[BD] Salas cargadas: {nombres}")

    # ----------------------------------------------------------
    #  CREAR FORMULARIO
    # ----------------------------------------------------------

    def crear_formulario(self):
        tk.Label(
            self.ventana,
            text="📋 Nueva Reserva",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1a237e",
        ).pack(pady=(15, 3))

        tk.Label(
            self.ventana,
            text="Complete todos los campos para registrar una reserva",
            font=("Arial", 9),
            bg="#f0f4f8",
            fg="#666",
        ).pack(pady=(0, 8))

        frame = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief="solid", padx=25, pady=15)
        frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Campo 1: Sala
        tk.Label(frame, text="Sala *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", pady=(6, 2))
        self.var_sala = tk.StringVar()
        self.combo_sala = ttk.Combobox(
            frame, textvariable=self.var_sala, values=[],
            state="readonly", width=34, font=("Arial", 10))
        self.combo_sala.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        # Campo 2: Fecha
        tk.Label(frame, text="Fecha * (YYYY-MM-DD)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=2, column=0, sticky="w", pady=(6, 2))
        self.var_fecha = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_fecha, width=37,
                 font=("Arial", 10)).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        # Campos 3 y 4: Horas
        frame_horas = tk.Frame(frame, bg="#ffffff")
        frame_horas.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        tk.Label(frame_horas, text="Hora Inicio * (HH:MM)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10))
        tk.Label(frame_horas, text="Hora Fin * (HH:MM)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=1, sticky="w")

        self.var_hora_inicio = tk.StringVar()
        tk.Entry(frame_horas, textvariable=self.var_hora_inicio, width=17,
                 font=("Arial", 10)).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(2, 6))

        self.var_hora_fin = tk.StringVar()
        tk.Entry(frame_horas, textvariable=self.var_hora_fin, width=17,
                 font=("Arial", 10)).grid(row=1, column=1, sticky="ew", pady=(2, 6))

        # Campo 5: Responsable
        tk.Label(frame, text="Responsable *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=5, column=0, sticky="w", pady=(6, 2))
        self.var_responsable = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_responsable, width=37,
                 font=("Arial", 10)).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        # Campo 6: Descripción
        tk.Label(frame, text="Descripción *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=7, column=0, sticky="w", pady=(6, 2))
        self.txt_descripcion = tk.Text(frame, width=37, height=4, font=("Arial", 10))
        self.txt_descripcion.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        # Botones
        frame_botones = tk.Frame(self.ventana, bg="#f0f4f8")
        frame_botones.pack(pady=12)

        tk.Button(
            frame_botones, text="💾  Guardar Reserva",
            bg="#2e7d32", fg="white", font=("Arial", 11, "bold"),
            width=18, cursor="hand2", relief="flat",
            command=self.guardar_reserva,
        ).pack(side="left", padx=10)

        tk.Button(
            frame_botones, text="✖  Cancelar",
            bg="#c62828", fg="white", font=("Arial", 11, "bold"),
            width=12, cursor="hand2", relief="flat",
            command=self.cancelar,
        ).pack(side="left", padx=10)

    # ----------------------------------------------------------
    #  VALIDACIONES
    # ----------------------------------------------------------

    def validar_formulario(self):
        sala_nombre = self.var_sala.get().strip()
        fecha       = self.var_fecha.get().strip()
        hora_inicio = self.var_hora_inicio.get().strip()
        hora_fin    = self.var_hora_fin.get().strip()
        responsable = self.var_responsable.get().strip()
        descripcion = self.txt_descripcion.get("1.0", "end").strip()

        # Validación 1: Campos vacíos
        if not all([sala_nombre, fecha, hora_inicio, hora_fin, responsable, descripcion]):
            messagebox.showerror("Campo vacío",
                "❌ Completa todos los campos.\nNingún campo puede quedar vacío.",
                parent=self.ventana)
            return None

        # Validación 2: Formato de hora correcto (HH:MM)
        try:
            t_inicio = datetime.strptime(hora_inicio, "%H:%M")
            t_fin    = datetime.strptime(hora_fin,    "%H:%M")
        except ValueError:
            messagebox.showerror("Formato incorrecto",
                "❌ Formato de hora incorrecto.\nUsa el formato HH:MM  (ejemplo: 09:00)",
                parent=self.ventana)
            return None

        # Validación 3: Hora fin mayor que hora inicio
        if t_fin <= t_inicio:
            messagebox.showerror("Error de horario",
                "❌ La hora fin debe ser mayor que la hora inicio.",
                parent=self.ventana)
            return None

        # Obtener ID de la sala seleccionada
        sala_id = self.mapa_salas.get(sala_nombre)
        if not sala_id:
            messagebox.showerror("Error de sala",
                "❌ No se pudo identificar la sala seleccionada.\n"
                "Intenta cerrar y volver a abrir la pantalla.",
                parent=self.ventana)
            return None

        # Validación 4: Solapamiento con BD real
        try:
            hay_conflicto = validar_solapamiento(sala_id, fecha, hora_inicio, hora_fin)
            if hay_conflicto:
                messagebox.showerror("Horario no disponible",
                    f"❌ La sala '{sala_nombre}' ya tiene una reserva\n"
                    f"en ese horario el día {fecha}.\n\n"
                    f"Por favor elige otro horario o sala.",
                    parent=self.ventana)
                return None
        except Exception as e:
            messagebox.showerror("Error de BD",
                f"❌ Error al verificar disponibilidad:\n{e}",
                parent=self.ventana)
            return None

        # Todo OK — retorna datos listos para guardar
        return {
            "sala_id":     sala_id,
            "sala_nombre": sala_nombre,
            "fecha":       fecha,
            "hora_inicio": hora_inicio,
            "hora_fin":    hora_fin,
            "responsable": responsable,
            "descripcion": descripcion,
        }

    # ----------------------------------------------------------
    #  GUARDAR EN BD REAL
    # ----------------------------------------------------------

    def guardar_reserva(self):
        datos = self.validar_formulario()
        if datos is None:
            return

        try:
            nuevo_id = insertar_reserva(
                datos["sala_id"],
                datos["fecha"],
                datos["hora_inicio"],
                datos["hora_fin"],
                datos["responsable"],
                datos["descripcion"],
            )
            print(f"[BD] Reserva guardada con ID: {nuevo_id}")

            messagebox.showinfo("✅ Reserva guardada",
                f"Reserva registrada exitosamente.\n\n"
                f"ID: {nuevo_id}\n"
                f"Sala: {datos['sala_nombre']}\n"
                f"Fecha: {datos['fecha']}\n"
                f"Horario: {datos['hora_inicio']} - {datos['hora_fin']}\n"
                f"Responsable: {datos['responsable']}",
                parent=self.ventana)

            self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error al guardar",
                f"❌ No se pudo guardar la reserva:\n{e}",
                parent=self.ventana)
            print(f"[ERROR] Al guardar reserva: {e}")

    # ----------------------------------------------------------
    #  LIMPIAR FORMULARIO
    # ----------------------------------------------------------

    def limpiar_formulario(self):
        self.var_sala.set("")
        self.var_fecha.set("")
        self.var_hora_inicio.set("")
        self.var_hora_fin.set("")
        self.var_responsable.set("")
        self.txt_descripcion.delete("1.0", "end")

    # ----------------------------------------------------------
    #  CANCELAR
    # ----------------------------------------------------------

    def cancelar(self):
        self.ventana.destroy()
        self.callback()


# ============================================================
#  PRUEBA RÁPIDA → python ui/pantalla_registro.py
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Menú Principal (prueba)")
    root.geometry("300x200")
    root.configure(bg="#e8eaf6")

    tk.Label(root, text="Sistema de Reservas",
        font=("Arial", 13, "bold"), bg="#e8eaf6", fg="#1a237e").pack(pady=30)

    def volver_menu():
        print("✅ Pantalla cerrada, volviendo al menú.")

    tk.Button(root, text="➕ Nueva Reserva",
        font=("Arial", 11, "bold"), bg="#1565c0", fg="white",
        relief="flat", cursor="hand2",
        command=lambda: PantallaRegistro(root, volver_menu)).pack(pady=10)

    root.mainloop()