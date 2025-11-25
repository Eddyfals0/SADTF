"""Encode/decode de mensajes JSON línea por línea (stub)."""
import json

def encode(msg: dict) -> bytes:
    return (json.dumps(msg) + "\n").encode('utf-8')

def decode(line: bytes) -> dict:
    return json.loads(line.decode('utf-8'))
