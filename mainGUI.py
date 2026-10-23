import sys
from proc import *
from tkinter import *
from tkinter import messagebox

user = None
frame_izq = None
frame_der = None

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

    messagebox.showwarning(title = None, message = "Bienvenido mi bri")
    mainScreen()


def mainScreen():
    root.geometry("800x600")
    container1.destroy()
    
    root.grid_columnconfigure(0, weight=35)
    root.grid_columnconfigure(1, weight=65)
    root.grid_rowconfigure(0, weight=1)

    frame_izq = Frame(root)
    frame_izq.grid(row=0, column=0, sticky="nsew")

    frame_der = Frame(root)
    frame_der.grid(row=0, column=1, sticky="nsew")

    Label(frame_izq, text="Acciones disponibles").grid(row=0, column=0, sticky="nsew", columnspan=3)

    if isAdmin(user.id):
        boton = Button(
            frame_izq,
            text="Buscar equipo",
            command=...,
        ).grid(row=1, column=0, sticky="nsew", padx=5, columnspan=3)

root = Tk()
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


root.mainloop()


