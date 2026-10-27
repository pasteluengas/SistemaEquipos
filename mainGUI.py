import random
jaja = ['"esp32 es solo una moda pasajera, en 2018 todos volveran a usar arduino" - Mahatma Gandhi', '"El logo de Java es un cafe porque a los programadores de Java no les pagan las horas nocturnas" - Jorge Eliecer Gaitán', '"Reconocida empresa del sector solicita programador senior de entre 13 y 15 años" - José Asunción Silva', '"Ya funciona Fortnite en Linux? Tengo un sueño" - Martin Luther King']

import sys
from proc import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

user = None
frame_izq = None
frame_der = None

class mainScreenController:
    def __init__(self, frame, user):
        self.frame = frame
        self.user = user

    def clean(self, arr=0):
        if arr == 0:
            frame = self.frame
            for widget in frame.winfo_children():
                        widget.destroy()
            return

        frame = arr
        for widget in frame.winfo_children():
                    widget.destroy()
        

    def buscarequipo(self):
        tipobusqueda = IntVar(value=1)
        searchinput = StringVar()
        changeable = "que"
        
        def displayreturn():
            nonlocal changeable #quien penso que esto era una buena idea?
            if changeable != "que":
                self.clean(changeable)
            
            func = self.user.consultar(searchinput.get().lower(), tipobusqueda.get())
            changeable = Frame(self.frame, bg="white")
            changeable.grid(row=4, column=0, sticky="nsew", columnspan=3)
            
            if func == -1:
                Label(changeable, text="No se encontraron resultados", bg="white", fg="black").grid(row=0, column=0)
            else:
                print(func)
                ttk.Separator(changeable, orient="horizontal").grid(row=0, column=0, sticky="ew", pady=10)
                Label(changeable, text="ID: " + str(func["id"]), bg="white", fg="black", justify="left", anchor="w").grid(row=1, column=0, sticky="nsew", columnspan=2)
                Label(changeable, text=func["nombre"], bg="white", fg="black", font=("Arial", 15, "bold"), justify="left", anchor="w").grid(row=2, column=0, sticky="nsew", columnspan=2)

                disponibilidad = "Disponible" if func["poseedor"] == 0 else "No disponible"
                if func["poseedor"] != 0 and self.user.isAdmin == True:
                    disponibilidad = disponibilidad + "(" + (getUser(func["poseedor"])["user"])  + ")"
                
                Label(changeable, text=disponibilidad, bg="white", fg="black", justify="left", anchor="w").grid(row=3, column=0, sticky="nsew", columnspan=2)
                Label(changeable, text="Estado: " + str(func["estado"]) + "/5", bg="white", fg="black", justify="left", anchor="w").grid(row=3, column=1, sticky="nsew", columnspan=2)
                
                Label(changeable, text=func["descripcion"], bg="white", fg="black", justify="left", anchor="w").grid(row=4, column=0, sticky="nsew", columnspan=2)

                if func["poseedor"] != 0 and self.user.isAdmin == True:
                    Button(changeable, text="Reportar devolución", command=lambda: devolucion(func["id"])).grid(row=5, column=0, sticky="nsew", columnspan=2)
                    
                if func["poseedor"] == 0 and self.user.isAdmin == False:
                    Button(changeable, text="Solicitar equipo", command=lambda:solicitud(func["id"])).grid(row=5, column=0, sticky="nsew", columnspan=2)

        def devolucion(id):
            func_devolver = self.user.devolver_equipo(id)
            if func_devolver == 0:
                messagebox.showinfo(title = None, message = "Equipo devuelto! Marcado como Disponible")
            else:
                messagebox.showerror(title = None, message = "No se pudo devolver el equipo. Error: " + str(func_devolver))

        def solicitud(id):
            func_solicitud = self.user.solicitar(id)
            if func_solicitud == 0:
                messagebox.showinfo(title = None, message = "Equipo solicitado!")
            elif func_solicitud == -2:
                messagebox.showwarning(title = None, message = "Usted ya ha solicitado este equipo.")
            else:
                messagebox.showerror(title = None, message = "No se pudo solicitar el equipo. Error: " + str(func_solicitud))
    
        self.clean()
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)

        Label(self.frame, text="Buscar un equipo", bg="white", fg="black", font=("Arial", 20, "bold"), justify="left", anchor="w").grid(row=0, column=0, sticky="nsew", columnspan=2)
        Label(self.frame, text="Nombre/Categoría", bg="white", fg="black", justify="left", anchor="w").grid(row=1, column=0, sticky="nsew")
        searchinput = Entry(self.frame)
        searchinput.grid(row=1, column=1, sticky="nsew", columnspan=2)


        
        Label(self.frame, text="Buscaro por: ", bg="white", fg="black").grid(row=2, column=0, sticky="nsew")
        Radiobutton(self.frame, text="Nombre", variable=tipobusqueda, value=0, bg="white", fg="black").grid(row=2, column=1, sticky="nsew")
        Radiobutton(self.frame, text="Categoría", variable=tipobusqueda, value=1, bg="white", fg="black").grid(row=2, column=2, sticky="nsew")
        
        Button(self.frame, text="Buscar", command=displayreturn, fg="black").grid(row=3, column=0, sticky="nsew", columnspan=3)

    def ver_solicitudes(self):
        def aceptar(id_equipo, id_usuario):
            result = self.user.aceptar_solicitud(id_equipo, id_usuario)
            if result == 0:
                messagebox.showinfo(title = None, message = "Solicitud aprobada! Marcado como No Disponible")
            else:
                messagebox.showerror(title = None, message = "No se pudo aprobar la solicitud. Error: " + str(result))
                self.frame.update_idletasks()
    
        self.clean()
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        
        Label(self.frame, text="Revisar solicitudes", bg="white", fg="black", font=("Arial", 20, "bold"), justify="left", anchor="w").grid(row=0, column=0, sticky="nsew", columnspan=2)


        sol = self.user.revisar_solicitudes()

        Label(self.frame, text="Equipo", font=("TkDefaultFont", 12, "bold"), bg="white", fg="black").grid(row=1, column=0, sticky="nsew")
        Label(self.frame, text="Usuario", font=("TkDefaultFont", 12, "bold"), bg="white", fg="black").grid(row=1, column=1, sticky="nsew")
        Label(self.frame, text="Acción", font=("TkDefaultFont", 12, "bold"), bg="white", fg="black").grid(row=1, column=2, sticky="nsew")

        rowcounter = 2
        for eq, us in sol.items():
            print(f"Equipo: {eq}, Usuario: {us}")
            for user in us:
                Label(self.frame, text=str(getEquipo(eq)["nombre"]), font=("TkDefaultFont", 12), bg="white", fg="black").grid(row=rowcounter, column=0, sticky="nsew")
                Label(self.frame, text=str(getUser(user)["user"]), font=("TkDefaultFont", 12), bg="white", fg="black").grid(row=rowcounter, column=1, sticky="nsew")
                Button(self.frame, text="Aceptar solicitud", font=("TkDefaultFont", 12), fg="black", command=lambda: aceptar(eq, user)).grid(row=rowcounter, column=2, sticky="nsew")
                rowcounter += 1
                
            
    def anadir_equipo(self):
        def anadir(name_entry, desc_entry, combostate, categ_entry):
            #revisar inputs
            if not name_entry.get() or not desc_entry.get() or not categ_entry.get():
                messagebox.showerror(title = None, message = "Debe rellenar todas las casillas.")
                return
            
            #procesar inputs
            name = name_entry.get().lower()
            desc = desc_entry.get().lower()
            categ = categ_entry.get().lower()

            #realizar req
            self.user.anadir_equipo(name, desc, combostate.get(), categ)

            #mostrar ventanita
            messagebox.showinfo(title = None, message = "Equipo añadido a la base de datos.")

            #limpiar
            name_entry.insert(0, "")
            desc_entry.insert(0, "")
            categ_entry.insert(0, "")


        self.clean()
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)

        Label(self.frame, text="Añadir un equipo", bg="white", fg="black", font=("Arial", 20, "bold"), justify="left", anchor="w").grid(row=0, column=0, sticky="nsew", columnspan=3)

        Label(self.frame, text="Nombre: ", bg="white", fg="black").grid(row=1, column=0, sticky="nsew")
        name = Entry(self.frame)
        name.grid(row=1, column=1, sticky="nsew")

        Label(self.frame, text="Descripcion: ", bg="white", fg="black").grid(row=2, column=0, sticky="nsew")
        desc = Entry(self.frame)
        desc.grid(row=2, column=1, sticky="nsew", columnspan=2)

        Label(self.frame, text="Estado: ", bg="white", fg="black").grid(row=3, column=0, sticky="nsew")
        estado= ttk.Combobox(self.frame, values=[1, 2, 3, 4, 5], state="readonly")
        estado.current(4) # state="readonly" evita que el usuario escriba texto libre
        estado.grid(row=3, column=1, padx=20, pady=20)
        Label(self.frame, text=" de 5 ", bg="white", fg="black").grid(row=3, column=2, sticky="nsew")

        Label(self.frame, text="Categoria: ", bg="white", fg="black").grid(row=4, column=0, sticky="nsew")
        categ = Entry(self.frame)
        categ.grid(row=4, column=1, sticky="nsew", columnspan=2)

        Button(self.frame, text="Añadir equipo", command=lambda: anadir(name, desc, estado, categ)).grid(row=5, column=0, sticky="nsew", columnspan=3)
        
        
