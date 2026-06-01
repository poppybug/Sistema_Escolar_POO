import os
import json


from Clases.Administrador import Administrador
from Clases.Profesor import Profesor
from Clases.Alumno import Alumno
from Clases.Materia import Materia
from Clases.Calificacion import Calificacion

# Usuarios por defecto
admin_sistemas = Administrador(1, "admin", "1234", "admin@escolar.com")
profe_test = Profesor(201, "profe1", "123", "profe@itp.esu.mx", "Ing. Manuel Esparza", "Sistemas")

lista_alumnos = []
lista_usuarios_sistema = [admin_sistemas, profe_test]
acceso = False

# =====================================================================
# CARGAR DATOS
# =====================================================================
def cargar_datos():
    try:
        if not os.path.exists("datos_escolares.json"):
            return
            
        with open("datos_escolares.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            lista_alumnos.clear()
            
            global lista_usuarios_sistema
            lista_usuarios_sistema = [admin_sistemas, profe_test]
            
            for a in datos["alumnos"]:
                nuevo_alumno = Alumno(
                    int(a['id_usuario']), a['username'], a['password'],
                    a['correo'], a['nombre_completo'], a['carrera'], a['semestre']
                )
                
                notas_guardadas = a.get('calificaciones', [])
                for n in notas_guardadas:
                    obj_materia = Materia(clave="GEN", nombre=n['materia_nombre'])
                    obj_nota = Calificacion(n['valor_numerico'], obj_materia)
                    nuevo_alumno.calificaciones.append(obj_nota)
                
                lista_alumnos.append(nuevo_alumno)
                lista_usuarios_sistema.append(nuevo_alumno)
        print("[SISTEMA] Datos cargados correctamente bajo arquitectura POO.")
    except Exception as e:
        print(f"Error al cargar: {e}")

def guardar_datos():
    lista_diccionarios_alumnos = []
    for a in lista_alumnos:
        dict_alumno = {
            "id_usuario": a.id_usuario,
            "username": a.username,
            "password": a.password,
            "rol": a.rol,
            "correo": a.correo,
            "nombre_completo": a.nombre_completo,
            "carrera": a.carrera,
            "semestre": a.semestre,
            "calificaciones": [
                {"valor_numerico": c.valor_numerico, "materia_nombre": c.materia.nombre} 
                for c in a.calificaciones
            ]
        }
        lista_diccionarios_alumnos.append(dict_alumno)
    
    datos = {
        "alumnos": lista_diccionarios_alumnos,
        "usuarios": [
            {
                "id_usuario": u.id_usuario, "username": u.username, 
                "password": u.password, "rol": u.rol, "correo": u.correo, 
                "nombre_completo": u.nombre_completo
            } for u in lista_usuarios_sistema if u.rol != "Alumno"
        ]
    }
    
    with open("datos_escolares.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

# =====================================================================
# MENÚS DEL PORTAL Escolar
# =====================================================================
def menu_alumno(alumno_actual):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- PORTAL DEL ALUMNO: {alumno_actual.nombre_completo} ---")
        print("1. Ver mis calificaciones")
        print("2. Ver mi promedio")
        print("3. Cerrar sesión")
        
        opc_alumno = input("\nSeleccione una opción: ")
        
        if opc_alumno == "1":
            print(f"\nDetalle de materias para {alumno_actual.nombre_completo}")
            for nota in alumno_actual.calificaciones:
                print(f"- {nota.materia.nombre}: {nota.valor_numerico}")
            input("\nPresione Enter para continuar...")
        
        elif opc_alumno == "2":
            promedio = alumno_actual.calcular_promedio()
            print(f"\nTu promedio general es: {round(promedio, 2)}")
            input("\nPresione Enter para continuar...")
        
        elif opc_alumno == "3":
            break

def menu_profesor(profe_actual, alumnos):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- PORTAL DOCENTE: {profe_actual.nombre_completo} ---")
        print("1. Ver lista de alumnos")
        print("2. Capturar calificación")
        print("3. Ver promedios del grupo")
        print("4. Cerrar sesión")
        
        opc_profe = input("\nSeleccione una opción: ")
        
        if opc_profe == "1":
            print("\n--- LISTA DE ALUMNOS REGISTRADOS ---")
            for est in alumnos:
                print(f"- {est.nombre_completo} ({est.carrera})")
            input("\nPresione Enter para continuar...")
            
        elif opc_profe == "2":
            print("\n--- ASIGNAR CALIFICACIÓN ---")
            buscar = input("Nombre del alumno a calificar: ")    
            encontrado = False      
            
            for estudiante in alumnos:
                if estudiante.nombre_completo == buscar:
                    materia_nom = input("Nombre de la materia: ")
                    
                    materia_existe = any(c.materia.nombre.lower() == materia_nom.lower() for c in estudiante.calificaciones)
                    if materia_existe:
                        print(f"\n[ERROR] El alumno ya tiene nota en '{materia_nom}'.")
                        break
                        
                    while True:
                        try:
                            nota = float(input("Calificación (0-100): "))
                            if 0 <= nota <= 100: break
                            else: print("¡ERROR! Debe estar entre 0 y 100.")
                        except ValueError:
                            print("Error: Ingrese un número válido.")
                            
                    nueva_materia_obj = Materia(clave="SIS", nombre=materia_nom)
                    nueva_cal = Calificacion(nota, nueva_materia_obj)
                    
                    estudiante.calificaciones.append(nueva_cal)
                    guardar_datos()
                    print(f"¡Éxito! Nota guardada para {estudiante.nombre_completo}")        
                    encontrado = True
                    break   
                
            if not encontrado: print("Alumno no encontrado.")
            input("\nPresione Enter para continuar... ")
            
        elif opc_profe == "3":
            print("\n--- RENDIMIENTO DEL GRUPO ---")
            for est in alumnos:
                print(f"- {est.nombre_completo}: {round(est.calcular_promedio(), 2)}")
            input("\nPresione Enter para continuar... ")
            
        elif opc_profe == "4":
            break

def menu_administrador():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Registrar Alumno")
        print("2. Ver Promedios")
        print("3. Salir")
    
        try:
            opc = int(input("Seleccione una opción: "))
        except ValueError:
            continue
    
        if opc == 1:
            print("\n--- SECCIÓN: REGISTRAR ALUMNO ---")
            id = input("Escribe la matrícula: ")
            
            existe = any(str(u.id_usuario) == id for u in lista_usuarios_sistema)
            if existe:
                print("¡ERROR! Esa matrícula ya existe.")
            else:
                nom = input("Escribe el nombre completo: ")
                car = input("Escribe la carrera: ")
                sem = int(input("Escribe el semestre: "))
                pass_new = input("Contraseña: ")
                correo_auto = f"{nom.lower().replace(' ', '')}{id}@itslp.edu.mx"
                
                alumno1 = Alumno(int(id), nom.lower().replace(' ', ''), pass_new, correo_auto, nom, car, sem)
                
                lista_alumnos.append(alumno1)       
                lista_usuarios_sistema.append(alumno1)      
                guardar_datos()
                print(f"¡Alumno {alumno1.nombre_completo} registrado!")
            input("\nPresione Enter para volver...")
        
        elif opc == 2:
            print("\n--- SECCIÓN: VER PROMEDIOS ---")
            for est in lista_alumnos:
                print(f"Nombre: {est.nombre_completo} | Promedio: {round(est.calcular_promedio(), 2)}")
            input("\nPresione Enter para volver...")
    
        elif opc == 3:
            break

# =====================================================================
# FLUJO PRINCIPAL (LOGIN)
# =====================================================================
cargar_datos()

while not acceso:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- LOGIN DE SISTEMA ---")
    user1 = input("ID o Correo institucional: ")
    pass1 = input("Contraseña: ")
    
    usuario_logueado = admin_sistemas.verificar_credenciales(user1, pass1, lista_usuarios_sistema)
        
    if usuario_logueado:
        print(f"¡Bienvenido {usuario_logueado.username}!")
        if usuario_logueado.rol == "Admin":
            menu_administrador()
        elif usuario_logueado.rol == "Alumno":
            menu_alumno(usuario_logueado)
        elif usuario_logueado.rol == "Docente":
            menu_profesor(usuario_logueado, lista_alumnos)
    else:
        print("Datos incorrectos.\n")
        input("Presione Enter para reintentar...")