"""Storage Manager - Gestión de lectura/escritura de bloques en disco"""
import os
import hashlib
from typing import Optional, Tuple
import threading


class StorageManager:
    """Gestor de almacenamiento de bloques en disco"""
    
    def __init__(self, ruta_espacio: str, tamanio_bloque_bytes: int = 1048576):
        """
        Args:
            ruta_espacio: Ruta del directorio espacioCompartido
            tamanio_bloque_bytes: Tamaño de cada bloque en bytes (default: 1 MB)
        """
        self.ruta_espacio = ruta_espacio
        self.tamanio_bloque = tamanio_bloque_bytes
        self.lock = threading.Lock()
        
        # Crear directorio si no existe
        if not os.path.exists(ruta_espacio):
            os.makedirs(ruta_espacio)
    
    def guardar_bloque(self, bloque_id: int, datos: bytes) -> Tuple[bool, str]:
        """Guarda un bloque en disco
        
        Returns:
            (éxito, hash_del_bloque)
        """
        with self.lock:
            try:
                ruta_bloque = os.path.join(self.ruta_espacio, f"block_{bloque_id}.dat")
                
                with open(ruta_bloque, 'wb') as f:
                    f.write(datos)
                
                # Calcular hash para verificación
                hash_obj = hashlib.sha256(datos)
                hash_bloque = hash_obj.hexdigest()
                
                return True, hash_bloque
            except IOError as e:
                return False, str(e)
    
    def leer_bloque(self, bloque_id: int) -> Optional[bytes]:
        """Lee un bloque del disco
        
        Returns:
            Datos del bloque o None si no existe
        """
        with self.lock:
            try:
                ruta_bloque = os.path.join(self.ruta_espacio, f"block_{bloque_id}.dat")
                
                if not os.path.exists(ruta_bloque):
                    return None
                
                with open(ruta_bloque, 'rb') as f:
                    return f.read()
            except IOError:
                return None
    
    def eliminar_bloque(self, bloque_id: int) -> bool:
        """Elimina un bloque del disco"""
        with self.lock:
            try:
                ruta_bloque = os.path.join(self.ruta_espacio, f"block_{bloque_id}.dat")
                
                if os.path.exists(ruta_bloque):
                    os.remove(ruta_bloque)
                    return True
                return False
            except IOError:
                return False
    
    def obtener_espacio_disponible(self) -> int:
        """Obtiene el espacio disponible en bytes"""
        try:
            stat = os.statvfs(self.ruta_espacio)
            return stat.f_bavail * stat.f_frsize
        except:
            return 0
    
    def obtener_espacio_usado(self) -> int:
        """Obtiene el espacio usado por bloques en bytes"""
        with self.lock:
            total = 0
            try:
                for archivo in os.listdir(self.ruta_espacio):
                    if archivo.startswith("block_") and archivo.endswith(".dat"):
                        ruta = os.path.join(self.ruta_espacio, archivo)
                        total += os.path.getsize(ruta)
            except:
                pass
            return total
    
    def obtener_bloques_locales(self) -> list:
        """Obtiene la lista de IDs de bloques almacenados localmente"""
        with self.lock:
            bloques = []
            try:
                for archivo in os.listdir(self.ruta_espacio):
                    if archivo.startswith("block_") and archivo.endswith(".dat"):
                        bloque_id = int(archivo.replace("block_", "").replace(".dat", ""))
                        bloques.append(bloque_id)
            except:
                pass
            return bloques