def gtfo():
    if not messagebox.askyesno("Confirmar salida", "¿Está seguro que quiere salir de su sesión?"):
        return

    print("[procediendo al gtfo]")
    global container1, rootuser, rootpwd, rooterrorlabel, boton, root, user

    #matar al usuario
    del user

    #reiniciar todo
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Equipos de laboratorio")
    root.geometry("350x250")
    #root.configure(bg="#555b67")

    container1 = Frame(root, bd=2, relief="groove")
    container1.pack(fill="x", padx=10, pady=10, expand=True)
    container1.columnconfigure(0, weight=1)

    Label(container1, text="Inicio de sesión | Equipos de laboratorio").grid(row=0, column=0, sticky="nsew", columnspan=3)

    Label(container1, text="Usuario: ").grid(row=1, column=0, sticky="nsew", padx=5)
    rootuser = Entry(container1)
    rootuser.grid(row=1, column=1, sticky="nsew", padx=5)

    Label(container1, text="Contraseña: ").grid(row=2, column=0, sticky="nsew", padx=5)
    rootpwd = Entry(container1, show="*")
    rootpwd.grid(row=2, column=1, sticky="nsew", padx=5, columnspan=3)

    rooterrorlabel = Label(container1, text="Inicio de sesión | Equipos de laboratorio")
    rooterrorlabel.grid(row=0, column=0, sticky="nsew", columnspan=3)

    boton = Button(
        container1,
        text="Ingresar",
        command=startuser,
    ).grid(row=3, column=0, sticky="nsew", padx=5, columnspan=3)

    for child in container1.winfo_children():
        child.grid_configure(padx=10, pady=10)   
        

