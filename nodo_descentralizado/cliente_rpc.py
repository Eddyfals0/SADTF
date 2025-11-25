"""Cliente RPC - Funciones para comunicarse con otros nodos"""
import socket
import json
from typing import Dict, Any, Optional, Tuple
import time


class ClienteRPC:
    """Cliente para comunicarse con otros nodos mediante RPC"""
    
    def __init__(self, timeout: int = 5):
        """
        Args:
            timeout: Timeout en segundos para conexiones
        """
        self.timeout = timeout
    
    def enviar_mensaje(self, host: str, puerto: int, mensaje_bytes: bytes) -> Optional[bytes]:
        """Envía un mensaje a otro nodo y espera respuesta
        
        Returns:
            Respuesta del nodo o None si hubo error
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, puerto))
            sock.sendall(mensaje_bytes)
            
            # Recibir respuesta
            respuesta = sock.recv(65536)
            sock.close()
            
            return respuesta
        except (socket.timeout, socket.error, ConnectionRefusedError) as e:
            return None
    
    def registrar_en_coordinador(self, host: str, puerto: int, 
                                 nodo_info: Dict[str, Any]) -> Tuple[bool, str]:
        """Registra este nodo en el coordinador"""
        # Este método sería llamado en un nodo descentralizado
        # Por ahora es un placeholder para sistemas híbridos
        return True, "Registrado"
    
    def obtener_lista_nodos(self, host: str, puerto: int) -> Optional[Dict]:
        """Obtiene la lista de nodos desde otro nodo"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, puerto))
            
            # Enviar solicitud (format: comando\n)
            sock.sendall(b"GET_NODES\n")
            
            respuesta = sock.recv(65536)
            sock.close()
            
            if respuesta:
                return json.loads(respuesta.decode('utf-8'))
            return None
        except:
            return None
    
    def enviar_heartbeat(self, host: str, puerto: int, nodo_id: str) -> bool:
        """Envía un heartbeat a otro nodo"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, puerto))
            
            msg = json.dumps({"tipo": "HEARTBEAT", "nodo_id": nodo_id})
            sock.sendall((msg + "\n").encode('utf-8'))
            
            sock.close()
            return True
        except:
            return False
    
    def solicitar_bloque(self, host: str, puerto: int, bloque_id: int) -> Optional[bytes]:
        """Solicita un bloque a otro nodo"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, puerto))
            
            msg = json.dumps({"tipo": "FETCH_BLOCK", "bloque_id": bloque_id})
            sock.sendall((msg + "\n").encode('utf-8'))
            
            # Recibir bloque (puede ser grande)
            bloques = []
            while True:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                bloques.append(chunk)
            
            sock.close()
            return b''.join(bloques) if bloques else None
        except:
            return None
    
    def enviar_bloque_a_nodo(self, host: str, puerto: int, 
                            bloque_id: int, datos: bytes) -> bool:
        """Envía un bloque a otro nodo (para replicación)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, puerto))
            
            # Header del mensaje
            header = json.dumps({
                "tipo": "STORE_BLOCK",
                "bloque_id": bloque_id,
                "size": len(datos)
            }).encode('utf-8')
            
            sock.sendall(header + b"\n")
            sock.sendall(datos)
            
            sock.close()
            return True
        except:
            return False
