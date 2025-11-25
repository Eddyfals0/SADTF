"""CLI - Interfaz de línea de comandos para el usuario"""
import os
import sys
from typing import Optional


class InterfazCLI:
    """CLI interactivo para SADTF"""
    
    def __init__(self, api_archivos, tabla_bloques, tabla_nodos, logger=None):
        """
        Args:
            api_archivos: Instancia de APIArchivos
            tabla_bloques: Instancia de TablaBloques
            tabla_nodos: Instancia de TablaNodos
            logger: Logger
        """
        self.api = api_archivos
        self.tabla_bloques = tabla_bloques
        self.tabla_nodos = tabla_nodos
        self.logger = logger
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("    SADTF - Sistema de Almacenamiento Distribuido")
        print("="*50)
        print("1. Subir archivo")
        print("2. Descargar archivo")
        print("3. Eliminar archivo")
        print("4. Ver información de archivo")
        print("5. Listar archivos")
        print("6. Ver tabla de bloques")
        print("7. Ver nodos activos")
        print("8. Salir")
        print("="*50)
    
    def subir_archivo(self):
        """Interfaz para subir un archivo"""
        ruta = input("Ingrese la ruta del archivo: ").strip()
        
        if not os.path.exists(ruta):
            print(f"Error: Archivo no encontrado: {ruta}")
            return
        
        try:
            with open(ruta, 'rb') as f:
                datos = f.read()
            
            nombre = os.path.basename(ruta)
            propietario = input("Ingrese nombre del propietario (default: anonimo): ").strip() or "anonimo"
            
            exito, resultado = self.api.subir_archivo(nombre, datos, propietario)
            
            if exito:
                print(f"\nArchivo subido exitosamente!")
                print(f"ID del archivo: {resultado}")
            else:
                print(f"\nError al subir archivo: {resultado}")
        except Exception as e:
            print(f"Error: {e}")
    
    def descargar_archivo(self):
        """Interfaz para descargar un archivo"""
        archivo_id = input("Ingrese el ID del archivo a descargar: ").strip()
        
        info = self.tabla_bloques.obtener_archivo(archivo_id)
        if not info:
            print(f"Error: Archivo {archivo_id} no encontrado")
            return
        
        ruta_salida = input(f"Ingrese ruta de salida (default: {info['nombre']}): ").strip()
        ruta_salida = ruta_salida or info['nombre']
        
        exito, datos = self.api.descargar_archivo(archivo_id)
        
        if exito:
            with open(ruta_salida, 'wb') as f:
                f.write(datos)
            print(f"\nArchivo descargado exitosamente en: {ruta_salida}")
            print(f"Tamaño: {len(datos)} bytes")
        else:
            print(f"\nError al descargar archivo")
    
    def eliminar_archivo(self):
        """Interfaz para eliminar un archivo"""
        archivo_id = input("Ingrese el ID del archivo a eliminar: ").strip()
        
        confirmacion = input(f"¿Está seguro que desea eliminar {archivo_id}? (s/n): ").strip().lower()
        if confirmacion != 's':
            print("Operación cancelada")
            return
        
        exito, msg = self.api.eliminar_archivo(archivo_id)
        
        if exito:
            print(f"\n{msg}")
        else:
            print(f"\nError: {msg}")
    
    def ver_info_archivo(self):
        """Muestra información detallada de un archivo"""
        archivo_id = input("Ingrese el ID del archivo: ").strip()
        
        info = self.api.obtener_info_archivo(archivo_id)
        
        if not info:
            print(f"Error: Archivo {archivo_id} no encontrado")
            return
        
        print(f"\n{'='*50}")
        print(f"ID: {info['id']}")
        print(f"Nombre: {info['nombre']}")
        print(f"Propietario: {info['propietario']}")
        print(f"Tamaño: {info['size']} bytes")
        print(f"Número de bloques: {len(info['bloques'])}")
        print(f"\nBloques:")
        for bloque in info['bloques']:
            print(f"  - Bloque {bloque['id']}: Replicas en {bloque['replicas']}")
        print(f"{'='*50}")
    
    def listar_archivos(self):
        """Lista todos los archivos"""
        archivos = self.tabla_bloques.obtener_todos_archivos()
        
        if not archivos:
            print("\nNo hay archivos en el sistema")
            return
        
        print(f"\n{'='*50}")
        print(f"{'ID':<20} {'Nombre':<20} {'Propietario':<10} {'Tamaño':<10}")
        print(f"{'='*50}")
        
        for archivo_id, info in archivos.items():
            print(f"{archivo_id:<20} {info['nombre']:<20} {info['propietario']:<10} {info['size']:<10}")
        
        print(f"{'='*50}")
        print(f"Total de archivos: {len(archivos)}")
    
    def ver_tabla_bloques(self):
        """Muestra el estado de la tabla de bloques"""
        estado = self.tabla_bloques.obtener_estado_tabla()
        
        print(f"\n{'='*50}")
        print("ESTADO DE LA TABLA DE BLOQUES")
        print(f"{'='*50}")
        print(f"Total de bloques: {estado['total_bloques']}")
        print(f"Bloques usados: {estado['bloques_usados']}")
        print(f"Bloques libres: {estado['bloques_libres']}")
        print(f"Porcentaje usado: {(estado['bloques_usados']/estado['total_bloques']*100):.2f}%")
        print(f"Archivos almacenados: {estado['archivos']}")
        print(f"{'='*50}")
    
    def ver_nodos_activos(self):
        """Muestra los nodos activos del cluster"""
        nodos = self.tabla_nodos.obtener_nodos_activos()
        
        if not nodos:
            print("\nNo hay nodos activos")
            return
        
        print(f"\n{'='*50}")
        print(f"{'ID':<15} {'Host':<15} {'Puerto':<10} {'Capacidad':<12} {'Libre':<10}")
        print(f"{'='*50}")
        
        for nodo_id, info in nodos.items():
            print(f"{nodo_id:<15} {info['host']:<15} {info['puerto']:<10} "
                  f"{info['capacidad_mb']:<12} {info['espacio_libre_mb']:<10}")
        
        print(f"{'='*50}")
        print(f"Total de nodos: {len(nodos)}")
    
    def ejecutar(self):
        """Ejecuta el loop principal de la CLI"""
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == '1':
                self.subir_archivo()
            elif opcion == '2':
                self.descargar_archivo()
            elif opcion == '3':
                self.eliminar_archivo()
            elif opcion == '4':
                self.ver_info_archivo()
            elif opcion == '5':
                self.listar_archivos()
            elif opcion == '6':
                self.ver_tabla_bloques()
            elif opcion == '7':
                self.ver_nodos_activos()
            elif opcion == '8':
                print("\nSaliendo...")
                break
            else:
                print("Opción no válida")
