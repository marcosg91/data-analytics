'''
Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:

Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
Implementar operaciones CRUD para gestionar productos del inventario.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.

Desafío 2: Persistencia de datos en MySQL
Objetivo: Mediante la creación de repositorios en GitHub que implemente la solución propuesta en el laboratorio anterior con persistencia en una base de datos SQL.

Requisitos:

En este laboratorio, deberás implementar la solución utilizando Python en el paradigma de programación orientada a objetos. 
La persistencia de los datos deberá realizarse en una base de datos SQL. 
Una vez completada la solución, deberás subir el código a un repositorio público en GitHub y proporcionar el enlace correspondiente para su evaluación.
'''
import mysql.connector
from mysql.connector import Error
from decouple import config
from datetime import datetime
import json

# Definimos la clase y sus atributos
class Producto:
    def __init__(self, nombre, marca, precio, cantidad):
        self.__nombre = nombre
        self.__marca = marca
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)

    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def marca(self):
        return self.__marca.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def cantidad(self):
        return self.__cantidad
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)
    
    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        self.__cantidad = self.validar_cantidad(nueva_cantidad)

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError('El precio debe ser un número positivo.')
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser un número válido.")
    
    def validar_cantidad(self, cantidad):
        try:
            cantidad_num = int(cantidad)
            if cantidad_num <= 0:
                raise ValueError('La cantidad debe ser un número entero positivo.')
            return cantidad_num
        except ValueError:
            raise ValueError("La cantidad debe ser un número entero válido.")

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "marca": self.marca,
            "precio": self.precio,
            "cantidad": self.cantidad,
        }
    
    def __str__(self):
        return f"{self.nombre} {self.marca}"

class ProductoAlimenticio(Producto):
    def __init__(self, nombre, marca, precio, cantidad, fecha_caducidad):
        super().__init__(nombre, marca, precio, cantidad)
        self.__fecha_caducidad = fecha_caducidad

    @property
    def fecha_caducidad(self):
        return self.__fecha_caducidad
    
    @fecha_caducidad.setter
    def fecha_caducidad(self, nueva_fecha):
        self.__fecha_caducidad = nueva_fecha
    
    def to_dict(self):
        data = super().to_dict()
        data['fecha_caducidad'] = self.fecha_caducidad
        return data
    
    def __str__(self):
        return f'{super().__str__()} - Fecha de caducidad: {self.fecha_caducidad}'
    
class ProductoElectronico(Producto):
    def __init__(self, nombre, marca, precio, cantidad, garantia):
        super().__init__(nombre, marca, precio, cantidad)
        self.__garantia = garantia

    @property
    def garantia(self):
        return self.__garantia
    
    @garantia.setter
    def garantia(self, nueva_garantia):
        self.__garantia = nueva_garantia
    
    def to_dict(self):
        data = super().to_dict()
        data['garantia'] = self.garantia
        return data
    
    def __str__(self):
        return f'{super().__str__()} - Garantía: {self.garantia}'

