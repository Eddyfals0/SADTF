"""Logger para SADTF - Impresión ordenada de logs"""
import logging
import sys
from datetime import datetime


class LoggerSADTF:
    """Logger personalizado para SADTF"""
    
    def __init__(self, nodo_id: str = "nodo"):
        self.nodo_id = nodo_id
        self.logger = logging.getLogger(nodo_id)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                f'[{nodo_id}] %(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def info(self, msg: str):
        self.logger.info(msg)
    
    def warning(self, msg: str):
        self.logger.warning(msg)
    
    def error(self, msg: str):
        self.logger.error(msg)
    
    def debug(self, msg: str):
        self.logger.debug(msg)


def get_logger(nodo_id: str = "nodo") -> LoggerSADTF:
    """Obtiene o crea un logger para el nodo"""
    return LoggerSADTF(nodo_id)
