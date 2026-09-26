import json

usuarios = []
equipo = []

#FUNCIONES GENERALES PUEDEN EJECUTARSE SIN SER USUARIO
'''
INICIALIZA BASES DE DATOS, EXTRAE EL CONTENIDO DE LOS TXT Y LO GUARDA EN LISTAS
'''
def init_db():
    global usuarios
    global equipo

    with open("usuarios.txt", "r", encoding="utf-8") as archivo:
        usuarios = json.load(archivo)

    with open("equipo.txt", "r", encoding="utf-8") as archivo:
        equipo = json.load(archivo)

'''
OBTENER INFO DE USUARIO POR SU ID
DEVUELVE UN DICCIONARIO CON INFO [OMITIENDO INFO SENSIBLE COMO CONTRASENAS Y CORREOS] EN CASO DE EXITO
DE LO CONTRARIO DEVUELVE -1
'''
def getUser(id):
    try:
        toRet = {}
        toRet["id"] = usuarios[id]["id"]
        toRet["user"] = usuarios[id]["user"]
        toRet["isAdmin"] = usuarios[id]["isAdmin"]
    except:
        toRet = -1
    return toRet

'''
OBTENER INFO DE EQUIPO POR SU ID
DEVUELVE UN DICCIONARIO CON INFO [OMITIENDO INFO SENSIBLE COMO POSEEDOR Y SOLICITUDES] EN CASO DE EXITO
DE LO CONTRARIO DEVUELVE -1
'''
def getEquipo(id):
    try:
        toRet = {}
        toRet["id"] = equipo[id]["id"]
        toRet["nombre"] = equipo[id]["nombre"]
        toRet["descripcion"] = equipo[id]["descripcion"]
    except:
        toRet = -1
    return toRet


'''
OBTENER INFO DE USUARIOS POR SU NOMBRE DE USUARIO
SI ENCUENTRA EL USUARIO DEVUELVE EL ID
SI NO LO ENCUENTRA DEVUELVE -1
'''
def getIdByUser(user):
    for i in range(0, len(usuarios)):
        if usuarios[i]["user"] == user:
            return usuarios[i]["id"]
    return -1

'''
REVISA SI EL USUARIO ES ADMIN
SI ES ADMIN DEVUELVE TRUE
SINO FALSE
'''
def isAdmin(id):
    if usuarios[id]["isAdmin"] == True:
        return True
    return False



'''
Errores de Usuario:
0: Sin errores
-1: Usuario no encontrado
-2: contrasena incorrecta
-3: Datos no concuerdan (Estudiante intentando entrar como encargado y viceversa)
'''
class Usuario():
    def __init__(self, user, pwd):
        init_db()
        self.error = 0
        self.isAdmin = False
        id = getIdByUser(user)
        if id == -1:
            self.error = -1
            return

        if usuarios[id]["pwd"] != pwd:
            self.error = -2
            return

        self.id = usuarios[id]["id"]
        self.usuario = usuarios[id]["user"]
        self.isAdmin = usuarios[id]["isAdmin"]
        self.multa = usuarios[id]["multa"]
        self.libros = usuarios[id]["libros"]
        self.isAdmin = isAdmin(id)
        print(self.isAdmin)

    '''
        TIPOS DE CONSULTA
        0 = BUSCAR POR NOMBRE
        1 = BUSCAR POR CATEGORIA

        DEVUELVE
        DICCIONARIO DEL EQUIPO EN CASO DE ENCONTRARLO
        -1 EN CASO DE ERROR
    '''
    def consultar(self, consulta, tipo_consulta):
        for eq in equipo:
            if tipo_consulta == 0 and eq["nombre"] == consulta:
                return eq
            if tipo_consulta == 1 and eq["categoria"] == consulta:
                return eq
        return -1

    '''
    GUARDA EL CONTENIDO DE LAS LISTAS DE NUEVO EN EL TXT
    '''
    def actualizar(self):
        global usuarios
        global equipo
        with open("equipo.txt", "w", encoding="utf-8") as archivo:
            json.dump(equipo, archivo, ensure_ascii=False, indent=4)


        with open("usuarios.txt", "w", encoding="utf-8") as archivo:
            json.dump(usuarios, archivo, ensure_ascii=False, indent=4)

    
class Estudiante(Usuario):
    def __init__(self, user, pwd):
        super().__init__(user, pwd)
        if self.isAdmin:
            self.error = -3
            return

    '''
    SOLICITAR UN EQUIPO SIENDO ESTUDIANTE
    SI SE PUEDE SOLICITAR DE AÑADE A LA LISTA DE SOLICITUDES Y DEVUELVE 0
    ERRORES:
    -1: EL EQUIPO NO ESTA DISPONIBLE
    -2: EL ESTUDIANTE YA ESTA EN LA LISTA DE SOLICITUDES
    '''
    def solicitar(self, id):
        if equipo[id]["poseedor"] != 0:
            return -1
        
        if self.id in equipo[id]["solicitudes"]:
            return -2
        
        equipo[id]["solicitudes"].append(self.id)
        self.actualizar()
        return 0

class Encargado(Usuario):
    def __init__(self, user, pwd):
        super().__init__(user, pwd)
        if not self.isAdmin:
            self.error = -3
            return

    '''
    DEVUELVE UN DICCIONARIO CON TODAS LAS SOLICITUDES
    '''
    def revisar_solicitudes(self):
        toRet = {}
        for eq in equipo:
            if eq["solicitudes"]:
                toRet[eq["id"]] = eq["solicitudes"]
        return toRet

    '''
    ELIMINA LA SOLICITUD DEL USUARIO Y LO COLOCA COMO POSEEDOR
    DEVUELVE 0 EN CASO DE EXITO Y -1 EN CASO DE NO EXITO
    '''
    def aceptar_solicitud(self, id_equipo, id_usuario):
        if id_usuario not in equipo[id_equipo]["solicitudes"]:
            return -1
        equipo[id_equipo]["solicitudes"].remove(id_usuario)
        equipo[id_equipo]["poseedor"] = id_usuario
        self.actualizar()
        return 0
    
    '''
    CONVIERTE EL POSEEDOR DEL EQUIPO A 0 (QUE ES EL ID DEL ADMIN)
    EN CASO DE EXITO DEVUELVE 0 Y -1 SINO
    '''
    def devolver_equipo(self, id_equipo):
        if equipo[id_equipo]["poseedor"] == 0:
            return -1
        equipo[id_equipo]["poseedor"] = 0
        self.actualizar()
        return 0
        

