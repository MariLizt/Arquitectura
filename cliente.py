import requests
from requests.auth import HTTPBasicAuth

# Contraseña para agregar y eliminar usuarios
#usuario = admin
#contrasena = admin1


# Dirección del servidor
BASE_URL = 'http://localhost:5000/'

# Función para obtener las credenciales
def obtener_credenciales():
    print("Para esta opción de debe loguear:")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")
    return usuario, password

# Obtener usuarios (no requiere autenticación)
def obtener_usuarios():
    response = requests.get(BASE_URL + 'usuarios')
    if response.status_code == 200:
        usuarios = response.json()
        print("\n -- Resultado Todos los Usuarios -- \n\nUsuarios encontrados:")
        for usuario in usuarios:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios")

# Buscar usuario por ID (no requiere autenticación)
def obtener_usuario_por_id():
    id_usuario = input("Ingrese el ID del usuario a buscar: ")
    response = requests.get(BASE_URL + f'usuarios/{id_usuario}')
    if response.status_code == 200:
        usuario = response.json()
        print(f"\n --Resultado Usuario encontrado por ID-- \n ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Usuario no encontrado")

# Agregar usuario (requiere autenticación)
def agregar_usuario(auth):
    nombre = input("Ingrese el nombre del nuevo usuario: ").strip()  # Eliminar espacios en blanco
    if not nombre:
        print("El nombre no puede estar vacío.")
        return
    response = requests.post(BASE_URL + 'usuarios', json={"nombre": nombre}, auth=auth)  # Se incluye la autenticación
    if response.status_code == 201:
        print("\n -- Resultado Usuario Agregado -- \n", response.json())
    elif response.status_code == 400:
        print("Error al agregar usuario:", response.json()["mensaje"])
    else:
        print("Error al agregar usuario")

# Eliminar usuario (requiere autenticación)
def eliminar_usuario(auth):
    id_usuario = input("Ingrese el ID del usuario a eliminar: ")
    response = requests.delete(BASE_URL + f'usuarios/{id_usuario}', auth=auth)  # Se incluye la autenticación
    if response.status_code == 200:
        print("\n --Resultado Usuario Eliminado: --\n Con exito\n")
    elif response.status_code == 404:
        print("\n --Resultado Usuario Eliminado: --\n No encontrado")
    else:
        print("\n --Resultado Usuario Eliminado: --\n Error al eliminar usuario")

# Función principal para mostrar el menú y ejecutar las opciones
def mostrar_menu():
    auth = None  # Variable para almacenar las credenciales
    while True:
        print("\n--- Menú ---")
        print("1. Ver usuarios")
        print("2. Agregar nuevo usuario (requiere autenticación)")
        print("3. Búsqueda de usuarios por ID")
        print("4. Eliminar usuario (requiere autenticación)")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            obtener_usuarios()
        elif opcion == '2':
            if not auth:  # Si aún no se han ingresado credenciales
                usuario, password = obtener_credenciales()
                auth = HTTPBasicAuth(usuario, password)
            agregar_usuario(auth)
        elif opcion == '3':
            obtener_usuario_por_id()
        elif opcion == '4':
            if not auth:  # Si aún no se han ingresado credenciales
                usuario, password = obtener_credenciales()
                auth = HTTPBasicAuth(usuario, password)
            eliminar_usuario(auth)
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

# Función principal
def main():
    mostrar_menu()

if __name__ == '__main__':
    main()
