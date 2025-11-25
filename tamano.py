"""
Programa para calcular el tamaño de un archivo
"""

import os

def obtener_tamano(ruta):
    if os.path.isfile(ruta):
        # Si es archivo, devuelve su tamaño en bytes
        return os.path.getsize(ruta)
    elif os.path.isdir(ruta):
        # Si es carpeta, suma el tamaño de todos los archivos dentro
        total = 0
        for carpeta, _, archivos in os.walk(ruta):
            for archivo in archivos:
                ruta_completa = os.path.join(carpeta, archivo)
                total += os.path.getsize(ruta_completa)
        return total
    else:
        raise FileNotFoundError(f"La ruta '{ruta}' no existe.")

def mostrar_tamano(ruta):
    try:
        tamano = obtener_tamano(ruta)
        # Convertir a KB, MB, GB según corresponda
        if tamano < 1024:
            print(f"{ruta}: {tamano} bytes")
        elif tamano < 1024**2:
            print(f"{ruta}: {tamano/1024:.2f} KB")
        elif tamano < 1024**3:
            print(f"{ruta}: {tamano/1024**2:.2f} MB")
        else:
            print(f"{ruta}: {tamano/1024**3:.2f} GB")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Ejemplo: cambia la ruta por la que quieras analizar
    ruta = "archivos_prueba/vieja_en_fondo_rojo.jpg"
    mostrar_tamano(ruta)