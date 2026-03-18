import tkinter as tk
from tkinter import messagebox, ttk
from models.database import BaseDatos
from ui.pantalla_registro import PantallaRegistro
from ui.pantalla_consulta import PantallaConsulta
from ui.pantalla_cancelar import PantallaCancelar
from ui.pantalla_detalles import PantallaDetalles
from ui.pantalla_modificar import PantallaModificar

class DashboardModerno:
    """Clase principal para el dashboard moderno"""
    
    # ========== PALETA DE COLORES MODERNA ==========
    COLORES = {
        'fondo_principal': '#0F1419',      # Negro azulado oscuro
        'fondo_secundario': '#1A1F2E',     # Gris oscuro
        'fondo_card': '#252D3D',           # Card background
        'borde': '#3A4452',                # Bordes sutiles
        'texto_principal': '#FFFFFF',      # Blanco
        'texto_secundario': '#B0B8C5',     # Gris claro
        'acento_azul': '#0084FF',          # Azul vibrante
        'acento_verde': '#10B981',         # Verde moderno
        'acento_coral': '#FF6B6B',         # Coral/Rojo
        'acento_amarillo': '#FBBF24',      # Amarillo/Naranja
        'acento_purple': '#8B5CF6',        # Púrpura
        'acento_cyan': '#06B6D4',          # Cyan
        'hover': '#3A4452',                # Color hover
        'sombra': '#000000',               # Sombra
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas de Salas - Dashboard Moderno")
        self.root.geometry("1200x750")
        self.root.resizable(False, False)
        
        # Base de datos
        self.db = BaseDatos()
        
        # Variables para controlar estados
        self.opcion_actual = tk.StringVar(value="home")
        
        # Configurar estilos ttk
        self.configurar_estilos()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def configurar_estilos(self):
        """Configura los estilos ttk para toda la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores para ttk
        style.configure('TFrame', background=self.COLORES['fondo_principal'])
        style.configure('TLabel', background=self.COLORES['fondo_principal'], 
        foreground=self.COLORES['texto_principal'])
    
    def crear_interfaz(self):
        """Crea la interfaz completa del dashboard"""
        self.root.configure(bg=self.COLORES['fondo_principal'])
        
        # ========== CONTENEDOR PRINCIPAL ==========
        main_container = tk.Frame(self.root, bg=self.COLORES['fondo_principal'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ========== SIDEBAR IZQUIERDO ==========
        self.crear_sidebar(main_container)
        
        # ========== CONTENIDO PRINCIPAL ==========
        self.crear_contenido_principal(main_container)
    
    def crear_sidebar(self, parent):
        """Crea la barra lateral de navegación"""
        sidebar = tk.Frame(parent, bg=self.COLORES['fondo_secundario'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH)
        sidebar.pack_propagate(False)
        
        # ========== HEADER DEL SIDEBAR ==========
        header_sidebar = tk.Frame(sidebar, bg=self.COLORES['acento_azul'], height=80)
        header_sidebar.pack(fill=tk.X, padx=0, pady=0)
        header_sidebar.pack_propagate(False)
        
        tk.Label(
            header_sidebar,
            text="📅",
            font=("Arial", 36),
            bg=self.COLORES['acento_azul'],
            fg=self.COLORES['texto_principal']
        ).pack(pady=(10, 0))
        
        tk.Label(
            header_sidebar,
            text="Reservas",
            font=("Arial", 14, "bold"),
            bg=self.COLORES['acento_azul'],
            fg=self.COLORES['texto_principal']
        ).pack(pady=(5, 10))
        
        # ========== SEPARADOR ==========
        separator = tk.Frame(sidebar, bg=self.COLORES['borde'], height=1)
        separator.pack(fill=tk.X, padx=0, pady=10)
        
        # ========== MENÚ LATERAL ==========
        menu_items = [
            ("🏠 Inicio", "home", self.COLORES['acento_azul']),
            ("➕ Registrar", "registrar", self.COLORES['acento_verde']),
            ("🔍 Consultar", "consultar", self.COLORES['acento_cyan']),
            ("📄 Detalles", "detalles", self.COLORES['acento_purple']),
            ("✏️ Modificar", "modificar", self.COLORES['acento_amarillo']),
            ("❌ Cancelar", "cancelar", self.COLORES['acento_coral']),
            ("🏢 Salas", "salas", self.COLORES['acento_verde']),
        ]
        
        for texto, valor, color in menu_items:
            self.crear_boton_sidebar(sidebar, texto, valor, color)
        
        # ========== FOOTER SIDEBAR ==========
        footer_space = tk.Frame(sidebar, bg=self.COLORES['fondo_secundario'])
        footer_space.pack(fill=tk.BOTH, expand=True)
        
        separator_footer = tk.Frame(sidebar, bg=self.COLORES['borde'], height=1)
        separator_footer.pack(fill=tk.X, padx=0, pady=10)
        
        btn_salir = tk.Button(
            sidebar,
            text="🚪 Salir",
            font=("Arial", 11, "bold"),
            bg=self.COLORES['acento_coral'],
            fg=self.COLORES['texto_principal'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.salir,
            padx=20,
            pady=10,
            activebackground="#FF5252",
            activeforeground=self.COLORES['texto_principal'],
            bd=0,
            highlightthickness=0
        )
        btn_salir.pack(fill=tk.X, padx=15, pady=10)
    
    def crear_boton_sidebar(self, parent, texto, valor, color):
        """Crea un botón del menú lateral con efecto hover"""
        btn = tk.Button(
            parent,
            text=texto,
            font=("Arial", 11, "bold"),
            bg=self.COLORES['fondo_secundario'],
            fg=self.COLORES['texto_principal'],
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.cambiar_vista(valor),
            padx=20,
            pady=12,
            activebackground=color,
            activeforeground=self.COLORES['texto_principal'],
            bd=0,
            highlightthickness=0,
            justify=tk.LEFT
        )
        btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Agregar efecto hover
        btn.bind("<Enter>", lambda e: btn.config(bg=self.COLORES['hover']))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.COLORES['fondo_secundario']))
    
    def crear_contenido_principal(self, parent):
        """Crea el área de contenido principal"""
        content_frame = tk.Frame(parent, bg=self.COLORES['fondo_principal'])
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ========== HEADER SUPERIOR ==========
        self.crear_header_superior(content_frame)
        
        # ========== ÁREA DE CONTENIDO ==========
        self.content_area = tk.Frame(content_frame, bg=self.COLORES['fondo_principal'])
        self.content_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mostrar vista por defecto
        self.mostrar_vista_inicio()
    
    def crear_header_superior(self, parent):
        """Crea el header superior con información"""
        header = tk.Frame(parent, bg=self.COLORES['fondo_secundario'], height=70)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Título
        tk.Label(
            header,
            text="Sistema de Gestión de Reservas",
            font=("Arial", 18, "bold"),
            bg=self.COLORES['fondo_secundario'],
            fg=self.COLORES['texto_principal']
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Información de usuario/hora (lado derecho)
        info_frame = tk.Frame(header, bg=self.COLORES['fondo_secundario'])
        info_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(
            info_frame,
            text="👤 Usuario",
            font=("Arial", 10),
            bg=self.COLORES['fondo_secundario'],
            fg=self.COLORES['texto_secundario']
        ).pack(side=tk.LEFT, padx=10)
    
    def cambiar_vista(self, vista):
        """Cambia la vista actual"""
        self.opcion_actual.set(vista)
        
        # Limpiar contenido
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Mostrar nueva vista
        if vista == "home":
            self.mostrar_vista_inicio()
        elif vista == "registrar":
            self.abrir_pantalla_registrar()
        elif vista == "consultar":
            self.abrir_pantalla_consultar()
        elif vista == "detalles":
            self.abrir_pantalla_detalles()
        elif vista == "modificar":
            self.abrir_pantalla_modificar()
        elif vista == "cancelar":
            self.abrir_pantalla_cancelar()
        elif vista == "salas":
            self.mostrar_salas()
    
    def mostrar_vista_inicio(self):
        """Muestra la vista de inicio con tarjetas de acciones rápidas"""
        # Título
        tk.Label(
            self.content_area,
            text="Bienvenido al Sistema de Reservas",
            font=("Arial", 20, "bold"),
            bg=self.COLORES['fondo_principal'],
            fg=self.COLORES['texto_principal']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        tk.Label(
            self.content_area,
            text="Selecciona una acción para comenzar",
            font=("Arial", 11),
            bg=self.COLORES['fondo_principal'],
            fg=self.COLORES['texto_secundario']
        ).pack(anchor=tk.W, pady=(0, 30))
        
        # Grid de tarjetas de acciones
        cards_frame = tk.Frame(self.content_area, bg=self.COLORES['fondo_principal'])
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        acciones = [
            ("➕", "Registrar Reserva", "Crea una nueva reserva", self.COLORES['acento_verde'], self.abrir_pantalla_registrar),
            ("🔍", "Consultar Reservas", "Busca por fecha", self.COLORES['acento_cyan'], self.abrir_pantalla_consultar),
            ("📄", "Ver Detalles", "Información completa", self.COLORES['acento_purple'], self.abrir_pantalla_detalles),
            ("✏️", "Modificar Reserva", "Edita una reserva", self.COLORES['acento_amarillo'], self.abrir_pantalla_modificar),
            ("❌", "Cancelar Reserva", "Elimina una reserva", self.COLORES['acento_coral'], self.abrir_pantalla_cancelar),
            ("🏢", "Gestionar Salas", "Ver salas disponibles", self.COLORES['acento_verde'], self.mostrar_salas),
        ]
        
        # Crear tarjetas en grid 3x2
        for idx, (icono, titulo, subtitulo, color, comando) in enumerate(acciones):
            fila = idx // 3
            col = idx % 3
            
            self.crear_tarjeta_accion(
                cards_frame, icono, titulo, subtitulo, color, comando
            ).grid(row=fila, column=col, padx=15, pady=15, sticky="nsew")
        
        # Configurar pesos de columnas
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)
    
    def crear_tarjeta_accion(self, parent, icono, titulo, subtitulo, color, comando):
        """Crea una tarjeta de acción moderna"""
        # Frame externo (para sombra)
        frame_shadow = tk.Frame(parent, bg=self.COLORES['borde'], relief=tk.FLAT, bd=0)
        
        # Frame principal
        frame = tk.Frame(frame_shadow, bg=self.COLORES['fondo_card'], relief=tk.FLAT, bd=0)
        frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
        
        # Barra de color en la parte superior
        color_bar = tk.Frame(frame, bg=color, height=4)
        color_bar.pack(fill=tk.X, padx=0, pady=0)
        
        # Contenido
        content = tk.Frame(frame, bg=self.COLORES['fondo_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Ícono grande
        tk.Label(
            content,
            text=icono,
            font=("Arial", 32),
            bg=self.COLORES['fondo_card'],
            fg=color
        ).pack(pady=(0, 10))
        
        # Título
        tk.Label(
            content,
            text=titulo,
            font=("Arial", 12, "bold"),
            bg=self.COLORES['fondo_card'],
            fg=self.COLORES['texto_principal']
        ).pack(pady=(0, 5))
        
        # Subtítulo
        tk.Label(
            content,
            text=subtitulo,
            font=("Arial", 9),
            bg=self.COLORES['fondo_card'],
            fg=self.COLORES['texto_secundario']
        ).pack(pady=(0, 15))
        
        # Botón
        btn = tk.Button(
            content,
            text="Ir →",
            font=("Arial", 10, "bold"),
            bg=color,
            fg=self.COLORES['texto_principal'],
            relief=tk.FLAT,
            cursor="hand2",
            command=comando,
            padx=20,
            pady=8,
            activebackground=color,
            activeforeground=self.COLORES['texto_principal'],
            bd=0,
            highlightthickness=0
        )
        btn.pack(fill=tk.X)
        
        # Efecto hover en la tarjeta completa
        def on_enter(e):
            frame.config(bg="#2E3847")
            content.config(bg="#2E3847")
        
        def on_leave(e):
            frame.config(bg=self.COLORES['fondo_card'])
            content.config(bg=self.COLORES['fondo_card'])
        
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
        content.bind("<Enter>", on_enter)
        content.bind("<Leave>", on_leave)
        
        return frame_shadow
    
    # ========== MÉTODOS PARA ABRIR PANTALLAS ==========
    
    def abrir_pantalla_registrar(self):
        ventana = tk.Toplevel(self.root)
        app = PantallaRegistro(ventana, self.db)
    
    def abrir_pantalla_consultar(self):
        ventana = tk.Toplevel(self.root)
        app = PantallaConsulta(ventana, self.db)
    
    def abrir_pantalla_detalles(self):
        ventana = tk.Toplevel(self.root)
        app = PantallaDetalles(ventana, self.db)
    
    def abrir_pantalla_modificar(self):
        ventana = tk.Toplevel(self.root)
        app = PantallaModificar(ventana, self.db)
    
    def abrir_pantalla_cancelar(self):
        ventana = tk.Toplevel(self.root)
        app = PantallaCancelar(ventana, self.db)
    
    def mostrar_salas(self):
        """Muestra las salas disponibles en la vista principal"""
        # Limpiar
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Título
        tk.Label(
            self.content_area,
            text="🏢 Salas Disponibles",
            font=("Arial", 20, "bold"),
            bg=self.COLORES['fondo_principal'],
            fg=self.COLORES['texto_principal']
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Obtener salas
        salas = self.db.obtener_salas()
        
        if not salas:
            tk.Label(
                self.content_area,
                text="No hay salas disponibles",
                font=("Arial", 12),
                bg=self.COLORES['fondo_principal'],
                fg=self.COLORES['texto_secundario']
            ).pack(pady=20)
            return
        
        # Mostrar salas en tarjetas
        for sala in salas:
            self.crear_tarjeta_sala(self.content_area, sala)
    
    def crear_tarjeta_sala(self, parent, sala):
        """Crea una tarjeta para mostrar información de una sala"""
        frame = tk.Frame(parent, bg=self.COLORES['fondo_card'], relief=tk.FLAT, bd=1)
        frame.pack(fill=tk.X, pady=10)
        
        content = tk.Frame(frame, bg=self.COLORES['fondo_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Nombre de la sala
        tk.Label(
            content,
            text=sala['nombre'],
            font=("Arial", 14, "bold"),
            bg=self.COLORES['fondo_card'],
            fg=self.COLORES['acento_azul']
        ).pack(anchor=tk.W)
        
        # Capacidad
        tk.Label(
            content,
            text=f"Capacidad: {sala['capacidad']} personas",
            font=("Arial", 11),
            bg=self.COLORES['fondo_card'],
            fg=self.COLORES['texto_secundario']
        ).pack(anchor=tk.W, pady=(5, 0))
        
        # Estado
        estado = "Disponible" if sala['disponible'] else "No disponible"
        color_estado = self.COLORES['acento_verde'] if sala['disponible'] else self.COLORES['acento_coral']
        
        tk.Label(
            content,
            text=f"Estado: {estado}",
            font=("Arial", 10),
            bg=self.COLORES['fondo_card'],
            fg=color_estado
        ).pack(anchor=tk.W, pady=(2, 0))
    
    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.root.quit()

def main():
    """Punto de entrada de la aplicación"""
    root = tk.Tk()
    app = DashboardModerno(root)
    root.mainloop()

if __name__ == "__main__":
    main()
