"""Registro de nodos y heartbeats (stub)."""

class TablaNodos:
    def __init__(self):
        self.nodos = {}

    def register(self, node_id, info):
        self.nodos[node_id] = info

    def heartbeat(self, node_id):
        print(f"Heartbeat recibido de {node_id}")
