import os
import platform
from datetime import datetime
from gestion_de_productos import (
    ProductoAlimenticio,
    ProductoElectronico,
    GestionProductos,
)

def limpiar_pantalla():
    '''Limpia la pantalla según el sistema operativo.'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')  # Para todos los demás sistemas operativos

def mostrar_menu():
    print("########## MENÚ SISTEMA DE GESTIÓN DE PRODUCTOS ##########")
    print('1 - Agregar nuevo producto alimenticio')
    print('2 - Agregar nuevo producto electrónico')
    print('3 - Buscar producto por nombre')
    print('4 - Actualizar precio')
    print('5 - Eliminar un producto por su nombre')
    print('6 - Mostrar todos los productos')
    print('7 - Salir')

def validar_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
        hoy = datetime.now()
        if fecha <= hoy:
            raise ValueError('La fecha de caducidad debe ser una fecha futura.')
        return fecha.strftime('%d/%m/%Y')
    except ValueError:
        raise ValueError('La fecha ingresada no tiene el formato correcto (DD/MM/AAAA) o no es una fecha futura.')

def agregar_producto(gestion, tipo_producto):
    try:
        nombre = input('INGRESE NOMBRE DEL PRODUCTO: ')
        marca = input('INGRESE MARCA DEL PRODUCTO: ')
        precio = float(input('INGRESE PRECIO DEL PRODUCTO: '))
        cantidad = int(input('INGRESE CANTIDAD EN STOCK DEL PRODUCTO: '))

        if tipo_producto == '1':
            fecha_caducidad = input('Ingrese fecha de caducidad del producto (DD/MM/AAAA): ')
            fecha_caducidad = validar_fecha(fecha_caducidad)
            producto = ProductoAlimenticio(nombre, marca, precio, cantidad, fecha_caducidad)
        elif tipo_producto == '2':
            garantia = int(input('Ingrese meses de garantía del producto: '))
            if garantia < 0:
                print("La garantía no puede ser negativa.")
                return
            producto = ProductoElectronico(nombre, marca, precio, cantidad, garantia)
        else:
            print('Opción inválida')
            return
        
        gestion.crear_producto(producto)
    
    except ValueError as e: 
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_producto_por_nombre(gestion):
    try:
        nombre = input('Ingrese el nombre del producto a buscar: ').strip()
        if nombre:
            producto = gestion.leer_producto(nombre)  # Guardar la variable de producto

            if producto:  # Verificar si se encontró un producto
                if isinstance(producto, ProductoAlimenticio):
                    print(f'Producto encontrado: {producto.nombre} - Fecha de caducidad: {producto.fecha_caducidad}')
                elif isinstance(producto, ProductoElectronico):
                    print(f'Producto encontrado: {producto.nombre} - Garantía: {producto.garantia} meses')
                else:
                    print(f'Producto encontrado: {producto.nombre} - Es un producto general.')
            else:
                print("No se encontró el producto.")
        else:
            print("No ingresaste un nombre válido. Inténtalo de nuevo.")
    except Exception as e:
        print(f'Error al intentar buscar el producto: {e}')
    input('Presione Enter para continuar...')

def actualizar_precio(gestion):
    nombre = input('Ingrese el nombre del producto para actualizar su precio: ')
    gestion.leer_producto(nombre)
    precio = float(input('Ingrese el nuevo precio del producto: '))
    gestion.actualizar_precio(nombre, precio)

def eliminar_producto_por_nombre(gestion):
    nombre = input('Ingrese el nombre del producto a eliminar: ')
    gestion.leer_producto(nombre)
    gestion.eliminar_producto(nombre)

def mostrar_todos_los_productos(gestion):
    print('########## LISTADO COMPLETO DE LOS PRODUCTOS ##########')
    try:
        productos = gestion.leer_todos_los_productos()
        for producto in productos:
            if isinstance(producto, ProductoAlimenticio):
                print(f'{producto.nombre} {producto.marca} {producto.fecha_caducidad}')
            elif isinstance(producto, ProductoElectronico):
                print(f'{producto.nombre} {producto.marca} {producto.garantia}')    

    except Exception as e:
        print(f'Error al mostrar los productos {e}')
    print('########## ########## ########## ########## ########## ##########')
    input('Presione Enter para continuar...')

if __name__ == "__main__":
    gestion = GestionProductos()

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')
        if opcion == '1':
            agregar_producto(gestion, '1')
        elif opcion == '2':
            agregar_producto(gestion, '2')
        elif opcion == '3':
            buscar_producto_por_nombre(gestion)
        elif opcion == '4':
            actualizar_precio(gestion)
        elif opcion == '5':
            eliminar_producto_por_nombre(gestion)
        elif opcion == '6':
            mostrar_todos_los_productos(gestion)
        elif opcion == '7':
            break
        else:
            print('Opción no válida. Intente de nuevo.')
        
        # Mostrar mensaje solo una vez al final de cada ciclo del menú
        input('Presione Enter para continuar...')

