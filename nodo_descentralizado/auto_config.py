"""
Auto-configuración del Nodo
Genera automáticamente la configuración sin intervención del usuario
"""

import os
import json
import socket
from pathlib import Path


class AutoConfig:
    """Auto-genera configuración para cada PC automáticamente"""

    def __init__(self, config_path="config/nodo_config.json"):
        self.config_path = config_path
        self.config = {}

    def obtener_ip_local(self):
        """Obtiene la IP local de la PC automáticamente"""
        try:
            # Conectar a un servidor DNS (no envía datos, solo obtiene IP)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def obtener_puerto_libre(self, puerto_base=9000):
        """Encuentra un puerto libre automáticamente"""
        puerto = puerto_base
        max_intentos = 100

        for _ in range(max_intentos):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("127.0.0.1", puerto))
                s.close()
                return puerto
            except OSError:
                puerto += 1

        return puerto_base

    def obtener_nombre_pc(self):
        """Obtiene el nombre de la PC"""
        try:
            return socket.gethostname()
        except:
            return "nodo_1"

    def generar_config_automatica(self):
        """Genera configuración automática"""
        ip = self.obtener_ip_local()
        puerto = self.obtener_puerto_libre(9000)
        nombre_pc = self.obtener_nombre_pc().lower()
        nodo_id = f"nodo_{nombre_pc}"

        self.config = {
            "nodo_id": nodo_id,
            "host": ip,
            "puerto": puerto,
            "capacidad_mb": 100,
            "espacioCompartido": "./espacioCompartido",
            "nodo_bootstrap": "127.0.0.1:9001",
            "heartbeat_intervalo": 5,
            "timeout_nodo": 15,
            "nombre_pc": nombre_pc,
            "generado_automaticamente": True,
        }

        return self.config

    def cargar_o_crear(self):
        """Carga config existente o crea una nueva automáticamente"""
        # Si existe config, cargarla
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    self.config = json.load(f)
                return self.config
            except:
                pass

        # Si no existe, generar automáticamente
        self.generar_config_automatica()
        self.guardar()
        return self.config

    def guardar(self):
        """Guarda la configuración en JSON"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def mostrar_info(self):
        """Muestra la configuración actual"""
        if not self.config:
            self.cargar_o_crear()

        print("\n" + "=" * 50)
        print("⚙️  CONFIGURACIÓN DEL NODO (AUTO-GENERADA)")
        print("=" * 50)
        print(f"  ID del Nodo:           {self.config.get('nodo_id')}")
        print(f"  Host:                  {self.config.get('host')}")
        print(f"  Puerto:                {self.config.get('puerto')}")
        print(f"  Capacidad:             {self.config.get('capacidad_mb')} MB")
        print(f"  Nombre PC:             {self.config.get('nombre_pc')}")
        print(f"  Almacenamiento:        {self.config.get('espacioCompartido')}")
        print(f"  Bootstrap:             {self.config.get('nodo_bootstrap')}")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    # Ejemplo de uso
    auto = AutoConfig()
    config = auto.cargar_o_crear()
    auto.mostrar_info()
