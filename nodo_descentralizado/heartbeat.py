"""Heartbeat - Mantiene la comunicación periódica entre nodos"""
import threading
import time
from typing import Callable


class ServicioHeartbeat:
    """Servicio de heartbeat para mantener nodos sincronizados"""
    
    def __init__(self, nodo_id: str, intervalo: int = 5, logger=None):
        """
        Args:
            nodo_id: ID del nodo local
            intervalo: Intervalo en segundos entre heartbeats
            logger: Logger para mensajes
        """
        self.nodo_id = nodo_id
        self.intervalo = intervalo
        self.logger = logger
        self.activo = False
        self.hilo = None
        self.callback_heartbeat: Callable = None
    
    def registrar_callback(self, callback: Callable):
        """Registra callback para ejecutar en cada heartbeat"""
        self.callback_heartbeat = callback
    
    def iniciar(self):
        """Inicia el servicio de heartbeat"""
        if self.activo:
            return
        
        self.activo = True
        self.hilo = threading.Thread(target=self._ejecutar_loop, daemon=True)
        self.hilo.start()
        
        if self.logger:
            self.logger.info(f"Servicio de heartbeat iniciado (intervalo: {self.intervalo}s)")
    
    def _ejecutar_loop(self):
        """Loop de heartbeat"""
        while self.activo:
            try:
                if self.callback_heartbeat:
                    self.callback_heartbeat()
                
                time.sleep(self.intervalo)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error en heartbeat loop: {e}")
                time.sleep(self.intervalo)
    
    def detener(self):
        """Detiene el servicio de heartbeat"""
        self.activo = False
        if self.hilo:
            self.hilo.join(timeout=2)
        
        if self.logger:
            self.logger.info("Servicio de heartbeat detenido")
