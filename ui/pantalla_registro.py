import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ============================================================
#  BASE DE DATOS FALSA (temporal hasta conectar SQLite real)
#  Cuando tengan la BD real, solo cambian estas funciones:
#  - obtener_salas()
#  - obtener_reservas()
#  - guardar_reserva_en_bd()
# ============================================================

SALAS_FAKE = [
    "Aula 101",
    "Aula 102",
    "Aula 103",
    "Laboratorio de cómputo 1",
    "Laboratorio de cómputo 2",
    "Sala de reuniones A",
    "Sala de reuniones B",
]

RESERVAS_FAKE = [
    {
        "id": 1,
        "sala": "Aula 101",
        "fecha": "2026-03-15",
        "hora_inicio": "09:00",
        "hora_fin": "11:00",
        "responsable": "Carlos Gómez",
        "descripcion": "Clase de Python",
    },
    {
        "id": 2,
        "sala": "Sala de reuniones A",
        "fecha": "2026-03-15",
        "hora_inicio": "14:00",
        "hora_fin": "16:00",
        "responsable": "Ana Torres",
        "descripcion": "Reunión de coordinación",
    },
    {
        "id": 3,
        "sala": "Laboratorio de cómputo 1",
        "fecha": "2026-03-16",
        "hora_inicio": "08:00",
        "hora_fin": "10:00",
        "responsable": "Grupo C3",
        "descripcion": "Taller de bases de datos",
    },
]


def obtener_salas():
    """Retorna la lista de salas. Aquí se conectará la BD real después."""
    return SALAS_FAKE


def obtener_reservas():
    """Retorna todas las reservas. Aquí se conectará la BD real después."""
    return RESERVAS_FAKE


def guardar_reserva_en_bd(datos):
    """
    Guarda la reserva. Por ahora solo la agrega a la lista fake.
    Cuando tengan SQLite, reemplazan esto por INSERT INTO reservas...
    """
    nuevo_id = len(RESERVAS_FAKE) + 1
    nueva_reserva = {
        "id": nuevo_id,
        "sala": datos["sala"],
        "fecha": datos["fecha"],
        "hora_inicio": datos["hora_inicio"],
        "hora_fin": datos["hora_fin"],
        "responsable": datos["responsable"],
        "descripcion": datos["descripcion"],
    }
    RESERVAS_FAKE.append(nueva_reserva)
    print(f"[BD FAKE] Reserva guardada: {nueva_reserva}")
    return True


# ============================================================
#  CLASE PRINCIPAL
# ============================================================

