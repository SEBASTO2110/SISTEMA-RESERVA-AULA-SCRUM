# 📅 Sistema de Gestión de Reservas de Salas



## Link del video

https://drive.google.com/file/d/1YfWkeM1GGKc44bR3U4Vxym13l9-KzuWe/view?usp=sharing



## Link de la documentación 

https://docs.google.com/document/d/1fzCzoZXGqFUtH_FqZPJ7Za6zVSeDOLaA/edit?usp=sharing&ouid=117062481297950245071&rtpof=true&sd=true


## Link de las diapositivas
https://drive.google.com/file/d/1Hzi8XRPIRwbZlBm5w_GOIbrRnecfW0Hl/view?usp=sharing

## 📖 Descripción

**Sistema de Gestión de Reservas de Salas** es una aplicación de escritorio desarrollada en Python que permite a usuarios y administradores gestionar de forma intuitiva la reserva de salas y aulas, evitando conflictos de horarios y manteniendo un control centralizado.

### ✨ Características Principales

- ✅ **Registrar reservas** con validación automática de solapamientos
- ✅ **Consultar reservas** por fecha específica
- ✅ **Ver detalles completos** de cada reserva
- ✅ **Modificar reservas** existentes
- ✅ **Cancelar reservas** con confirmación de usuario
- ✅ **Gestionar salas** disponibles en el sistema
- ✅ **Dashboard moderno** con interfaz intuitiva
- ✅ **Base de datos robusta** con validaciones integradas

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- Windows, macOS o Linux

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/SEBASTO2110/SISTEMA-RESERVA-AULA-SCRUM.git
cd SISTEMA-RESERVA-AULA-SCRUM
```

2. **Crear entorno virtual (opcional pero recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Ejecutar la aplicación**
```bash
python main.py
```

**¡Listo!** La aplicación abrirá automáticamente.

---

## 📁 Estructura del Proyecto

```
SISTEMA-RESERVA-AULA-SCRUM/
├── main.py                    # Punto de entrada de la aplicación
├── db.sqlite                  # Base de datos SQLite
├── README.md                  # Este archivo
├── .gitignore                 # Archivos ignorados por Git
│
├── models/
│   ├── __init__.py
│   └── database.py            # Lógica de BD y funciones CRUD
│
├── ui/
│   ├── __init__.py
│   ├── interfaz.py            # Dashboard principal
│   ├── pantalla_registro.py   # Registrar reserva
│   ├── pantalla_consulta.py   # Consultar por fecha
│   ├── pantalla_cancelar.py   # Cancelar reserva
│   ├── pantalla_detalles.py   # Ver detalles
│   └── pantalla_modificar.py  # Modificar reserva
│
└── utils/
    ├── __init__.py
    └── constantes.py          # Constantes globales
```

---

## 🎯 Uso de la Aplicación

### 1. **Registrar Nueva Reserva**
```
1. Click en "Registrar Nueva Reserva"
2. Selecciona sala del dropdown
3. Ingresa fecha (YYYY-MM-DD)
4. Ingresa hora inicio y fin (HH:MM)
5. Ingresa responsable y descripción
6. Click en "Guardar"
```

**Validaciones:**
- Hora fin debe ser mayor que hora inicio
- No puede haber solapamiento en la misma sala
- Todos los campos son obligatorios

### 2. **Consultar Reservas por Fecha**
```
1. Click en "Consultar Reservas"
2. Ingresa fecha (YYYY-MM-DD)
3. Click en "Buscar"
4. Ve tabla con reservas del día
```

### 3. **Ver Detalles de Reserva**
```
1. Click en "Ver Detalles"
2. Selecciona fecha
3. Doble click en una reserva
4. Se abre popup con información completa
```

### 4. **Modificar Reserva**
```
1. Click en "Modificar Reserva"
2. Ingresa ID de reserva
3. Edita los campos que necesites
4. Click en "Guardar"
```

### 5. **Cancelar Reserva**
```
1. Click en "Cancelar Reserva"
2. Ingresa fecha
3. Selecciona reserva de la lista
4. Click en "Cancelar"
5. Confirma la acción
```

### 6. **Gestionar Salas**
```
1. Click en "Gestionar Salas"
2. Ve todas las salas disponibles
3. Puedes agregar o eliminar salas
```

---

## 🗄️ Base de Datos

### Tabla: `salas`
```sql
CREATE TABLE salas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    capacidad INTEGER NOT NULL,
    disponible BOOLEAN DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### Tabla: `reservas`
