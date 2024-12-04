from crud_api import *
from crud_db import db
import getpass
import string
import random

bd_productos = db()  # Se instancia la base de datos
bd_productos.creacion_tablas()  # Se crean las tablas necesarias en la base de datos

class Menu:
    def __init__(self, db_name='fakestore.db'):
        # Inicializa el gestor de la base de datos y la variable para el usuario autenticado
        self.db = db(db_name)
        self.usuario_logueado = "" # Variable para almacenar al usuario que ha iniciado sesión

    def ingreso(self):
        print("1 = Iniciar sesión")
        print("2 = Crear cuenta")
        respuesta = input("Seleccione una opción: ").strip()

        if respuesta == "1":
            self.iniciar_sesion()  # Si selecciona iniciar sesión, se ejecuta la función correspondiente
        elif respuesta == "2":
            print("crea tu cuenta")
            self.creacion_cuenta()  # Si selecciona crear cuenta, se ejecuta la función correspondiente
        else:
            print("Por favor, selecciona '1' o '2'.")
            self.ingreso()  # Si no es una opción válida, se vuelve a mostrar el menú

    def creacion_cuenta(self):
        nombre = input("Ingresa tu nombre: ").strip()
        nombre_usuario = input("Elige un nombre de usuario: ").strip()

        # Verifica si el nombre de usuario ya existe en la base de datos
        if self.db.verificar_usuario(nombre_usuario):
            print("Este nombre de usuario ya está en uso. Por favor, elige otro.")
            return  # Si el nombre de usuario ya existe, no continúa con la creación de cuenta

        print("¿Te gustaría que se genere una contraseña automáticamente? (si/no)")
        respuesta = input().strip().lower()

        if respuesta == "si":
            self.generar_contraseña_automatica(nombre, nombre_usuario)  # Si elige 'si', genera una contraseña automáticamente
        elif respuesta == "no":
            self.crear_contraseña_personalizada(nombre, nombre_usuario)  # Si elige 'no', le permite crear una contraseña personalizada
        else:
            print("Respuesta no válida. Por favor, responde con 'si' o 'no'.")

    def crear_contraseña_personalizada(self, nombre, nombre_usuario):
        contrasena = input("Crea tu contraseña (mínimo 8 caracteres): ").strip()
        while len(contrasena) < 8:  # Verifica que la contraseña tenga al menos 8 caracteres
            print("La contraseña es demasiado corta. Debe tener al menos 8 caracteres.")
            contrasena = input("Crea tu contraseña (mínimo 8 caracteres): ").strip()

        confirmacion = input("Confirma tu contraseña: ").strip()
        while confirmacion != contrasena:  # Verifica que las contraseñas coincidan
            print("Las contraseñas no coinciden. Intenta nuevamente.")
            confirmacion = input("Confirma tu contraseña: ").strip()

        # Inserta el usuario en la base de datos
        if self.db.insertar_usuario(nombre, nombre_usuario, contrasena):
            print("Cuenta creada con éxito.")
        else:
            print("Hubo un problema al crear tu cuenta. Intenta nuevamente.")

    def generar_contraseña_automatica(self, nombre, nombre_usuario):

        # Genera una contraseña aleatoria de 12 caracteres
        contrasena = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        print(f"Tu contraseña generada automáticamente es: {contrasena}")

        # Inserta el usuario en la base de datos con la contraseña generada automáticamente
        if self.db.insertar_usuario(nombre, nombre_usuario, contrasena):
            print("Cuenta creada con éxito.")
        else:
            print("Hubo un problema al crear tu cuenta. Intenta nuevamente.")

    def iniciar_sesion(self):
        nombre_usuario = input("Ingresa tu nombre de usuario: ").strip()
        contrasena = getpass.getpass("Ingresa tu contraseña: ").strip()

        # Verifica si el usuario existe y si la contraseña es correcta
        if self.db.verificar_usuario(nombre_usuario):
            if self.db.verificar_contraseña(nombre_usuario, contrasena):
                self.usuario_logueado = nombre_usuario  # Guarda al usuario autenticado
                print("Inicio de sesión exitoso.")
            else:
                print("Contraseña incorrecta. Intenta nuevamente.")
        else:
            print("Usuario no encontrado. Por favor, crea una cuenta.")

    def cerrar(self):
        if self.db.cerrar():
            print("Conexión cerrada correctamente.")
        else:
            print("Hubo un problema al cerrar la conexión.")

    def verificar_autenticacion(self):
        if not self.usuario_logueado:  # Si no hay un usuario autenticado
            print("Debes iniciar sesión para realizar esta acción.")
            self.ingreso()  # Vuelve al flujo de inicio de sesión
            return False  # No permite realizar la acción
        # Pide el usuario y la contraseña para confirmar la acción
        nombre_usuario = input("Ingresa tu nombre de usuario para continuar: ").strip()
        contrasena = getpass.getpass("Ingresa tu contraseña para continuar: ").strip()

        if not self.db.verificar_usuario(nombre_usuario):
            print("Usuario no encontrado. Intenta nuevamente.")
            return False  # No permite realizar la acción si el usuario no existe

        if not self.db.verificar_contraseña(nombre_usuario, contrasena):
            print("Contraseña incorrecta. Intenta nuevamente.")
            return False  # No permite realizar la acción si la contraseña es incorrecta

        self.usuario_logueado = nombre_usuario  # Actualiza al usuario logueado
        return True  # Permite realizar la acción si la autenticación es correcta


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n--- Menú Principal ---")
    print("1. Realizar una solicitud GET")
    print("2. Crear un nuevo producto (POST)")
    print("3. Actualizar un producto (PUT)")
    print("4. Actualización parcial de un producto (PATCH)")
    print("5. Ver lista de productos creados")
    print("6. Eliminar un producto (DELETE)")
    print("7. Cerrar sesión")
    print("8. Salir")


