import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db.sqlite"

class ConexionBD:
    def __init__(self):
        self.conexion = None
    
    def conectar(self):
        self.conexion = sqlite3.connect(str(DB_PATH))
        self.conexion.row_factory = sqlite3.Row
    
    def desconectar(self):
        if self.conexion:
            self.conexion.close()
    
    def ejecutar(self, sql, params=()):
        cursor = self.conexion.cursor()
        cursor.execute(sql, params)
        self.conexion.commit()
        return cursor.lastrowid
    
    def consultar(self, sql, params=()):
        cursor = self.conexion.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

class BaseDatos:
    def __init__(self):
        self.bd = ConexionBD()
        self.bd.conectar()
        self.inicializar()
    
    def inicializar(self):
        sql_salas = "CREATE TABLE IF NOT EXISTS salas (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL UNIQUE, capacidad INTEGER NOT NULL, disponible BOOLEAN DEFAULT 1, fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP)"
        self.bd.ejecutar(sql_salas)
        
        sql_reservas = "CREATE TABLE IF NOT EXISTS reservas (id INTEGER PRIMARY KEY AUTOINCREMENT, sala_id INTEGER NOT NULL, fecha DATE NOT NULL, hora_inicio TIME NOT NULL, hora_fin TIME NOT NULL, responsable TEXT NOT NULL, descripcion TEXT, estado TEXT DEFAULT 'activa', fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (sala_id) REFERENCES salas(id))"
        self.bd.ejecutar(sql_reservas)
        
        self.insertar_salas_defecto()
    
    def insertar_salas_defecto(self):
        salas = [("Aula 101", 30), ("Aula 102", 40), ("Sala de Juntas", 15)]
        for nombre, capacidad in salas:
            try:
                self.bd.ejecutar("INSERT INTO salas (nombre, capacidad) VALUES (?, ?)", (nombre, capacidad))
            except:
                pass
    
    def obtener_salas(self):
        return self.bd.consultar("SELECT * FROM salas WHERE disponible = 1")
    
    def obtener_sala_por_id(self, sala_id):
        resultado = self.bd.consultar("SELECT * FROM salas WHERE id = ?", (sala_id,))
        return resultado[0] if resultado else None
    
    def insertar_sala(self, nombre, capacidad):
        return self.bd.ejecutar("INSERT INTO salas (nombre, capacidad) VALUES (?, ?)", (nombre, capacidad))
    
    def eliminar_sala(self, sala_id):
        return self.bd.ejecutar("UPDATE salas SET disponible = 0 WHERE id = ?", (sala_id,))
    
    def insertar_reserva(self, sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion=""):
        sql = "INSERT INTO reservas (sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion) VALUES (?, ?, ?, ?, ?, ?)"
        return self.bd.ejecutar(sql, (sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion))
    
    def obtener_reservas_por_fecha(self, fecha):
        sql = "SELECT r.*, s.nombre as sala_nombre FROM reservas r JOIN salas s ON r.sala_id = s.id WHERE r.fecha = ? AND r.estado = 'activa' ORDER BY r.hora_inicio"
        return self.bd.consultar(sql, (fecha,))
    
    def obtener_reserva_por_id(self, reserva_id):
        sql = "SELECT r.*, s.nombre as sala_nombre FROM reservas r JOIN salas s ON r.sala_id = s.id WHERE r.id = ?"
        resultado = self.bd.consultar(sql, (reserva_id,))
        return resultado[0] if resultado else None
    
    def validar_solapamiento(self, sala_id, fecha, hora_inicio, hora_fin, reserva_id=None):
        sql = "SELECT * FROM reservas WHERE sala_id = ? AND fecha = ? AND estado = 'activa' AND ((hora_inicio < ? AND hora_fin > ?) OR (hora_inicio < ? AND hora_fin > ?) OR (hora_inicio >= ? AND hora_fin <= ?))"
        if reserva_id:
            sql += f" AND id != {reserva_id}"
        resultado = self.bd.consultar(sql, (sala_id, fecha, hora_fin, hora_inicio, hora_fin, hora_inicio, hora_inicio, hora_fin))
        return len(resultado) > 0
    
    def actualizar_reserva(self, reserva_id, sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion=""):
        sql = "UPDATE reservas SET sala_id = ?, fecha = ?, hora_inicio = ?, hora_fin = ?, responsable = ?, descripcion = ? WHERE id = ?"
        return self.bd.ejecutar(sql, (sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion, reserva_id))
    
    def eliminar_reserva(self, reserva_id):
        return self.bd.ejecutar("UPDATE reservas SET estado = 'cancelada' WHERE id = ?", (reserva_id,))
    
    def cerrar(self):
        self.bd.desconectar()