```sql
CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sala_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    responsable TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT DEFAULT 'activa',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sala_id) REFERENCES salas(id)
)
```

### Salas Predeterminadas
- **Aula 101** - Capacidad: 30 personas
- **Aula 102** - Capacidad: 40 personas
- **Sala de Juntas** - Capacidad: 15 personas

---

## 🔧 API de la Base de Datos

### Clase `BaseDatos`

```python
from models.database import BaseDatos

db = BaseDatos()
```

#### Métodos Disponibles

**Salas:**
```python
db.obtener_salas()                      # Retorna todas las salas
db.insertar_sala(nombre, capacidad)     # Crea nueva sala
db.eliminar_sala(id)                    # Elimina una sala
```

**Reservas:**
```python
db.obtener_reservas_por_fecha(fecha)    # Obtiene reservas de un día
db.obtener_reserva_por_id(id)           # Obtiene una reserva específica
db.insertar_reserva(...)                # Crea nueva reserva
db.actualizar_reserva(...)              # Modifica una reserva
db.eliminar_reserva(id)                 # Cancela una reserva (soft delete)
```

**Validaciones:**
```python
db.validar_solapamiento(sala_id, fecha, hora_inicio, hora_fin)
# Retorna True si hay solapamiento, False si está disponible
```

---

## 💻 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|----------|
| **Python** | 3.13 | Lenguaje principal |
| **Tkinter** | Incluido | Interfaz gráfica |
| **SQLite3** | Incluido | Base de datos |
| **Git** | - | Control de versión |

### ¿Por qué estas tecnologías?

- ✅ **Sin dependencias externas**: Tkinter y SQLite3 vienen con Python
- ✅ **Multiplataforma**: Windows, macOS, Linux
- ✅ **Ligero**: Bajo consumo de memoria
- ✅ **Rápido**: Excelente rendimiento
- ✅ **Fácil de mantener**: Código limpio y documentado

---

## 📊 Desarrollo - Metodología SCRUM

### Sprint 1 (Día 1 - 14 de Marzo)
- Arquitectura base del sistema
- Base de datos con tablas iniciales
- Interfaz principal con 7 opciones
- Pantallas con datos fake

**Historias:** 4 | **Puntos:** 20

### Sprint 2 (Día 2 - 15 de Marzo)
- Integración con base de datos real
- Todas las pantallas funcionales
- Validaciones completas
- Sistema listo para uso

**Historias:** 7 | **Puntos:** 26

### Sprint 3 (Día 3 - 18 de Marzo)
- Rediseño visual
- Testing integral
- Documentación final
- Presentación

---

## 👥 Equipo de Desarrollo

| Miembro | Rol | Responsabilidad |
|---------|-----|-----------------|
| **Sebastián Díaz** | Scrum Master + Senior Dev | Liderazgo, Interfaz Principal, Integración |
| **Montoya** | Database Developer | Base de datos y funciones CRUD |
| **Junior** | Frontend Developer | Pantalla de Registro |
| **Santiago** | Frontend Developer | Pantallas de Consulta y Cancelación |
| **Jesús** | Product Owner | Visión y prioridades del proyecto |

---

## 📈 Métricas del Proyecto

### Productividad
- **Líneas de código:** 1200+
- **Funciones:** 15+
- **Clases:** 7
- **Historias completadas:** 11/11 (100%)

### Calidad
- **Bugs críticos:** 0
- **Bugs menores:** 0
- **Tests pasados:** 100%
- **Code review:** Aprobado

### Tiempo
- **Duración planeada:** 3 días
- **Duración real:** 3 días
- **Exactitud:** 100%

---

## 🐛 Reporte de Errores

Si encuentras un bug:

1. Abre un **Issue** en GitHub
2. Describe el problema detalladamente
3. Incluye pasos para reproducirlo
4. Adjunta capturas si es necesario

```
Título: [BUG] Descripción breve
Descripción:
- Qué pasó
- Qué esperabas que pasara
- Pasos para reproducir
- Versión de Python
```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

### Cómo contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- Usar nombres descriptivos en español
- Documentar funciones con docstrings
- Seguir PEP 8
- Hacer commits atómicos y significativos

