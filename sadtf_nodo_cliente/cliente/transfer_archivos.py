"""Enviar/recibir bloques a/de nodos (stub)."""
import socket

def send_block(node_addr, block_id, data):
    print(f"Enviando bloque {block_id} a {node_addr} (stub)")

def fetch_block(node_addr, block_id):
    print(f"Pidiendo bloque {block_id} a {node_addr} (stub)")