class GestionProductos: 
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')

    def connect(self):
        '''Método para establecer una conexión a la base de datos'''
        try: 
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,                           
                user=self.user,
                password=self.password,
                port=self.port
            )

            if connection.is_connected():
                return connection
        
        except Error as e:
            print(f'Error al conectar la base de datos: {e}')
            return None
          
    def crear_producto(self, producto):
        try:
            # Obtener la conexión a la base de datos
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:

                    # Verificar si el producto ya existe
                    cursor.execute(
                        'SELECT Nombre FROM Productos WHERE Nombre = %s',
                        (producto.nombre,)
                    )
                    if cursor.fetchone():
                        print(f'Error: ya existe un producto con el nombre {producto.nombre}')
                        return
                    
                    # Insertar producto dependiendo del tipo
                    if isinstance(producto, ProductoAlimenticio):
                        try:
                            # Convertir la fecha al formato correcto (YYYY-MM-DD)
                            fecha_caducidad = datetime.strptime(producto.fecha_caducidad, '%Y-%m-%d').date()
                        except ValueError as ve:
                            print(f'Error en el formato de la fecha de caducidad: {ve}')
                            return

                        # Insertar en Productos
                        query = '''
                        INSERT INTO Productos (Nombre, Marca, Precio, Cantidad)
                        VALUES (%s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.nombre, producto.marca, producto.precio, producto.cantidad))

                        # Insertar en ProductoAlimenticio
                        query = '''
                        INSERT INTO ProductoAlimenticio (Fecha_caducidad, Nombre)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (fecha_caducidad, producto.nombre))

                    elif isinstance(producto, ProductoElectronico):
                        # Insertar en Productos
                        query = '''
                        INSERT INTO Productos (Nombre, Marca, Precio, Cantidad)
                        VALUES (%s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.nombre, producto.marca, producto.precio, producto.cantidad))

                        # Insertar en ProductoElectronico
                        query = '''
                        INSERT INTO ProductoElectronico (Garantia, Nombre)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (producto.garantia, producto.nombre))

                    # Confirmar cambios en la base de datos
                    connection.commit()
                    print(f'Producto {producto.nombre} creado correctamente.')

        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')
        finally:
            if connection:
                connection.close()  # Cerrar la conexión

    def leer_producto(self, nombre):
        try:
            # Conectar a la base de datos
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    # Buscar producto en la tabla Productos
                    cursor.execute('SELECT * FROM Productos WHERE Nombre = %s', (nombre,))
                    producto_data = cursor.fetchone()

                    if producto_data:
                        # Convertir las claves a minúsculas
                        producto_data = {key.lower(): value for key, value in producto_data.items()}
                        
                        # Buscar si es un ProductoAlimenticio
                        cursor.execute('SELECT Fecha_caducidad FROM ProductoAlimenticio WHERE Nombre = %s', (nombre,))
                        fecha_caducidad = cursor.fetchone()

                        if fecha_caducidad:
                            # Convertir claves a minúsculas
                            fecha_caducidad = {key.lower(): value for key, value in fecha_caducidad.items()}
                            
                            # Es un ProductoAlimenticio
                            producto_data['fecha_caducidad'] = fecha_caducidad['fecha_caducidad']
                            producto = ProductoAlimenticio(**producto_data)

                        else:
                            # Buscar si es un ProductoElectronico
                            cursor.execute('SELECT Garantia FROM ProductoElectronico WHERE Nombre = %s', (nombre,))
                            garantia = cursor.fetchone()

                            if garantia:
                                # Convertir claves a minúsculas
                                garantia = {key.lower(): value for key, value in garantia.items()}
                                
                                # Es un ProductoElectronico
                                producto_data['garantia'] = garantia['garantia']
                                producto = ProductoElectronico(**producto_data)

                            else:
                                # Si no está en ninguna de las tablas específicas, es un Producto general
                                producto = Producto(**producto_data)
                    else:
                        producto = None

        except Error as e:
            print(f'Error al leer producto: {e}')
        else:
            return producto
        finally:
            if connection and connection.is_connected():
                connection.close()  # Cerrar la conexión
        
    def actualizar_precio(self, nombre, nuevo_precio):
        try:
            # Obtener la conexión a la base de datos
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:

                    # Verificar si el producto existe
                    cursor.execute('SELECT * FROM Productos WHERE Nombre = %s', (nombre,))
                    if not cursor.fetchone():
                        print(f'No se encontró producto con el nombre {nombre}.')
                        return
                    
                    # Si encuentra el producto, actualizar el precio
                    cursor.execute('UPDATE Productos SET Precio = %s WHERE Nombre = %s', (nuevo_precio, nombre))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Precio actualizado para el producto con nombre: {nombre}.')
                    else:
                        print(f'No se encontró el producto con nombre: {nombre}.')
        
        except Exception as e:
            print(f'Error al actualizar el precio del producto: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()  # Cerrar la conexión
  
    def eliminar_producto(self, nombre):
        try:
            # Obtener la conexión a la base de datos
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:

                    # Verificar si el producto existe
                    cursor.execute('SELECT * FROM Productos WHERE Nombre = %s', (nombre,))
                    if not cursor.fetchone():
                        print(f'No se encontró producto con el nombre {nombre}.')
                        return
                    
                    # Si encuentra el producto, eliminar de las tablas correspondientes
                    cursor.execute('DELETE FROM ProductoAlimenticio WHERE Nombre = %s', (nombre,))
                    cursor.execute('DELETE FROM ProductoElectronico WHERE Nombre = %s', (nombre,))
                    cursor.execute('DELETE FROM Productos WHERE Nombre = %s', (nombre,))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print(f'Se eliminó el producto con nombre: {nombre}')
                    else:
                        print(f'No se encontró el producto con nombre: {nombre}')
        
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()  # Cerrar la conexión

    def leer_todos_los_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    # Seleccionar todos los productos de la tabla Productos
                    cursor.execute('SELECT * FROM productos')
                    productos_data = cursor.fetchall()

                    productos = []  # Declaro una lista vacía

                    for producto_data in productos_data:
                        # Convertir las claves a minúsculas
                        producto_data = {key.lower(): value for key, value in producto_data.items()}
                        nombre = producto_data['nombre']  # Extraer el valor del campo 'nombre'

                        # Verificar si es un producto alimenticio
                        cursor.execute('SELECT fecha_caducidad FROM productoalimenticio WHERE nombre = %s', (nombre,))
                        fecha_caducidad = cursor.fetchone()

                        if fecha_caducidad:
                            # Si es un producto alimenticio, agregar la fecha de caducidad
                            producto_data['fecha_caducidad'] = fecha_caducidad['fecha_caducidad']
                            producto = ProductoAlimenticio(**producto_data)
                        else:
                            # Verificar si es un producto electrónico
                            cursor.execute('SELECT garantia FROM productoelectronico WHERE nombre = %s', (nombre,))
                            garantia = cursor.fetchone()

                            if garantia:
                                # Si es un producto electrónico, agregar la garantía
                                producto_data['garantia'] = garantia['garantia']
                                producto = ProductoElectronico(**producto_data)
                            else:
                                # Si no es ni alimenticio ni electrónico, se trata de un producto general
                                producto = Producto(**producto_data)

                        # Añadir el producto a la lista
                        productos.append(producto)

        except Exception as e:
            print(f'Error al mostrar los productos: {e}')
        else:
            return productos
        finally:
            if connection.is_connected():
                connection.close()  # Cerrar la conexión