'''
import proc

def mainestudiante():
    estudiante = proc.Estudiante("jerry123", "12345")

    if estudiante.error != 0:
        print("Error", estudiante.error)
        return

    print("pasa")

    if proc.isAdmin(estudiante.id):
        print("oh y eres admin")
    else:
        print("hola esclavo")

    print("Ahora unas consultas")
    res = estudiante.consultar("amplificadores", 1)
    print(res)

    print("y una solicitud")
    sol = estudiante.solicitar(res["id"])
    if sol == 0:
        print("exito en solicitar")
    if sol == -1:
        print("No se puede solicitar")
    if sol == -2:
        print("ud ya lo solicito")


def mainencargado():
    encargao = proc.Encargado("Admin", "contrasena123")
    if encargao.error != 0:
        print("Error", encargao.error)
        return
    print("Ahora unas consultas")
    res = encargao.consultar("amplificadores", 1)
    print(res)
    print("a revisar solicitudes")
    print(encargao.revisar_solicitudes())
    print("a aprobar solicitudes")

    r = encargao.devolver_equipo(1)

    r = encargao.aceptar_solicitud(0, 1)
    if r == -1:
        print("Parece que el usuario no esta solicitando ese mierda")
        return
    print("el usuario ahgora es poseedor lalol")
    print("el usuario ya devolvio el equipoi")
    r = encargao.devolver_equipo(0)
    if r == -1:
        print("Parece que el equipo no se fue")
        return
    print("El equipo regreso!")

proc.init_db()
print(proc.getEquipo(1))
inpu = input("estudiante/encargado: ")
if inpu == "estudiante":
    mainestudiante()
if inpu == "encargado":
    mainencargado()

'''


import json
import sqlite3

# 1. Datos en formato JSON proporcionados
usuarios_json = [
    {
        "id": 0,
        "user": "Admin",
        "pwd": "contrasena123",
        "isAdmin": True,
        "correo": "realadmin@gmail.com",
        "multa": 0,
        "libros": [],
    },
    {
        "id": 1,
        "user": "jerry123",
        "pwd": "12345",
        "isAdmin": False,
        "correo": "correon@gmail.com",
        "multa": 0,
        "libros": [],
    },
]

equipoc_json = [
    {
        "id": 0,
        "nombre": "Amplificador LM386",
        "estado": 5,
        "descripcion": (
            "Amplificador de audio LM386 en formato DIP-8, Texas Instruments"
        ),
        "categoria": "amplificadores",
        "solicitudes": [],
        "poseedor": 0,
    },
    {
        "id": 1,
        "nombre": "Cable HDMI",
        "estado": 3,
        "descripcion": "Cable HDMI Marca generica, daño en una de las puntas.",
        "categoria": "cables",
        "solicitudes": [],
        "poseedor": 0,
    },
]

# 2. Conexión a la base de datos SQLite (crea el archivo 'inventario.db' si no existe)
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

# 3. Crear tabla 'usuarios'
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        user TEXT NOT NULL,
        pwd TEXT NOT NULL,
        isAdmin BOOLEAN NOT NULL,
        correo TEXT,
        multa INTEGER,
        libros TEXT
    )
""")

# 4. Crear tabla 'equipoc'
cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipoc (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        estado INTEGER,
        descripcion TEXT,
        categoria TEXT,
        solicitudes TEXT,
        poseedor INTEGER,
        FOREIGN KEY (poseedor) REFERENCES usuarios(id)
    )
""")

# 5. Insertar datos en 'usuarios'
# Nota: Los campos de tipo lista (como 'libros') se convierten a JSON string para almacenarlos
for u in usuarios_json:
  cursor.execute(
      """
        OR IGNORE INTO usuarios (id, user, pwd, isAdmin, correo, multa, libros)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
      (
          u["id"],
          u["user"],
          u["pwd"],
          1 if u["isAdmin"] else 0,
          u["correo"],
          u["multa"],
          json.dumps(u["libros"]),
      ),
  )

# 6. Insertar datos en 'equipoc'
# Nota: Los campos de tipo lista (como 'solicitudes') también se guardan como texto JSON
for e in equipoc_json:
  cursor.execute(
      """
        INSERT OR IGNORE INTO equipoc (id, nombre, estado, descripcion, categoria, solicitudes, poseedor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
      (
          e["id"],
          e["nombre"],
          e["estado"],
          e["descripcion"],
          e["categoria"],
          json.dumps(e["solicitudes"]),
          e["poseedor"],
      ),
  )

# 7. Guardar cambios y cerrar conexión
conexion.commit()
conexion.close()

print(
    "¡Base de datos 'inventario.db' creada y datos guardados exitosamente con"
    " éxito!"
)
