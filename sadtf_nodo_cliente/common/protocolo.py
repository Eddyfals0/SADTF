"""Protocolo compartido (encode/decode) - debe coincidir con el coordinador."""
import json

def encode(msg: dict) -> bytes:
    return (json.dumps(msg) + "\n").encode('utf-8')

def decode(line: bytes) -> dict:
    return json.loads(line.decode('utf-8'))
