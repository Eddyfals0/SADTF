"""Gestión de lectura/escritura de bloques en `espacioCompartido/` (stub)."""
from pathlib import Path

class StorageManager:
    def __init__(self, base_path: str):
        self.base = Path(base_path)
        self.base.mkdir(parents=True, exist_ok=True)

    def store_block(self, block_id: str, data: bytes):
        p = self.base / block_id
        p.write_bytes(data)

    def fetch_block(self, block_id: str) -> bytes:
        p = self.base / block_id
        return p.read_bytes()