def main():
    menu = Menu()  # Instancia de la clase Menu para gestionar el flujo
    menu.ingreso()  # Inicia sesión o permite crear cuenta

    api = APIClient("https://fakestoreapi.com")  # Instancia para realizar peticiones a la API

    while True:
        if not menu.verificar_autenticacion():  # Verifica que el usuario esté autenticado
            continue  # Si no está autenticado, vuelve a pedir inicio de sesión

        mostrar_menu()  # Muestra el menú de opciones
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":  # Solicitud GET
            print("¿Qué quieres ver?")
            print("1: Productos")
            print("2: Categorías")
            print("3: Buscar un producto por su ID")
            seleccion = input("Selecciona una opción: ").strip()

            if seleccion == "1":
                cantidad = int(input("¿Cuántos productos quieres ver?: "))
                api.metodo_get("products", cantidad)  # Llama a la API para obtener productos

            elif seleccion == "2":
                # Muestra las categorías disponibles
                categorias = {
                    "1": "electronics",
                    "2": "jewelery",
                    "3": "men's clothing",
                    "4": "women's clothing"
                }
                print("Categorías disponibles:")
                print(" 1: electronics")
                print("2: jewelery")
                print("3: men's clothing")
                print("4: women's clothing")
                
                categoria = input("Selecciona una categoría (1-4): ").strip()
                if categoria in categorias:
                    cantidad = int(input("¿Cuántos productos quieres ver?: "))
                    api.metodo_g3t("products", "category", categorias[categoria], cantidad)  # Llama a la API para obtener productos por categoría
                else:
                    print("Categoría inválida.")

            elif seleccion == "3":
                id_producto = int(input("Ingresa el ID del producto: "))
                api.metodo_gett("products", id_producto)  # Llama a la API para obtener un producto por ID

        elif opcion == "2":  # Crear un nuevo producto (POST)
            if not menu.verificar_autenticacion():  # Verifica la autenticación antes de eliminar
                continue            
            datos_post, title, price, description, image, category = solicitar_datos_post()
            api.metodopost("products", datos_post)  # Crea el producto en la API
            bd_productos.guardar_datos_db(title, price, description, image, category)  # Guarda el producto en la base de datos
            print("Producto creado con éxito.")

        elif opcion == "3":  # Actualizar un producto (PUT)
            if not menu.verificar_autenticacion():  # Verifica la autenticación antes de eliminar
                continue
            id_producto = solicitud_id()
            datos_put, title, price, description, image, category = solicitud_put()
            api.metodoput("products", id_producto, datos_put)  # Actualiza el producto en la API
            bd_productos.modificar_datos_db(id_producto, title, price, description, image, category)  # Actualiza el producto en la base de datos
            print("Producto actualizado con éxito.")

        elif opcion == "4":  # Actualización parcial de un producto (PATCH)
            if not menu.verificar_autenticacion():  # Verifica la autenticación antes de eliminar
                continue
            id_producto = solicitud_id()
            datos_patch = solicitud_patch()
            api.metodopatch("products", id_producto, datos_patch)  # Realiza una actualización parcial en la API
            print("Producto actualizado parcialmente.")

        elif opcion == "5":  # Ver lista de productos creados
            productos = bd_productos.obtener_datos_db()  # Obtiene la lista de productos creados
            for producto in productos:
                print(f"""
                    ID: {producto[0]}
                    Nombre: {producto[1]}
                    Precio: {producto[2]}
                    Descripción: {producto[3]}
                    Imagen: {producto[4]}
                    Categoría: {producto[5]}
                """)

        elif opcion == "6":  # Eliminar un producto (DELETE)
            if not menu.verificar_autenticacion():  # Verifica la autenticación antes de eliminar
                continue
            id_producto = solicitud_id()
            api.metododelete("products", id_producto)  # Elimina el producto de la API
            bd_productos.eliminar_datos_db(id_producto)  # Elimina el producto de la base de datos
            print("Producto eliminado con éxito.")

        elif opcion == "7":  # Cerrar sesión
            menu.usuario_logueado = None  # Cierra la sesión actual
            print("Has cerrado sesión.")

        elif opcion == "8":  # Salir del programa
            print("Saliendo del programa. ¡Hasta luego!")
            break  # Sale del programa

        else:  # Opción no válida
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    main()  # Ejecuta la función principal