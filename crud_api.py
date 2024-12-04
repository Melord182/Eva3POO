import requests
import json

# definimos la clase
class APIClient:
    def __init__(self, url):
        # Constructor que inicializa la URL base de la API
        self.url = url

    # Método GET
    def metodo_get(self, endpoint, valor):
        try:
            # Construcción de la URL completa
            url = f"{self.url}/{endpoint}"
            # Realizamos la solicitud GET
            response = requests.get(url)
            print(f"codigo de respuesta get :{response.status_code}")
            # Verificamos si la respuesta fue exitosa 
            if response.status_code == 200:
                # Convertimos la respuesta a formato JSON
                products = response.json()
                # Iteramos y mostramos solo la cantidad determinada
                for product in products[:valor]:
                    
                    print(f"- {product['title']} (${product['price']})")
                    
            else:
                # Si falla, mostramos el código de error
                print(f"Error al obtener productos: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")

        except ValueError:
            print("error la respuesta no es un json valido")
    def metodo_gett(self, endpoint, id):
        try:
        # Construcción de la URL completa
            url = f"{self.url}/{endpoint}/{id}"
            # Realizamos la solicitud GET
            response = requests.get(url)
            print(f"Código de respuesta GET: {response.status_code}")
            
            # Verificamos si la respuesta fue exitosa
            if response.status_code == 200:
                # Convertimos la respuesta a formato JSON
                response= response.json()
                print("-------------------------------------------")
                print(f"Nombre: {response['title']}")
                print(f"Precio: ${response['price']}")
                print(f"Descripción: {response['description']}")
                print(f"Categoría: {response['category']}")
                print("-------------------------------------------")
            else:
                # Si falla, mostramos el código de error
                print(f"Error al obtener producto: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")

    def metodo_g3t(self, endpoint, endpoint2, categoria, cantidad):
        try:
            url = f"{self.url}/{endpoint}/{endpoint2}/{categoria}"
            # Hacer la solicitud GET a la API
            response = requests.get(url)
            response.raise_for_status()  # Lanza un error si el código no es 200
            # Convertir la respuesta a JSON
            response = response.json()
            # Validar que existan productos
            if response:        
                # Mostrar solo la cantidad indicada productos con los parámetros solicitados
                for i,producto in enumerate(response[:cantidad], start=1):
                    print("--------------------------------------------------------------------")
                    print(f"Nombre: {producto.get('title', )}")
                    print(f"Precio: ${producto.get('price', )}")
                    print(f"Descripción: {producto.get('description', )}")
                    print(f"Categoría: {producto.get('category', )}")
                    print("--------------------------------------------------------------------")
            else:
                print(f"No hay productos disponibles en la categoría '{categoria}'.")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
        except ValueError:
            print("Error al procesar los datos de la API.")

    # Método POST 
    def metodopost(self, endpoint, data):
        try:
            url = f"{self.url}/{endpoint}"
            # Realizamos la solicitud POST
            response = requests.post(url, json=data)
            print(f"Código de respuesta POST: {response.status_code}")
            
            # Verificamos si el recurso fue creado
            if response.status_code == 201:
                print("Datos enviados con POST:")
                # Mostramos la respuesta formateada en JSON
                print(json.dumps(response.json(), indent=4))
                return response.json()
            else:
                print("Error al enviar datos:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")

    # Método PUT para actualizar
    def metodoput(self, endpoint, id, data):
        try:
            #contruccion url completa
            url =f"{self.url}/{endpoint}/{id}"
            # Realizamos la solicitud Put
            response = requests.put(url, json=data)
            print(f"Código de respuesta PUT: {response.status_code}")
            # Verificamos si el recurso fue creado
            if response.status_code == 200:
                print("Datos enviados con PUT:")
                # Mostramos la respuesta formateada en JSON
                print(json.dumps(response.json(), indent=4))
                return response.json()
            else:
                print("Error al enviar datos:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")


    # Método PATCH para actualizar parcialmente
    def metodopatch(self, endpoint, id, data):
        try:
            url = f"{self.url}/{endpoint}/{id}"
            # Realizamos la solicitud PATCH
            response = requests.patch(url, json=data)
            print(f"Código de respuesta PATCH: {response.status_code}")
            
            # Verificamos si la actualización parcial fue exitosa 
            if response.status_code == 200:
                print("Datos enviados con PATCH:")

                print(json.dumps(response.json(), indent=4))
                return response.json()
            else:
                print("Error al enviar datos:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")

    # Método DELETE para eliminar 
    def metododelete(self, endpoint, id):
        try:
            url = f"{self.url}/{endpoint}/{id}"
            # Realizamos la solicitud DELETE
            response = requests.delete(url)
            print(f"Código de respuesta DELETE: {response.status_code}")
            
            # Verificamos si la eliminación fue exitosa (código 200 o 204)
            if response.status_code in [200, 204]:
                print("Datos eliminados satisfactoriamente")
                return True
            else:
                print("Error al eliminar datos:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            
# Función para solicitar un ID
def solicitud_id():
    # Solicitamos el ID al usuario
    try:
        id = int(input("Ingrese el ID del producto: "))
        # Validamos que el ID no sea mayor a 20
        while id > 20:
            print("Por favor, ingrese un ID menor o igual a 20")
            id = int(input("Ingrese el ID del producto: "))
        return id
    except ValueError:
        print("ID no válido. Por favor ingrese un número entero.")
        return None

# Función para recopilar datos para la solicitud PUT
def solicitud_put():
    try:
        print("--------------------------------------------------------------------")
        print("Actualizar un producto")
        # Solicitamos los datos al usuario
        producto = input("Ingrese el nuevo título del producto: ")
        precio = float(input("Ingrese el nuevo precio del producto: "))
        descripcion = input("Ingrese la nueva descripción del producto: ")
        imagen = input("Ingrese la nueva URL de la imagen del producto: ")
        categoria = input("Ingrese la nueva categoría del producto: ")
        print("--------------------------------------------------------------------")
        while precio < 0:
            print("Error: El precio no puede ser negativo.")
            precio=float(input("ingrese el precio nuevamente"))
            
        # Creamos un diccionario con los datos recopilados
        datos = {
            "title": producto,
            "price": precio,  # Aseguramos que el precio no sea negativo
            "description": descripcion,
            "image": imagen,
            "category": categoria}
        

        return datos, producto, precio, descripcion, imagen, categoria
    except ValueError:
        print("Error: El precio ingresado no es válido. Debe ser un número.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Solicitud POST
def solicitar_datos_post():
    try:
        print("--------------------------------------------------------------------")
        producto = input("Ingrese el título del producto: ")
        precio = float(input("Ingrese el precio del producto: "))
        descripcion = input("Ingrese la descripción del producto: ")
        imagen = input("Ingrese la URL de la imagen del producto: ")
        categoria = input("Ingrese la categoría del producto: ")
        print("--------------------------------------------------------------------")
        while precio < 0:
            print("Error: El precio no puede ser negativo.")
            precio=float(input("ingrese el precio nuevamente"))
            
        # Creamos un diccionario con los datos del nuevo producto
        nuevo = {
            "title": producto,
            "price": precio,
            "description": descripcion,
            "image": imagen,
            "category": categoria}
        
        return nuevo, producto, precio, descripcion, imagen, categoria

    except ValueError:
        print("Error: El precio ingresado no es válido. Debe ser un número.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Solicitud PATCH
def solicitud_patch():
    print("Actualización parcial de datos:")
    try:
        print("--------------------------------------------------------------------")
        producto = input("Ingrese el nuevo título del producto: ")
        precio = float(input("Ingrese el nuevo precio del producto: "))
        descripcion = input("Ingrese la nueva descripción del producto: ")
        imagen = input("Ingrese la nueva URL de la imagen del producto: ")
        categoria = input("Ingrese la nueva categoría del producto: ")
        print("--------------------------------------------------------------------")

        if precio < 0:
            print("Error: El precio no puede ser negativo.")
            return None

        # Diccionario con datos para la actualización parcial
        datos_actualizados = {
            "title": producto,
            "price": precio,
            "description": descripcion,
            "image": imagen,
            "category": categoria}

        return datos_actualizados
    except ValueError:
        print("Error: El precio ingresado no es válido. Debe ser un número.")
    except Exception as e:
        print(f"Error inesperado: {e}")
