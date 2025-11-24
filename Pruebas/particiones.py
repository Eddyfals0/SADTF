import os

BLOCK_SIZE = 1024 *1024


def partir_archivo(ruta_entrada, carpeta_salida):
    
    #Crear la carpeta por si no exixte
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # 'rb' = read binary
    with open(ruta_entrada, "rb") as f:
        indice = 0 
        
        while True:
            bloque = f.read(BLOCK_SIZE)
            
            if not bloque:
                break
            
            #Creamos el nombre del bloque
            nombre_bloque = f"block_{indice}.bin"
            
            ruta_bloque = os.path.join(carpeta_salida, nombre_bloque)
            
            #abrimos archivo del bloque en
            #write binary
            with open(ruta_bloque, "wb") as out:
                out.write(bloque)
            
            print(f"Pal Bloque {indice} -> {ruta_bloque} ({len(bloque)} bytes  )")

            indice += 1
        print(f"Total de bloques generados: {indice}")    
        
def recontruir_archivo(carpeta_bloques, archivo_salida):
    
    #lsita de nombres de archivos
    archivos = os.listdir(carpeta_bloques)
    
    #Filtrar solo los que empiecen con block_ 
    archivos = [a for a in archivos if a.startswhith("block_")]
    
    


if __name__ == "__main__":

    ruta_archivo_original = r"archivos_prueba\vieja_en_fondo_rojo.jpg"
    carpeta_bloques = r"espacioCompartido\bloques"

    # Partir el archivo en bloques de 1 MB
    partir_archivo(ruta_archivo_original, carpeta_bloques)
    
    def extraer_indice(nombre):
        #nombre = "block_0.bin"
        sin_prefijo = nombre[len("block_"):]
        numero_str = sin_prefijo.split(".")[0]
        return int(numero_str)
    
    