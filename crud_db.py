import sqlite3  # Importa el módulo para interactuar con bases de datos SQLite
import bcrypt  # Importa el módulo para trabajar con contraseñas de forma segura
from crud_api import *  # Importa funcionalidades adicionales desde un módulo llamado api1

# Clase que representa la base de datos y contiene métodos para interactuar con ella
class db:    
    def __init__(self, db_name='fakestore.db'):
        # Inicializa la clase con un nombre de base de datos predeterminado
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)  # Conecta a la base de datos
        self.cursor = self.conn.cursor()  # Crea un cursor para ejecutar consultas SQL
        
    def creacion_tablas(self):
        # Método para crear las tablas 'usuarios' y 'productos' si no existen
        if self.cursor:
            try:
                # Crea la tabla 'usuarios' con columnas id, nombre, nombre_usuario y contraseña
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        nombre_usuario TEXT UNIQUE,
                        contraseña TEXT
                    )
                ''')
                # Crea la tabla 'productos' con columnas id, title, price, description, image y category
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        price INTEGER NOT NULL,
                        description TEXT NOT NULL,
                        image TEXT NOT NULL,
                        category INTEGER NOT NULL
                    )
                """)
                self.conn.commit()  # Confirma la ejecución de las consultas
                return True  # Retorna True si las tablas fueron creadas correctamente
            except sqlite3.Error as e:
                # Si ocurre un error al crear las tablas, se captura la excepción
                print(f"Error al crear la tabla: {e}")
                return "Conexion con DB exitosa!"
    
    def insertar_usuario(self, nombre, nombre_usuario, contraseña):
        # Método para insertar un nuevo usuario en la tabla 'usuarios'
        if self.cursor:
            try:
                # Verifica si el nombre de usuario ya existe en la base de datos
                if self.verificar_usuario(nombre_usuario):
                    print(f"Error: El usuario '{nombre_usuario}' ya existe.")
                    return False  # Retorna False si el usuario ya existe
                
                # Hashea la contraseña para almacenarla de forma segura
                hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

                # Inserta el nuevo usuario con el nombre, nombre de usuario y contraseña hasheada
                self.cursor.execute(''' 
                    INSERT INTO usuarios (nombre, nombre_usuario, contraseña)
                    VALUES (?, ?, ?)
                ''', (nombre, nombre_usuario, hashed_password.decode('utf-8')))  # Guardamos el hash como string
                self.conn.commit()  # Confirma la inserción
                print("Usuario insertado correctamente.")
                return True  # Retorna True si el usuario fue insertado correctamente
            except sqlite3.Error as e:
                # Si ocurre un error al insertar el usuario, se captura la excepción
                print(f"Error al insertar el usuario: {e}")
                return False

    def verificar_contraseña(self, nombre_usuario, contraseña):
        # Método para verificar la contraseña ingresada por el usuario
        if self.cursor:
            # Busca la contraseña almacenada en la base de datos para el usuario especificado
            self.cursor.execute(''' 
                SELECT contraseña FROM usuarios WHERE nombre_usuario = ? 
            ''', (nombre_usuario,))
            resultado = self.cursor.fetchone()

            if resultado:
                # Compara la contraseña ingresada con la almacenada (utilizando el hash)
                if bcrypt.checkpw(contraseña.encode('utf-8'), resultado[0].encode('utf-8')):
                    return True  # La contraseña es correcta
                else:
                    print(f"Contraseña incorrecta.")  # La contraseña no coincide
                    return False
            else:
                print(f"Usuario no encontrado.")  # Si el usuario no existe
                return False

    def verificar_usuario(self, nombre_usuario):
        # Método para verificar si un usuario existe en la base de datos
        if self.cursor:
            # Busca al usuario en la base de datos
            self.cursor.execute(''' 
                SELECT * FROM usuarios WHERE nombre_usuario = ? 
            ''', (nombre_usuario,))
            return self.cursor.fetchone() is not None  # Retorna True si el usuario existe
    
    def cerrar(self):
        # Método para cerrar la conexión con la base de datos
        if self.conn:
            try:
                self.cursor.close()  # Cierra el cursor
                self.conn.close()  # Cierra la conexión con la base de datos
                return True
            except sqlite3.Error as e:
                # Si ocurre un error al cerrar la conexión, se captura la excepción
                print(f"Error al cerrar la conexión: {e}")

    def obtener_datos_db(self):
        # Método para obtener todos los productos de la base de datos
        cursor = self.conn.execute("SELECT * FROM productos ORDER BY id")
        data = cursor.fetchall()  # Obtiene todos los registros de productos
        return data
    
    def guardar_datos_db(self, title, price, description, image, category):
        # Método para insertar un nuevo producto en la tabla 'productos'
        self.conn.execute("INSERT INTO productos (title, price, description, image, category) VALUES (?,?,?,?,?)",
                          (title, price, description, image, category))
        self.conn.commit()  # Confirma la inserción
        return "Producto ingresado con éxito a la base de datos."  # Retorna un mensaje de éxito

    def modificar_datos_db(self, id, title, price, description, image, category):
        # Método para modificar un producto existente en la base de datos
        self.conn.execute("UPDATE productos SET title=?, price=?, description=?, image=?, category=? WHERE id = ?",
                          (title, price, description, image, category, id))
        self.conn.commit()  # Confirma la modificación
        return f"Producto de id {id} modificado exitosamente"  # Retorna un mensaje de éxito

    def eliminar_datos_db(self, id):
        # Método para eliminar un producto de la base de datos
        self.conn.execute("DELETE FROM productos WHERE id = ?", (id,))
        self.conn.commit()  # Confirma la eliminación
        return f"Producto {id} eliminado correctamente"  # Retorna un mensaje de éxito
