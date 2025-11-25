"""Registro y heartbeats hacia el coordinador (stub)."""
import time

def register_node(coordinador_addr, node_info):
    print(f"Registrando nodo en {coordinador_addr} -> {node_info}")

def send_heartbeat(coordinador_addr, node_id):
    print(f"Enviando heartbeat de {node_id} a {coordinador_addr}")
