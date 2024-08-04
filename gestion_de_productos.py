'''
Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:

Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
Implementar operaciones CRUD para gestionar productos del inventario.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.

'''
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
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else: 
            return datos
        
    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado al guardar los datos: {error}')
    
    def crear_producto(self, producto):
        try:
            datos = self.leer_datos()
            nombre = producto.nombre
            if nombre not in datos:
                datos[nombre] = producto.to_dict()
                self.guardar_datos(datos)
                print(f'Nuevo producto {producto.nombre} {producto.marca} guardado.')
            else:
                print(f'Ya existe un producto con nombre {nombre}.')
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}') 

    def leer_producto(self, nombre):
        try: 
            datos = self.leer_datos()
            nombre = nombre.capitalize()
            if nombre in datos:
                producto_data = datos[nombre]
                if 'fecha_caducidad' in producto_data:
                    producto = ProductoAlimenticio(**producto_data) 
                else: 
                    producto = ProductoElectronico(**producto_data)
                print(f'Producto nombre {nombre} encontrado.')
            else: 
                print(f'No se encontró producto con nombre {nombre}.')
        except Exception as e:
            print(f'Error al leer el producto: {e}')                    

    def actualizar_precio(self, nombre, nuevo_precio):
        try:
            datos = self.leer_datos()
            if nombre in datos:
                nuevo_precio = Producto.validar_precio(self, nuevo_precio)
                datos[nombre]["precio"] = nuevo_precio
                self.guardar_datos(datos)
                print(f'Precio actualizado para el producto con nombre: {nombre}.')
            else: 
                print(f'No se encontró producto con nombre: {nombre}.')
        except Exception as e:
            print(f'Error al actualizar el precio del producto: {e}')   

    def eliminar_producto(self, nombre):
        try:
            datos = self.leer_datos()
            if nombre in datos:
                del datos[nombre]
                self.guardar_datos(datos)
                print(f'Producto con el nombre: {nombre} eliminado correctamente.')
            else: 
                print(f'No se encontró producto con el nombre: {nombre}.')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
