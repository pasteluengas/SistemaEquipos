# TODO CONVERTIR A SQLLITE3

import json
import sqlite3


con = sqlite3.connect("data.db")
dbcur = con.cursor()

def getFetch(strreq, mode):
    res = dbcur.execute(strreq)
    if mode == "ALL":
        return res.fetchall()
    if mode == "ONE":
        return res.fetchone()


#FUNCIONES GENERALES PUEDEN EJECUTARSE SIN SER USUARIO
'''
INICIALIZA BASES DE DATOS (lo hacia)
'''
def init_db():
    ...

'''

OBTENER INFO DE USUARIO POR SU ID
DEVUELVE UN DICCIONARIO CON INFO [OMITIENDO INFO SENSIBLE COMO CONTRASENAS Y CORREOS] EN CASO DE EXITO
DE LO CONTRARIO DEVUELVE -1
'''
def getUser(id):
    global con
    global dbcur

    request = f"SELECT * FROM usuarios WHERE id = {id}"
    result = getFetch(request, "ONE")
    

    if result is None:
        return -1

    toRet = {}
    toRet["id"] = result[0]
    toRet["user"] = result[1]
    if result[3] == 0:    
        toRet["isAdmin"] = False
    if result[3] == 1:
        toRet["isAdmin"] = True

    return toRet


'''
OBTENER INFO DE EQUIPO POR SU ID
DEVUELVE UN DICCIONARIO CON INFO [OMITIENDO INFO SENSIBLE COMO SOLICITUDES] EN CASO DE EXITO
DE LO CONTRARIO DEVUELVE -1
'''
def getEquipo(id):
    global con
    global dbcur

    request = f"SELECT * FROM equipo WHERE id = {id}"
    result = getFetch(request, "ONE")
    

    if result is None:
        return -1

    toRet = {}
    toRet["id"] = result[0]
    toRet["nombre"] = result[1]
    toRet["descripcion"] = result[3]
    toRet["poseedor"] = result[5]

    return toRet
    


'''
OBTENER INFO DE USUARIOS POR SU NOMBRE DE USUARIO
SI ENCUENTRA EL USUARIO DEVUELVE EL ID
SI NO LO ENCUENTRA DEVUELVE -1
'''
def getIdByUser(user):
    global con
    global dbcur
    
    request = f"SELECT * FROM usuarios WHERE user = '{user}'"
    result = getFetch(request, "ONE")

    if result is None:
        return -1

    return result[0]


'''
REVISA SI EL USUARIO ES ADMIN
SI ES ADMIN DEVUELVE TRUE
SINO FALSE
'''
def isAdmin(id):
    global con
    global dbcur
    
    request = f"SELECT * FROM usuarios WHERE id = '{id}'"
    result = getFetch(request, "ONE")

    if result == None:
        return -1
    
    if result[3] == 1:
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

        global con
        global dbcur
        
        request = f"SELECT * FROM usuarios WHERE user = '{user}' AND pwd = '{pwd}'"
        result = getFetch(request, "ONE")

        if result is None:
            self.error = -2
            return

        self.id = result[0]
        self.usuario = result[1]
        self.isAdmin = isAdmin(id)
        
    '''
        TIPOS DE CONSULTA
        0 = BUSCAR POR NOMBRE
        1 = BUSCAR POR CATEGORIA

        DEVUELVE
        DICCIONARIO DEL EQUIPO EN CASO DE ENCONTRARLO
        -1 EN CASO DE ERROR
    '''
    def consultar(self, req, tipo_consulta):
        global equipo
        #print(equipo)
        if tipo_consulta == 0:
            consulta = "nombre"
        if tipo_consulta == 1:
            consulta = "categoria"

        global con
        global dbcur
        request = f"SELECT * FROM equipo WHERE {consulta} = '{req}'"
        result = getFetch(request, "ONE")

        if result is None:
            return -1

        toRet = {}
        toRet["id"] = result[0]
        toRet["nombre"] = result[1]
        toRet["estado"] = result[2]
        toRet["descripcion"] = result[3]
        toRet["categoria"] = result[4]
        toRet["poseedor"] = result[5]

        return toRet


    '''
    GUARDA EL CONTENIDO DE LAS LISTAS DE NUEVO EN EL TXT (ya no lo hace)
    '''
    def actualizar(self):
        ...

    
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
        if getEquipo(id)["poseedor"] != 0:
            return -1

        global con
        global dbcur
        
        request = f"SELECT * FROM solicitudes WHERE id_equipo = {id} AND id_usuario = {self.id}"
        result = getFetch(request, "ONE")
        
        if result is not None:
            return -2
        
        #equipo[id]["solicitudes"].append(self.id)
        request = f"""
            INSERT INTO solicitudes (id_usuario, id_equipo) VALUES ({self.id}, {id})
        """
        dbcur.execute(request)
        con.commit()

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
        '''
        for eq in equipo:
            if eq["solicitudes"]:
                toRet[eq["id"]] = eq["solicitudes"]
        '''
        global con
        global dbcur
        request = f"SELECT * FROM solicitudes"
        result = getFetch(request, "ALL")

        for eq in result:
            toRet[eq[2]] = []

        for eq in result:
            toRet[eq[2]].append(eq[1]) 

        return toRet

    '''
    ELIMINA LA SOLICITUD DEL USUARIO Y LO COLOCA COMO POSEEDOR
    DEVUELVE 0 EN CASO DE EXITO Y -1 EN CASO DE NO EXITO
    '''
    def aceptar_solicitud(self, id_equipo, id_usuario):
        global con
        global dbcur

        request = f"SELECT * FROM solicitudes WHERE id_equipo = {id_equipo} AND id_usuario = {id_usuario}"
        result = getFetch(request, "ONE")

        if request is None:
            return -1
        
        request = f"DELETE FROM solicitudes WHERE id_usuario = {id_usuario} AND id_equipo = {id_equipo}"
        dbcur.execute(request)
        con.commit()

        request = f"UPDATE equipo SET poseedor = {id_usuario} WHERE id = {id_equipo}"
        dbcur.execute(request)
        con.commit()
        
        return 0


    
    '''
    CONVIERTE EL POSEEDOR DEL EQUIPO A 0 (QUE ES EL ID DEL ADMIN)
    EN CASO DE EXITO DEVUELVE 0 Y -1 SINO
    '''
    def devolver_equipo(self, id_equipo):
        global con
        global dbcur
        
        request = f"SELECT * FROM equipo WHERE id = {id_equipo}"
        result = getFetch(request, "ONE")

        if result[5] == 0:
            return -1

        request = f"UPDATE equipo SET poseedor = 0 WHERE id = {id_equipo}"
        dbcur.execute(request)
        con.commit()

        return 0

