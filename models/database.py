import sqlite3
class ConexionBD:

    def __init__(self, nombre_db="db.sqlite"):
        self.nombre_db = nombre_db
        self.conn = None

    def conectar(self):
        self.conn = sqlite3.connect(self.nombre_db)
        return self.conn

    def desconectar(self):
        if self.conn:
            self.conn.close()

    def ejecutar(self, sql, params=()):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute(sql, params)
        conn.commit()

        last_id = cursor.lastrowid

        self.desconectar()

        return last_id

    def consultar(self, sql, params=()):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute(sql, params)

        resultados = cursor.fetchall()

        self.desconectar()

        return resultados


def crear_tablas():
    
    db = ConexionBD()

    sql_salas = """
    CREATE TABLE IF NOT EXISTS salas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        capacidad INTEGER,
        disponible BOOLEAN DEFAULT 1,
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """

    sql_reservas = """
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sala_id INTEGER,
        fecha DATE,
        hora_inicio TIME,
        hora_fin TIME,
        responsable TEXT,
        descripcion TEXT,
        estado TEXT DEFAULT 'activa',
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sala_id) REFERENCES salas(id)
    )
    """

    db.ejecutar(sql_salas)
    db.ejecutar(sql_reservas)

def insertar_salas_prueba():

    db = ConexionBD()

    salas = [
        ("Aula 101", 30),
        ("Aula 102", 40),
        ("Sala de Juntas", 15)
    ]

    for sala in salas:
        try:
            db.ejecutar(
                "INSERT INTO salas(nombre, capacidad) VALUES (?,?)",
                sala
            )
        except:
            pass

def obtener_salas():

    db = ConexionBD()

    sql = "SELECT * FROM salas"

    return db.consultar(sql)


def insertar_reserva(sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion):

    db = ConexionBD()

    sql = """
    INSERT INTO reservas
    (sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    return db.ejecutar(sql, (sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion))

def obtener_reservas_por_fecha(fecha):

    db = ConexionBD()

    sql = """
    SELECT * FROM reservas
    WHERE fecha = ?
    """

    return db.consultar(sql, (fecha,))

def validar_solapamiento(sala_id, fecha, hora_inicio, hora_fin):

    db = ConexionBD()

    sql = """
    SELECT * FROM reservas
    WHERE sala_id = ?
    AND fecha = ?
    AND estado = 'activa'
    AND hora_inicio < ?
    AND hora_fin > ?
    """

    reservas = db.consultar(sql, (sala_id, fecha, hora_fin, hora_inicio))

    return len(reservas) > 0
#True → hay conflicto
#False → la sala está libre


def actualizar_reserva(id_reserva, sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion):

    db = ConexionBD()

    sql = """
    UPDATE reservas
    SET sala_id = ?, fecha = ?, hora_inicio = ?, hora_fin = ?, responsable = ?, descripcion = ?
    WHERE id = ?
    """

    db.ejecutar(sql, (sala_id, fecha, hora_inicio, hora_fin, responsable, descripcion, id_reserva))

    return True

def eliminar_reserva(id_reserva):

    db = ConexionBD()

    sql = """
    UPDATE reservas
    SET estado = 'cancelada'
    WHERE id = ?
    """

    db.ejecutar(sql, (id_reserva,))

    return True

def obtener_reserva_por_id(id_reserva):

    db = ConexionBD()

    sql = """
    SELECT * FROM reservas
    WHERE id = ?
    """

    resultado = db.consultar(sql, (id_reserva,))

    if resultado:
        reserva = resultado[0]

        return {
            "id": reserva[0],
            "sala_id": reserva[1],
            "fecha": reserva[2],
            "hora_inicio": reserva[3],
            "hora_fin": reserva[4],
            "responsable": reserva[5],
            "descripcion": reserva[6],
            "estado": reserva[7]
        }

    return None


def insertar_sala(nombre, capacidad):

    db = ConexionBD()

    sql = """
    INSERT INTO salas(nombre, capacidad)
    VALUES (?, ?)
    """

    return db.ejecutar(sql, (nombre, capacidad))


def insertar_sala(nombre, capacidad):

    db = ConexionBD()

    sql = """
    INSERT INTO salas(nombre, capacidad)
    VALUES (?, ?)
    """

    return db.ejecutar(sql, (nombre, capacidad))

if __name__ == "__main__":

    crear_tablas()
    insertar_salas_prueba()

    print("Salas:", obtener_salas())

    reserva_id = insertar_reserva(
        1,
        "2026-03-20",
        "09:00",
        "11:00",
        "Juan",
        "Clase"
    )

    print("Reserva creada:", reserva_id)

    print("Reserva:", obtener_reserva_por_id(reserva_id))

    actualizar_reserva(
        reserva_id,
        1,
        "2026-03-20",
        "10:00",
        "12:00",
        "Juan",
        "Clase actualizada"
    )

    print("Reserva actualizada:", obtener_reserva_por_id(reserva_id))