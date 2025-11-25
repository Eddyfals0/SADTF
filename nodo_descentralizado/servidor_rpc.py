"""Servidor RPC - Acepta conexiones de otros nodos y del cliente"""
import socket
import threading
import json
from typing import Callable, Dict, Any
import struct


class ServidorRPC:
    """Servidor TCP que maneja peticiones RPC de otros nodos y del cliente"""
    
    def __init__(self, host: str, puerto: int, logger=None):
        """
        Args:
            host: IP del servidor
            puerto: Puerto del servidor
            logger: Logger para mensajes
        """
        self.host = host
        self.puerto = puerto
        self.logger = logger
        self.socket_servidor = None
        self.activo = False
        self.hilo_aceptar = None
        self.handlers: Dict[str, Callable] = {}
    
    def registrar_handler(self, tipo_mensaje: str, callback: Callable):
        """Registra un handler para un tipo de mensaje"""
        self.handlers[tipo_mensaje] = callback
    
    def iniciar(self):
        """Inicia el servidor RPC"""
        if self.activo:
            return
        
        try:
            self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_servidor.bind((self.host, self.puerto))
            self.socket_servidor.listen(5)
            self.activo = True
            
            self.hilo_aceptar = threading.Thread(target=self._loop_accept, daemon=True)
            self.hilo_aceptar.start()
            
            if self.logger:
                self.logger.info(f"Servidor RPC iniciado en {self.host}:{self.puerto}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error al iniciar servidor RPC: {e}")
    
    def _loop_accept(self):
        """Loop de aceptación de conexiones"""
        while self.activo:
            try:
                cliente_sock, addr = self.socket_servidor.accept()
                hilo = threading.Thread(target=self._manejar_cliente, 
                                      args=(cliente_sock, addr), daemon=True)
                hilo.start()
            except Exception as e:
                if self.logger and self.activo:
                    self.logger.error(f"Error en accept: {e}")
    
    def _manejar_cliente(self, sock: socket.socket, addr: tuple):
        """Maneja una conexión de cliente"""
        try:
            sock.settimeout(30)
            
            # Leer primer línea (header JSON)
            datos = b''
            while b'\n' not in datos:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                datos += chunk
            
            if b'\n' not in datos:
                return
            
            header_str = datos[:datos.index(b'\n')].decode('utf-8')
            payload = datos[datos.index(b'\n')+1:]
            
            try:
                header = json.loads(header_str)
                tipo = header.get('tipo')
                
                if tipo in self.handlers:
                    respuesta = self.handlers[tipo](header, payload, sock)
                    if respuesta and isinstance(respuesta, bytes):
                        sock.sendall(respuesta)
                else:
                    if self.logger:
                        self.logger.warning(f"Handler no encontrado para: {tipo}")
                    sock.sendall(b'{"error": "Handler not found"}\n')
            except json.JSONDecodeError:
                sock.sendall(b'{"error": "Invalid JSON"}\n')
        except socket.timeout:
            pass
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error manejando cliente: {e}")
        finally:
            try:
                sock.close()
            except:
                pass
    
    def detener(self):
        """Detiene el servidor RPC"""
        self.activo = False
        if self.socket_servidor:
            try:
                self.socket_servidor.close()
            except:
                pass
        if self.hilo_aceptar:
            self.hilo_aceptar.join(timeout=2)
        
        if self.logger:
            self.logger.info("Servidor RPC detenido")
