import sys
from proc import Estudiante, Encargado, getIdByUser, getUser, init_db, getEquipo

def main():
    init_db()
    
    print("=== SISTEMA DE GESTION DE EQUIPOS ===")
    
    usuario_instancia = None
    
    while usuario_instancia is None:
        print("\n--- INICIO DE SESION ---")
        usr = input("▶ Usuario [Dejar en blanco para salir]: ")

        if not usr:
            return
        
        id_user = getIdByUser(usr)
        if id_user == -1:
            print("Error: El usuario no existe.")
            continue
            
        info = getUser(id_user)
        if info == -1:
            print("Error al obtener datos del usuario.")
            continue

        pwd = input("▶ Contrasena: ")
            
        if info["isAdmin"]:
            temp = Encargado(usr, pwd)
        else:
            temp = Estudiante(usr, pwd)
            
        if temp.error == -2:
            print("Error: Contrasena incorrecta.")
        elif temp.error == 0:
            usuario_instancia = temp
            print("\nBienvenido/a " + usuario_instancia.usuario)
        else:
            print("Error al iniciar sesion.")

    while True:
        print("\n================ MENU ================")
        if usuario_instancia.isAdmin:
            print("1. Buscar equipo")
            print("2. Revisar solicitudes pendientes")
            print("3. Registrar devolucion de equipo")
            print("4. Salir")
            
            x = input("▶ Seleccione una opcion: ")
            
            if x == "1":
                q = input("▶ Ingrese busqueda: ")
                print("1. Por nombre | 2. Por categoria")
                t = input("▶ Tipo: ")
                tipo_c = 0 if t == "1" else 1
                res = usuario_instancia.consultar(q, tipo_c)
                
                if res == -1:
                    print("\nNo se encontraron resultados.")
                else:
                    print("\n--- DETALLE DEL EQUIPO ---")
                    print("ID:", res.get("id", "N/A"))
                    print("Nombre:", res.get("nombre", "N/A"))
                    print("Categoria:", res.get("categoria", "N/A"))
                    print("Descripcion:", res.get("descripcion", "N/A"))
                    print("Poseedor (ID):", res.get("poseedor", "Ninguno"))
                    print("--------------------------")
                    
            elif x == "2":
                sols = usuario_instancia.revisar_solicitudes()
                if not sols:
                    print("\nNo hay solicitudes pendientes.")
                else:
                    print("\n--- SOLICITUDES ACTIVAS ---")
                    for eq_id, reqs in sols.items():
                        eq_info = getEquipo(eq_id)
                        nom = eq_info["nombre"] if eq_info != -1 else "Desconocido"
                        print("Equipo:", nom, "(ID:", str(eq_id) + ")")
                        print("IDs Usuarios Solicitantes:", ", ".join(map(str, reqs)))
                        print("-" * 30)
                    
                    print("\n¿Que desea hacer?")
                    print("1. Aceptar una solicitud")
                    print("2. Volver al menu principal")
                    
                    sub_opt = input("▶ ")
                    
                    if sub_opt == "1":
                        try:
                            eq_id = int(input("▶ ID del equipo: "))
                            usr_id = int(input("▶ ID del usuario a aprobar: "))
                            res_acc = usuario_instancia.aceptar_solicitud(eq_id, usr_id)
                            if res_acc == 0:
                                print("Solicitud aceptada con exito.")
                            else:
                                print("No se pudo procesar la solicitud.")
                        except ValueError:
                            print("Error: Ingrese solo numeros enteros.")
                        
            elif x == "3":
                try:
                    eq_id = int(input("▶ ID del equipo a devolver: "))
                    res = usuario_instancia.devolver_equipo(eq_id)
                    if res == 0:
                        print("Equipo recibido correctamente.")
                    else:
                        print("El equipo no estaba prestado o no existe.")
                except ValueError:
                    print("Error: Ingrese un numero valido.")
                    
            elif x == "4":
                print("Saliendo...")
                break
            else:
                print("Opcion no valida.")
                
        else:
            print("1. Buscar equipo")
            print("2. Salir")
            
            x = input("▶ Seleccione una opcion: ")
            
            if x == "1":
                q = input("▶ Ingrese busqueda: ")
                print("1. Por nombre | 2. Por categoria")
                t = input("▶ Tipo: ")
                tipo_c = 0 if t == "1" else 1
                res = usuario_instancia.consultar(q, tipo_c)
                
                if res == -1:
                    print("\nNo se encontraron resultados.")
                else:
                    print("\n--- DETALLE DEL EQUIPO ---")
                    print("ID:", res.get("id", "N/A"))
                    print("Nombre:", res.get("nombre", "N/A"))
                    print("Categoria:", res.get("categoria", "N/A"))
                    print("Descripcion:", res.get("descripcion", "N/A"))
                    print("--------------------------")
                    
                    print("\n¿Que desea hacer?")
                    print("1. Solicitar este equipo")
                    print("2. Volver al menu principal")
                    
                    sub_opt = input("▶ ")
                    
                    if sub_opt == "1":
                        try:
                            eq_id = int(input("▶ Ingrese el ID del equipo para confirmar: "))
                            res_sol = usuario_instancia.solicitar(eq_id)
                            if res_sol == 0:
                                print("Solicitud realizada con exito.")
                            elif res_sol == -1:
                                print("El equipo ya se encuentra ocupado.")
                            elif res_sol == -2:
                                print("Ya habias solicitado este equipo previamente.")
                            else:
                                print("Error al procesar la solicitud.")
                        except ValueError:
                            print("Error: Debe ingresar un ID numerico valido.")
                            
            elif x == "2":
                print("Saliendo...")
                break
            else:
                print("Opcion invalida.")

if __name__ == "__main__":
    main()
