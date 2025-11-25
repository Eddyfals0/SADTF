#!/usr/bin/env python3
"""Script para generar configuración de múltiples nodos rápidamente"""
import json
import os
import sys


def crear_config_nodo(nodo_id: int, puerto_base: int = 9000, 
                     capacidad_mb: int = 50, host: str = "127.0.0.1"):
    """Crea configuración para un nodo"""
    return {
        "nodo_id": f"nodo_{nodo_id}",
        "host": host,
        "puerto": puerto_base + nodo_id,
        "capacidad_mb": capacidad_mb,
        "espacioCompartido": "./espacioCompartido",
        "nodo_bootstrap": f"{host}:{puerto_base + 1}",
        "heartbeat_intervalo": 5,
        "timeout_nodo": 15
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python setup_config.py <numero_nodos> [puerto_base] [capacidad_mb] [host]")
        print("Ejemplo: python setup_config.py 3 9000 50 127.0.0.1")
        sys.exit(1)
    
    num_nodos = int(sys.argv[1])
    puerto_base = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
    capacidad_mb = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    host = sys.argv[4] if len(sys.argv) > 4 else "127.0.0.1"
    
    os.makedirs("config", exist_ok=True)
    
    for i in range(1, num_nodos + 1):
        config = crear_config_nodo(i, puerto_base, capacidad_mb, host)
        config_path = f"config/nodo_{i}_config.json"
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Creado: {config_path}")
    
    print(f"\nTotal: {num_nodos} configuraciones creadas")
    print("Capacidad total del cluster:", num_nodos * capacidad_mb, "MB")


if __name__ == '__main__':
    main()
