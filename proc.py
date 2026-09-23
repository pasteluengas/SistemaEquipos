import json

users = []
gear = []

def getIdByUser(id):
    for user in users:
        if user["id"] == id:
            return id
        return -1

'''
Errores de Usuario:
0: Sin errores
-1: Usuario no encontrado
-2: contrasena incorrecta
'''
class Usuario():
    def __init__(self, user, pwd):
        self.error = 0

        checkid = getIdByUser()
        if id == -1:
            self.error = -1
            return

        if users[id]["pwd"] != pwd:
            self.error = -2
            return

        self.id = users[id]["id"]
        self.usuario = users[id]["user"]
        self.isAdmin = users[id]["isAdmin"]
        self.multa = users[id]["multa"]
        self.libros = users[id]["libros"]

    def consular(self, consulta):
        #hace luego
        pass

    def solicitar(self, id):
        #hhace lueg
        pass

    def actualizar(self):
        #haceluyego
        pass

    def cerrar_sesion():
        with open("usuarios.txt", "w", encoding="utf-8") as archivo:
            json.dump(users, archivo, ensure_ascii=False, indent=4)

        
        
        



def start():
    global users
    global gear
    with open("equipo.txt", "w", encoding="utf-8") as archivo:
        json.dump(gear, archivo, ensure_ascii=False, indent=4)


    with open("usu.txt", "w", encoding="utf-8") as archivo:
            json.dump(gear, archivo, ensure_ascii=False, indent=4)

    #with open("usuarios.txt", "r", encoding="utf-8") as archivo:
    #    users = json.load(archivo)

    

    print(gear[0]["nombre"])

if __name__ == "__main__":
    start()
