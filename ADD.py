import os

def mostrar_arbol(ruta=".", ignorar=None):
    if ignorar is None:
        ignorar = {"env", "__pycache__", ".git"}  # carpetas a ignorar

    def recorrer(carpeta, prefijo=""):
        # Filtrar subcarpetas y archivos
        elementos = [e for e in os.listdir(carpeta) if e not in ignorar]
        elementos.sort()
        total = len(elementos)

        for i, nombre in enumerate(elementos):
            ruta_completa = os.path.join(carpeta, nombre)
            conector = "├── " if i < total - 1 else "└── "

            print(prefijo + conector + nombre)

            if os.path.isdir(ruta_completa):
                nuevo_prefijo = prefijo + ("│   " if i < total - 1 else "    ")
                recorrer(ruta_completa, nuevo_prefijo)

    print(ruta)
    recorrer(ruta)

# Ejecuta en la carpeta actual
mostrar_arbol(".")