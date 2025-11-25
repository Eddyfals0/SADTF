"""API de Archivos - Lógica de PUT/GET/DELETE de archivos"""
import uuid
import math
from typing import Dict, List, Optional, Tuple
import threading


class APIArchivos:
    """API para operaciones de archivos (subir, descargar, eliminar)"""
    
    TAMANIO_BLOQUE = 1048576  # 1 MB en bytes
    REPLICAS = 2  # Número de replicas por bloque
    
    def __init__(self, tabla_nodos, tabla_bloques, storage_manager, cliente_rpc, logger=None):
        """
        Args:
            tabla_nodos: Instancia de TablaNodos
            tabla_bloques: Instancia de TablaBloques
            storage_manager: Instancia de StorageManager
            cliente_rpc: Instancia de ClienteRPC
            logger: Logger
        """
        self.tabla_nodos = tabla_nodos
        self.tabla_bloques = tabla_bloques
        self.storage = storage_manager
        self.cliente_rpc = cliente_rpc
        self.logger = logger
        self.lock = threading.Lock()
    
    def subir_archivo(self, nombre_archivo: str, datos: bytes, 
                     propietario: str = "anonimo") -> Tuple[bool, str]:
        """Sube un archivo al sistema distribuido
        
        Returns:
            (éxito, archivo_id o mensaje_error)
        """
        with self.lock:
            try:
                # Calcular número de bloques necesarios
                num_bloques = math.ceil(len(datos) / self.TAMANIO_BLOQUE)
                
                # Verificar espacio disponible
                if self.tabla_bloques.obtener_bloques_libres() < (num_bloques * self.REPLICAS):
                    return False, "Espacio insuficiente en el cluster"
                
                # Asignar bloques
                bloques_asignados = self.tabla_bloques.asignar_bloques(
                    f"file_{uuid.uuid4()}", num_bloques
                )
                
                # Partir el archivo en bloques
                bloques_datos = []
                for i in range(num_bloques):
                    inicio = i * self.TAMANIO_BLOQUE
                    fin = min(inicio + self.TAMANIO_BLOQUE, len(datos))
                    bloques_datos.append(datos[inicio:fin])
                
                # Obtener nodos activos
                nodos_activos = list(self.tabla_nodos.obtener_nodos_activos().keys())
                if not nodos_activos:
                    return False, "No hay nodos activos disponibles"
                
                # Guardar bloques localmente y replicar
                archivo_id = f"file_{uuid.uuid4()}"
                for bloque_idx, (bloque_id, datos_bloque) in enumerate(
                    zip(bloques_asignados, bloques_datos)
                ):
                    # Guardar localmente
                    self.storage.guardar_bloque(bloque_id, datos_bloque)
                    self.tabla_bloques.registrar_replica(bloque_id, nodos_activos[0])
                    
                    # Replicar en otro nodo
                    if len(nodos_activos) > 1:
                        nodo_replica = nodos_activos[1]
                        info_nodo = self.tabla_nodos.obtener_nodo(nodo_replica)
                        if info_nodo:
                            self.cliente_rpc.enviar_bloque_a_nodo(
                                info_nodo["host"], info_nodo["puerto"],
                                bloque_id, datos_bloque
                            )
                            self.tabla_bloques.registrar_replica(bloque_id, nodo_replica)
                
                # Registrar archivo
                self.tabla_bloques.registrar_archivo(
                    archivo_id, nombre_archivo, propietario,
                    bloques_asignados, len(datos)
                )
                
                if self.logger:
                    self.logger.info(f"Archivo subido: {archivo_id} ({len(datos)} bytes en {num_bloques} bloques)")
                
                return True, archivo_id
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error subiendo archivo: {e}")
                return False, str(e)
    
    def descargar_archivo(self, archivo_id: str) -> Tuple[bool, bytes]:
        """Descarga un archivo del sistema distribuido
        
        Returns:
            (éxito, datos_del_archivo)
        """
        with self.lock:
            try:
                info_archivo = self.tabla_bloques.obtener_archivo(archivo_id)
                if not info_archivo:
                    return False, b""
                
                # Recuperar bloques
                bloques_data = []
                for bloque_id in info_archivo["bloques"]:
                    # Intentar leer localmente primero
                    datos = self.storage.leer_bloque(bloque_id)
                    
                    if not datos:
                        # Intentar obtener desde réplica
                        replicas = self.tabla_bloques.obtener_replicas(bloque_id)
                        for nodo_id in replicas:
                            info_nodo = self.tabla_nodos.obtener_nodo(nodo_id)
                            if info_nodo:
                                datos = self.cliente_rpc.solicitar_bloque(
                                    info_nodo["host"], info_nodo["puerto"], bloque_id
                                )
                                if datos:
                                    break
                    
                    if not datos:
                        return False, b""
                    
                    bloques_data.append(datos)
                
                datos_completos = b''.join(bloques_data)
                
                if self.logger:
                    self.logger.info(f"Archivo descargado: {archivo_id} ({len(datos_completos)} bytes)")
                
                return True, datos_completos
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error descargando archivo: {e}")
                return False, b""
    
    def eliminar_archivo(self, archivo_id: str) -> Tuple[bool, str]:
        """Elimina un archivo del sistema distribuido
        
        Returns:
            (éxito, mensaje)
        """
        with self.lock:
            try:
                info_archivo = self.tabla_bloques.obtener_archivo(archivo_id)
                if not info_archivo:
                    return False, "Archivo no encontrado"
                
                # Eliminar bloques locales
                for bloque_id in info_archivo["bloques"]:
                    self.storage.eliminar_bloque(bloque_id)
                
                # Eliminar de tabla de bloques
                self.tabla_bloques.liberar_bloques(archivo_id)
                
                if self.logger:
                    self.logger.info(f"Archivo eliminado: {archivo_id}")
                
                return True, "Archivo eliminado"
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error eliminando archivo: {e}")
                return False, str(e)
    
    def obtener_info_archivo(self, archivo_id: str) -> Optional[Dict]:
        """Obtiene información detallada de un archivo"""
        info_archivo = self.tabla_bloques.obtener_archivo(archivo_id)
        if not info_archivo:
            return None
        
        detalles = {
            "id": archivo_id,
            "nombre": info_archivo["nombre"],
            "propietario": info_archivo["propietario"],
            "size": info_archivo["size"],
            "bloques": []
        }
        
        for bloque_id in info_archivo["bloques"]:
            replicas = self.tabla_bloques.obtener_replicas(bloque_id)
            detalles["bloques"].append({
                "id": bloque_id,
                "replicas": replicas
            })
        
        return detalles
