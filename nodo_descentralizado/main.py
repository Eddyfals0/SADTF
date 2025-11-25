"""Main - Punto de entrada del nodo descentralizado"""
import json
import os
import sys
import signal
from pathlib import Path

from nodo_descentralizado.utils_logger import get_logger
from nodo_descentralizado.tabla_nodos import TablaNodos
from nodo_descentralizado.tabla_bloques import TablaBloques
from nodo_descentralizado.storage_manager import StorageManager
from nodo_descentralizado.replicacion_meta import ReplicacionMetadatos
from nodo_descentralizado.cliente_rpc import ClienteRPC
from nodo_descentralizado.servidor_rpc import ServidorRPC
from nodo_descentralizado.heartbeat import ServicioHeartbeat
from nodo_descentralizado.api_archivos import APIArchivos
from nodo_descentralizado.cli import InterfazCLI


class NodoDescentralizado:
    """Nodo principal del sistema SADTF descentralizado"""
    
    def __init__(self, config_path: str = "config/nodo_config.json"):
        """Inicializa el nodo con la configuración"""
        self.config = self._cargar_config(config_path)
        self.logger = get_logger(self.config['nodo_id'])
        
        # Inicializar componentes
        self.tabla_nodos = TablaNodos(self.config.get('timeout_nodo', 15))
        
        # Calcular total de bloques (será actualizado con otros nodos)
        capacidad_mb = self.config['capacidad_mb']
        self.tabla_bloques = TablaBloques(capacidad_mb)
        
        self.storage = StorageManager(self.config['espacioCompartido'])
        self.replicacion = ReplicacionMetadatos(self.tabla_nodos, self.tabla_bloques)
        self.cliente_rpc = ClienteRPC()
        
        self.servidor_rpc = ServidorRPC(
            self.config['host'],
            self.config['puerto'],
            self.logger
        )
        
        self.api_archivos = APIArchivos(
            self.tabla_nodos,
            self.tabla_bloques,
            self.storage,
            self.cliente_rpc,
            self.logger
        )
        
        self.heartbeat = ServicioHeartbeat(
            self.config['nodo_id'],
            self.config.get('heartbeat_intervalo', 5),
            self.logger
        )
        
        self.cli = InterfazCLI(
            self.api_archivos,
            self.tabla_bloques,
            self.tabla_nodos,
            self.logger
        )
        
        # Registrar este nodo
        self._registrar_nodo_local()
    
    def _cargar_config(self, config_path: str) -> dict:
        """Carga la configuración desde JSON"""
        if not os.path.exists(config_path):
            self.logger = get_logger("SADTF")
            self.logger.error(f"Archivo de configuración no encontrado: {config_path}")
            raise FileNotFoundError(config_path)
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _registrar_nodo_local(self):
        """Registra este nodo en la tabla local"""
        self.tabla_nodos.registrar_nodo(
            self.config['nodo_id'],
            {
                'host': self.config['host'],
                'puerto': self.config['puerto'],
                'capacidad_mb': self.config['capacidad_mb']
            }
        )
        self.logger.info(f"Nodo {self.config['nodo_id']} registrado localmente")
    
    def _registrar_handlers_rpc(self):
        """Registra los handlers para mensajes RPC"""
        def handler_heartbeat(header, payload, sock):
            nodo_id = header.get('nodo_id')
            try:
                self.tabla_nodos.actualizar_heartbeat(nodo_id)
                self.logger.debug(f"Heartbeat recibido de {nodo_id}")
                return b'{"status": "ok"}\n'
            except:
                return b'{"status": "error"}\n'
        
        def handler_store_block(header, payload, sock):
            bloque_id = header.get('bloque_id')
            size = header.get('size')
            try:
                datos = payload[:size] if size else payload
                self.storage.guardar_bloque(bloque_id, datos)
                self.logger.debug(f"Bloque {bloque_id} almacenado ({size} bytes)")
                return b'{"status": "ok"}\n'
            except Exception as e:
                self.logger.error(f"Error almacenando bloque: {e}")
                return b'{"status": "error"}\n'
        
        def handler_fetch_block(header, payload, sock):
            bloque_id = header.get('bloque_id')
            try:
                datos = self.storage.leer_bloque(bloque_id)
                if datos:
                    sock.sendall(datos)
                    return None  # Ya se envió
                else:
                    return b'{"status": "not_found"}\n'
            except Exception as e:
                self.logger.error(f"Error leyendo bloque: {e}")
                return b'{"status": "error"}\n'
        
        self.servidor_rpc.registrar_handler('HEARTBEAT', handler_heartbeat)
        self.servidor_rpc.registrar_handler('STORE_BLOCK', handler_store_block)
        self.servidor_rpc.registrar_handler('FETCH_BLOCK', handler_fetch_block)
    
    def iniciar(self):
        """Inicia todos los servicios del nodo"""
        self.logger.info("Iniciando nodo descentralizado...")
        
        # Registrar handlers RPC
        self._registrar_handlers_rpc()
        
        # Iniciar servidor RPC
        self.servidor_rpc.iniciar()
        
        # Iniciar servicio de heartbeat
        self.heartbeat.registrar_callback(self._enviar_heartbeat)
        self.heartbeat.iniciar()
        
        self.logger.info(f"Nodo {self.config['nodo_id']} iniciado correctamente")
    
    def _enviar_heartbeat(self):
        """Envía heartbeat a otros nodos conocidos"""
        for nodo_id, info in self.tabla_nodos.obtener_todos_nodos().items():
            if nodo_id != self.config['nodo_id']:
                try:
                    self.cliente_rpc.enviar_heartbeat(
                        info['host'], info['puerto'],
                        self.config['nodo_id']
                    )
                except Exception as e:
                    self.logger.debug(f"Error enviando heartbeat a {nodo_id}: {e}")
    
    def ejecutar_cli(self):
        """Ejecuta la interfaz CLI"""
        self.logger.info("Iniciando interfaz CLI...")
        self.cli.ejecutar()
    
    def detener(self):
        """Detiene todos los servicios"""
        self.logger.info("Deteniendo servicios...")
        self.heartbeat.detener()
        self.servidor_rpc.detener()
        self.logger.info("Nodo detenido")


def main():
    """Función principal"""
    try:
        # Cargar configuración
        config_path = "config/nodo_config.json"
        nodo = NodoDescentralizado(config_path)
        
        # Iniciar servicios
        nodo.iniciar()
        
        # Configurar manejador de señal para Ctrl+C
        def signal_handler(sig, frame):
            print("\n")
            nodo.detener()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Ejecutar CLI
        nodo.ejecutar_cli()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