def startuser():
    global rooterrorlabel, user
    id_user = getIdByUser(rootuser.get())
    print(id_user)

    if id_user == -1:
        messagebox.showerror(title=None, message="Usuario o contraseña incorrecta")
        return

    if isAdmin(id_user):
        user = Encargado(rootuser.get(), rootpwd.get())
    else:
        user = Estudiante(rootuser.get(), rootpwd.get())

    if user.error != 0:
        messagebox.showerror(title=None, message="Usuario o contraseña incorrecta")
        return

    messagebox.showinfo(title = None, message = "Bienvenido mi bri")
    mainScreen()


def mainScreen():
    #global gtfo
    root.geometry("800x600")
    container1.destroy()
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=99)
    root.grid_rowconfigure(0, weight=1)

    frame_izq = Frame(root)
    frame_izq.grid(row=0, column=0, sticky="nsew")

    frame_der = Frame(root, bg="white")
    frame_der.grid(row=0, column=1, sticky="nsew")
    controlVentana = mainScreenController(frame_der, user)

    frame_izq.columnconfigure(0, weight=1)

    Label(frame_izq, text="Logeado como: "  + user.usuario).grid(row=0, column=0, sticky="nsew", columnspan=3)
    

    if isAdmin(user.id):
        boton = Button(
            frame_izq,
            text="Buscar equipo",
            command= lambda: controlVentana.buscarequipo(),
        ).grid(row=1, column=0, sticky="nsew", padx=5)

        boton = Button(
            frame_izq,
            text="Añadir requipo",
            command=lambda: controlVentana.anadir_equipo(),
        ).grid(row=2, column=0, sticky="nsew", padx=5)

        boton = Button(
            frame_izq,
            text="Revisar solicitudes",
            command=lambda: controlVentana.ver_solicitudes(),
        ).grid(row=3, column=0, sticky="nsew", padx=5)

        boton = Button(
            frame_izq,
            text="Cerrar sesión",
            command=gtfo,
        ).grid(row=5, column=0, sticky="nsew", padx=5)


    if isAdmin(user.id) == False:
        boton = Button(
            frame_izq,
            text="Buscar equipo",
            command= lambda: controlVentana.buscarequipo(),
        ).grid(row=1, column=0, sticky="nsew", padx=5)

        boton = Button(
            frame_izq,
            text="Cerrar sesión",
            command=gtfo,
        ).grid(row=5, column=0, sticky="nsew", padx=5)


    Label(frame_der, text="Bienvenido/a " + user.usuario, bg="white", fg="black", font=("Arial", 20, "bold"), justify="left", anchor="w").grid(row=0, column=0, sticky="nsew")
    Label(frame_der, text=jaja[random.randint(0, len(jaja)-1)], bg="white", fg="black", font=("Arial", 12)).grid(row=1, column=0, sticky="nsew")
        

##### YA QUE JAJA
root = Tk()
root.title("Equipos de laboratorio")
root.geometry("350x250")

container1 = Frame(root, bd=2, relief="groove")
container1.pack(fill="x", padx=10, pady=10, expand=True)
container1.columnconfigure(0, weight=1)

Label(container1, text="Inicio de sesión | Equipos de laboratorio").grid(row=0, column=0, sticky="nsew", columnspan=3)

Label(container1, text="Usuario: ").grid(row=1, column=0, sticky="nsew", padx=5)
rootuser = Entry(container1)
rootuser.grid(row=1, column=1, sticky="nsew", padx=5)

Label(container1, text="Contraseña: ").grid(row=2, column=0, sticky="nsew", padx=5)
rootpwd = Entry(container1, show="*")
rootpwd.grid(row=2, column=1, sticky="nsew", padx=5, columnspan=3)

rooterrorlabel = Label(container1, text="Inicio de sesión | Equipos de laboratorio")
rooterrorlabel.grid(row=0, column=0, sticky="nsew", columnspan=3)

boton = Button(
    container1,
    text="Ingresar",
    command=startuser,
).grid(row=3, column=0, sticky="nsew", padx=5, columnspan=3)

for child in container1.winfo_children():
    child.grid_configure(padx=10, pady=10)


root.mainloop()


