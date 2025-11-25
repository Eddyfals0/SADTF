"""Tabla de bloques: qué bloque está en qué nodo (stub)."""

class TablaBloques:
    def __init__(self):
        self.tabla = {}

    def asignar_bloque(self, bloque_id, node_id):
        self.tabla[bloque_id] = node_id

    def buscar_bloque(self, bloque_id):
        return self.tabla.get(bloque_id)
