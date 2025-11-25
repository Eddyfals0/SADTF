"""Protocolo de mensajes - Formato JSON línea por línea"""
import json
from enum import Enum
from typing import Dict, Any


class TipoMensaje(Enum):
    """Tipos de mensajes del protocolo RPC"""
    HEARTBEAT = "HEARTBEAT"
    REGISTER_NODE = "REGISTER_NODE"
    GET_NODES = "GET_NODES"
    GET_BLOCK_TABLE = "GET_BLOCK_TABLE"
    PUT_FILE = "PUT_FILE"
    GET_FILE = "GET_FILE"
    DELETE_FILE = "DELETE_FILE"
    STORE_BLOCK = "STORE_BLOCK"
    FETCH_BLOCK = "FETCH_BLOCK"
    REPLICATE_METADATA = "REPLICATE_METADATA"
    REPLICA_BLOCK = "REPLICA_BLOCK"
    ACK = "ACK"
    ERROR = "ERROR"


class Mensaje:
    """Clase para encapsular mensajes del protocolo"""
    
    def __init__(self, tipo: TipoMensaje, payload: Dict[str, Any], id_msg: str = ""):
        self.tipo = tipo
        self.payload = payload
        self.id_msg = id_msg
    
    def to_json(self) -> str:
        """Serializa a JSON"""
        return json.dumps({
            "tipo": self.tipo.value,
            "payload": self.payload,
            "id_msg": self.id_msg
        })
    
    def to_bytes(self) -> bytes:
        """Serializa a bytes (JSON + newline)"""
        return (self.to_json() + "\n").encode('utf-8')
    
    @staticmethod
    def from_bytes(data: bytes) -> 'Mensaje':
        """Deserializa desde bytes"""
        obj = json.loads(data.decode('utf-8').strip())
        return Mensaje(
            tipo=TipoMensaje(obj['tipo']),
            payload=obj['payload'],
            id_msg=obj.get('id_msg', '')
        )


def encode_msg(tipo: TipoMensaje, payload: Dict) -> bytes:
    """Helper para codificar mensaje"""
    msg = Mensaje(tipo, payload)
    return msg.to_bytes()


def decode_msg(data: bytes) -> Mensaje:
    """Helper para decodificar mensaje"""
    return Mensaje.from_bytes(data)
