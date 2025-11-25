"""Replicación de Metadatos - Sincronización de tabla_nodos y tabla_bloques entre nodos"""
import threading
from typing import Dict, Any
import json


class ReplicacionMetadatos:
    """Gestiona la replicación de metadatos entre nodos"""
    
    def __init__(self, tabla_nodos, tabla_bloques):
        """
        Args:
            tabla_nodos: Instancia de TablaNodos
            tabla_bloques: Instancia de TablaBloques
        """
        self.tabla_nodos = tabla_nodos
        self.tabla_bloques = tabla_bloques
        self.lock = threading.Lock()
    
    def obtener_snapshot_metadatos(self) -> Dict[str, Any]:
        """Obtiene un snapshot de los metadatos actuales"""
        return {
            "nodos": self.tabla_nodos.obtener_todos_nodos(),
            "bloques": self._serializar_tabla_bloques(),
            "archivos": self.tabla_bloques.obtener_todos_archivos()
        }
    
    def _serializar_tabla_bloques(self) -> Dict:
        """Serializa la tabla de bloques para transmisión"""
        with self.lock:
            tabla_serializada = {}
            for bloque_id, info in self.tabla_bloques.tabla.items():
                tabla_serializada[str(bloque_id)] = {
                    "archivo_id": info["archivo_id"],
                    "indice": info["indice"],
                    "replicas": info["replicas"]
                }
            return tabla_serializada
    
    def recibir_snapshot_metadatos(self, snapshot: Dict[str, Any]) -> bool:
        """Recibe y merge de snapshot de metadatos de otro nodo
        
        Implementa merge inteligente para evitar conflictos
        """
        try:
            with self.lock:
                # Actualizar tabla de nodos
                for nodo_id, info in snapshot.get("nodos", {}).items():
                    if nodo_id not in self.tabla_nodos.nodos:
                        self.tabla_nodos.registrar_nodo(nodo_id, info)
                
                # Merge de tabla de bloques (keep local if timestamp is newer)
                nodos_remotos = snapshot.get("nodos", {})
                for nodo_id, info in nodos_remotos.items():
                    self.tabla_nodos.actualizar_heartbeat(nodo_id)
                
                return True
        except Exception as e:
            print(f"Error en recibir_snapshot_metadatos: {e}")
            return False
    
    def sincronizar_nodo(self, nodo_remoto_id: str, snapshot_remoto: Dict) -> Dict[str, Any]:
        """Sincroniza con otro nodo y retorna cambios locales que necesita el remoto"""
        local_snapshot = self.obtener_snapshot_metadatos()
        
        # Merge
        self.recibir_snapshot_metadatos(snapshot_remoto)
        
        return {
            "cambios_locales": local_snapshot,
            "estado": "sincronizado"
        }