class PantallaRegistro:
    def __init__(self, parent, callback):
        """
        parent   = ventana padre (la ventana principal / menú)
        callback = función que se llama al cerrar esta pantalla
        """
        self.parent = parent
        self.callback = callback

        # Ventana emergente
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Nueva Reserva")
        self.ventana.geometry("500x560")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f4f8")
        self.ventana.grab_set()  # Bloquea la ventana padre mientras esta está abierta

        # Centrar ventana en pantalla
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - 250
        y = (self.ventana.winfo_screenheight() // 2) - 280
        self.ventana.geometry(f"500x560+{x}+{y}")

        self.crear_formulario()

    # ----------------------------------------------------------
    #  CREAR FORMULARIO
    # ----------------------------------------------------------

    def crear_formulario(self):
        # Título
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

        # Frame del formulario
        frame = tk.Frame(self.ventana, bg="#ffffff", bd=1, relief="solid", padx=25, pady=20)
        frame.pack(fill="both", expand=True, padx=20, pady=5)

        # --- Campo 1: Sala ---
        tk.Label(frame, text="Sala *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", pady=(8, 2))
        self.var_sala = tk.StringVar()
        self.combo_sala = ttk.Combobox(
            frame,
            textvariable=self.var_sala,
            values=obtener_salas(),
            state="readonly",
            width=34,
            font=("Arial", 10),
        )
        self.combo_sala.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # --- Campo 2: Fecha ---
        tk.Label(frame, text="Fecha * (YYYY-MM-DD)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=2, column=0, sticky="w", pady=(8, 2))
        self.var_fecha = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_fecha, width=37,
                 font=("Arial", 10)).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # --- Fila de horas (inicio y fin en la misma fila) ---
        frame_horas = tk.Frame(frame, bg="#ffffff")
        frame_horas.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        # Campo 3: Hora Inicio
        tk.Label(frame_horas, text="Hora Inicio * (HH:MM)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 10))
        # Campo 4: Hora Fin
        tk.Label(frame_horas, text="Hora Fin * (HH:MM)", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=0, column=1, sticky="w")

        self.var_hora_inicio = tk.StringVar()
        tk.Entry(frame_horas, textvariable=self.var_hora_inicio, width=17,
                 font=("Arial", 10)).grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(2, 8))

        self.var_hora_fin = tk.StringVar()
        tk.Entry(frame_horas, textvariable=self.var_hora_fin, width=17,
                 font=("Arial", 10)).grid(row=1, column=1, sticky="ew", pady=(2, 8))

        # --- Campo 5: Responsable ---
        tk.Label(frame, text="Responsable *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=5, column=0, sticky="w", pady=(8, 2))
        self.var_responsable = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_responsable, width=37,
                 font=("Arial", 10)).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # --- Campo 6: Descripción ---
        tk.Label(frame, text="Descripción *", font=("Arial", 10, "bold"),
                 bg="#ffffff", anchor="w").grid(row=7, column=0, sticky="w", pady=(8, 2))
        self.txt_descripcion = tk.Text(frame, width=37, height=4, font=("Arial", 10))
        self.txt_descripcion.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # --- Botones ---
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
            command=self.cancelar,
        ).pack(side="left", padx=10)

    # ----------------------------------------------------------
    #  VALIDACIONES
    # ----------------------------------------------------------

    def validar_formulario(self):
        sala        = self.var_sala.get().strip()
        fecha       = self.var_fecha.get().strip()
        hora_inicio = self.var_hora_inicio.get().strip()
        hora_fin    = self.var_hora_fin.get().strip()
        responsable = self.var_responsable.get().strip()
        descripcion = self.txt_descripcion.get("1.0", "end").strip()

        # Validación 1: Ningún campo vacío
        if not all([sala, fecha, hora_inicio, hora_fin, responsable, descripcion]):
            messagebox.showerror(
                "Campo vacío",
                "❌ Completa todos los campos.\nNingún campo puede quedar vacío.",
                parent=self.ventana,
            )
            return False

        # Validación 2: Formato de hora correcto (HH:MM)
        try:
            t_inicio = datetime.strptime(hora_inicio, "%H:%M")
            t_fin    = datetime.strptime(hora_fin,    "%H:%M")
        except ValueError:
            messagebox.showerror(
                "Formato incorrecto",
                "❌ Formato de hora incorrecto.\nUsa el formato HH:MM  (ejemplo: 09:00)",
                parent=self.ventana,
            )
            return False

        # Validación 3: Hora fin > Hora inicio
        if t_fin <= t_inicio:
            messagebox.showerror(
                "Error de horario",
                "❌ La hora fin debe ser mayor que la hora inicio.",
                parent=self.ventana,
            )
            return False

        # Validación 4: Solapamiento con reservas existentes (BD fake)
        for r in obtener_reservas():
            if r["sala"] == sala and r["fecha"] == fecha:
                r_inicio = datetime.strptime(r["hora_inicio"], "%H:%M")
                r_fin    = datetime.strptime(r["hora_fin"],    "%H:%M")
                # Hay solapamiento si los intervalos se cruzan
                if t_inicio < r_fin and t_fin > r_inicio:
                    messagebox.showerror(
                        "Horario no disponible",
                        f"❌ La sala '{sala}' ya tiene una reserva\n"
                        f"de {r['hora_inicio']} a {r['hora_fin']} ese día.\n\n"
                        f"Por favor elige otro horario o sala.",
                        parent=self.ventana,
                    )
                    return False

        return True

    # ----------------------------------------------------------
    #  GUARDAR
    # ----------------------------------------------------------

    def guardar_reserva(self):
        if self.validar_formulario():
            datos = {
                "sala":        self.var_sala.get().strip(),
                "fecha":       self.var_fecha.get().strip(),
                "hora_inicio": self.var_hora_inicio.get().strip(),
                "hora_fin":    self.var_hora_fin.get().strip(),
                "responsable": self.var_responsable.get().strip(),
                "descripcion": self.txt_descripcion.get("1.0", "end").strip(),
            }

            # Guardar (en BD fake por ahora)
            guardar_reserva_en_bd(datos)

            messagebox.showinfo(
                "Reserva guardada",
                f"✅ Reserva guardada exitosamente.\n\n"
                f"Sala: {datos['sala']}\n"
                f"Fecha: {datos['fecha']}\n"
                f"Horario: {datos['hora_inicio']} - {datos['hora_fin']}\n"
                f"Responsable: {datos['responsable']}",
                parent=self.ventana,
            )

            # Limpiar formulario para una nueva reserva
            self.limpiar_formulario()

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
#  PRUEBA RÁPIDA — Corre este archivo solo para probarlo
#  python ui/pantalla_registro.py
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Menú Principal (prueba)")
    root.geometry("300x200")
    root.configure(bg="#e8eaf6")

    tk.Label(
        root,
        text="Sistema de Reservas",
        font=("Arial", 13, "bold"),
        bg="#e8eaf6",
        fg="#1a237e",
    ).pack(pady=30)

    def volver_menu():
        print("✅ Pantalla cerrada, volviendo al menú principal.")

    tk.Button(
        root,
        text="➕ Nueva Reserva",
        font=("Arial", 11, "bold"),
        bg="#1565c0",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=lambda: PantallaRegistro(root, volver_menu),
    ).pack(pady=10)

    root.mainloop()