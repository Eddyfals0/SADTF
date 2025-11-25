"""Tabla de bloques - Mapeo de bloques a nodos (similar a tabla de páginas)"""
from typing import Dict, List, Optional, Set
import threading


class TablaBloques:
    """Tabla de bloques del sistema distribuido (tipo paginación)
    
    Mapea: bloque_id -> lista de nodos donde está replicado
    """
    
    def __init__(self, total_bloques: int):
        """
        Args:
            total_bloques: Número total de bloques en el sistema
                          (suma de capacidades de todos los nodos)
        """
        self.total_bloques = total_bloques
        # bloque_id -> {"archivo_id": str, "indice": int, "replicas": [nodo_id, ...]}
        self.tabla: Dict[int, Dict] = {}
        # archivo_id -> {"nombre": str, "propietario": str, "bloques": [bloque_id, ...], "size": int}
        self.archivos: Dict[str, Dict] = {}
        self.bloques_libres: Set[int] = set(range(total_bloques))
        self.lock = threading.Lock()
    
    def asignar_bloques(self, archivo_id: str, num_bloques: int) -> List[int]:
        """Asigna bloques libres para un archivo
        
        Returns:
            Lista de IDs de bloques asignados
        """
        with self.lock:
            if len(self.bloques_libres) < num_bloques:
                raise ValueError(f"No hay suficientes bloques libres. "
                               f"Requeridos: {num_bloques}, Disponibles: {len(self.bloques_libres)}")
            
            bloques_asignados = []
            for i in range(num_bloques):
                bloque_id = self.bloques_libres.pop()
                self.tabla[bloque_id] = {
                    "archivo_id": archivo_id,
                    "indice": i,
                    "replicas": []
                }
                bloques_asignados.append(bloque_id)
            
            return bloques_asignados
    
    def registrar_replica(self, bloque_id: int, nodo_id: str):
        """Registra una réplica de un bloque en un nodo"""
        with self.lock:
            if bloque_id not in self.tabla:
                raise KeyError(f"Bloque {bloque_id} no existe")
            
            if nodo_id not in self.tabla[bloque_id]["replicas"]:
                self.tabla[bloque_id]["replicas"].append(nodo_id)
    
    def obtener_replicas(self, bloque_id: int) -> List[str]:
        """Obtiene la lista de nodos donde está replicado un bloque"""
        with self.lock:
            if bloque_id in self.tabla:
                return list(self.tabla[bloque_id]["replicas"])
            return []
    
    def liberar_bloques(self, archivo_id: str):
        """Libera los bloques de un archivo (para eliminación)"""
        with self.lock:
            if archivo_id not in self.archivos:
                raise KeyError(f"Archivo {archivo_id} no encontrado")
            
            bloques = self.archivos[archivo_id]["bloques"]
            for bloque_id in bloques:
                if bloque_id in self.tabla:
                    del self.tabla[bloque_id]
                    self.bloques_libres.add(bloque_id)
            
            del self.archivos[archivo_id]
    
    def registrar_archivo(self, archivo_id: str, nombre: str, 
                         propietario: str, bloques: List[int], size: int):
        """Registra un archivo en la tabla"""
        with self.lock:
            self.archivos[archivo_id] = {
                "nombre": nombre,
                "propietario": propietario,
                "bloques": bloques,
                "size": size,
                "timestamp": __import__('datetime').datetime.now()
            }
    
    def obtener_archivo(self, archivo_id: str) -> Optional[Dict]:
        """Obtiene información de un archivo"""
        with self.lock:
            return self.archivos.get(archivo_id)
    
    def obtener_todos_archivos(self) -> Dict[str, Dict]:
        """Obtiene todos los archivos registrados"""
        with self.lock:
            return dict(self.archivos)
    
    def obtener_bloques_libres(self) -> int:
        """Retorna el número de bloques libres"""
        with self.lock:
            return len(self.bloques_libres)
    
    def obtener_estado_tabla(self) -> Dict:
        """Retorna el estado actual de la tabla de bloques"""
        with self.lock:
            return {
                "total_bloques": self.total_bloques,
                "bloques_usados": self.total_bloques - len(self.bloques_libres),
                "bloques_libres": len(self.bloques_libres),
                "archivos": len(self.archivos)
            }
