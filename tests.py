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

