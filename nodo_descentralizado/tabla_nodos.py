"""Tabla de nodos - Registro de nodos activos del cluster"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import threading


class TablaNodos:
    """Tabla que mantiene registro de nodos activos en el cluster"""
    
    def __init__(self, timeout_segundos: int = 15):
        self.nodos: Dict[str, Dict[str, Any]] = {}
        self.timeout = timeout_segundos
        self.lock = threading.Lock()
    
    def registrar_nodo(self, nodo_id: str, info: Dict[str, Any]):
        """Registra un nodo en la tabla"""
        with self.lock:
            self.nodos[nodo_id] = {
                "id": nodo_id,
                "host": info.get("host"),
                "puerto": info.get("puerto"),
                "capacidad_mb": info.get("capacidad_mb"),
                "espacio_libre_mb": info.get("capacidad_mb"),
                "ultimo_heartbeat": datetime.now(),
                "estado": "activo"
            }
    
    def actualizar_heartbeat(self, nodo_id: str):
        """Actualiza el timestamp del último heartbeat"""
        with self.lock:
            if nodo_id in self.nodos:
                self.nodos[nodo_id]["ultimo_heartbeat"] = datetime.now()
            else:
                raise KeyError(f"Nodo {nodo_id} no encontrado")
    
    def obtener_nodo(self, nodo_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de un nodo"""
        with self.lock:
            return self.nodos.get(nodo_id)
    
    def obtener_todos_nodos(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene todos los nodos registrados"""
        with self.lock:
            return dict(self.nodos)
    
    def obtener_nodos_activos(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene solo los nodos activos (no expirados)"""
        with self.lock:
            ahora = datetime.now()
            activos = {}
            for nodo_id, info in self.nodos.items():
                tiempo_sin_latido = ahora - info["ultimo_heartbeat"]
                if tiempo_sin_latido < timedelta(seconds=self.timeout):
                    activos[nodo_id] = info
                else:
                    info["estado"] = "inactivo"
            return activos
    
    def eliminar_nodo(self, nodo_id: str):
        """Elimina un nodo de la tabla"""
        with self.lock:
            if nodo_id in self.nodos:
                del self.nodos[nodo_id]
    
    def actualizar_espacio_libre(self, nodo_id: str, espacio_mb: int):
        """Actualiza el espacio libre disponible en un nodo"""
        with self.lock:
            if nodo_id in self.nodos:
                self.nodos[nodo_id]["espacio_libre_mb"] = espacio_mb
    
    def obtener_nodo_con_espacio(self, bloques_requeridos: int) -> Optional[str]:
        """Obtiene un nodo con espacio suficiente para los bloques"""
        with self.lock:
            for nodo_id, info in self.nodos.items():
                if info["espacio_libre_mb"] >= bloques_requeridos:
                    return nodo_id
            return None
