# Diseño de arquitectura

Este documento describe la arquitectura propuesta para el sistema distribuido tolerante a fallas (SADTF). Está pensado como material de referencia para entender los módulos, los flujos principales (subir, descargar, eliminar archivos) y las estructuras de datos que implementaremos en el repositorio.

## Visión general

SADTF permite almacenar archivos grandes dividiéndolos en bloques de 1 Mbyte y distribuyéndolos entre `n` nodos (computadoras). Cada nodo expone un directorio `espacioCompartido` con capacidad configurable (50–100 MB por nodo en la especificación, pero el valor debe ser configurable). La suma de las capacidades de todos los nodos es la capacidad global del sistema.

Elementos principales:
- `coordinator/`: componente central que mantiene la tabla global de bloques, registro de archivos y la lista de nodos disponibles.
- `storage_node/`: servicio que corre en cada nodo y gestiona su `espacioCompartido` (almacena/borra bloques, reporta espacio libre y responde heartbeats).
- `common/`: utilidades y modelos compartidos (p. ej. `file_utils.py`, `models.py`, `network_utils.py`).
- `gui/`: interfaz web que muestra nodos, archivos y permite subir/descargar/eliminar archivos.
- `config/`: archivos JSON con parámetros del coordinador y nodos.

## Estructuras de datos clave

- Block: unidad física de 1 MB. Cada bloque se guarda como un archivo independiente dentro de `espacioCompartido`.
- BlockEntry: registro en la tabla de bloques que indica si la entrada está ocupada y, en su caso, los metadatos del bloque (ID, referencia al archivo, índice dentro del archivo, nodos donde existe).
- FileEntry: metadatos por archivo (ID, nombre, tamaño, lista de bloques que lo componen).

En el código base estas estructuras están representadas como dataclasses en `common/models.py`.

## Tabla global de bloques (similar a tabla de páginas)

- La tabla tiene tantas entradas como Mbytes totales del sistema (ej.: 220 entradas para 220 MB). Cada entrada representa un bloque físico de 1 MB.
- La tabla mapea entradas libres/ocupadas y, para las entradas ocupadas, al `block_id` y metadatos necesarios.
- El coordinador es responsable de asignar entradas libres al subir archivos y de liberarlas al eliminar archivos.

## Replicación y tolerancia a fallas

- `replication_factor` (configurable en `config/coordinator_config.json`) define cuántas copias guardar por bloque. Por defecto en `requirements.txt`/config ejemplo usamos 3.
- Al almacenar un bloque, el coordinador elige `replication_factor` nodos distintos (preferiblemente con suficiente espacio libre) y hace `POST` a sus APIs (`/store_block`) para que guarden la copia.
- Si un nodo falla (heartbeats perdidos), el coordinador marca sus bloques como no disponibles y, si alguna entrada queda por debajo de la réplica deseada, programa re-replicación hacia nodos saludables.

## Capacidad y cuotas

- Cada nodo comunica su `free_space` al coordinador mediante heartbeats o en respuesta a consultas (`/free_space`).
- La suma de las capacidades disponibles constituye la capacidad total reportada por la GUI y usada por el coordinador para asignación de bloques.

## Flujos principales (paso a paso)

1) Subir (guardar) un archivo
	- El cliente (GUI o CLI) envía el archivo al coordinador.
	- `file_utils.split_file` divide el archivo en bloques de 1 MB (último bloque puede ser menor).
	- Para cada bloque el coordinador selecciona `replication_factor` nodos con espacio suficiente.
	- El coordinador solicita a cada nodo que almacene el bloque (`POST /store_block`), y cuando todas (o la mayoría configurable) confirman, registra el `BlockEntry` en la `BlockTable` y registra la `FileEntry` en el `FileManager`.
	- Si alguna réplica falla, el coordinador intenta reintentar o elegir otro nodo.

2) Descargar un archivo
	- El cliente solicita la descarga al coordinador.
	- El coordinador responde con la lista de `block_id` y las ubicaciones (nodos) donde conseguir cada bloque.
	- El cliente (o un componente descargador) pide cada bloque a un nodo disponible y usa `file_utils.rebuild_file` para recomponer el archivo localmente.
	- Si una réplica falta, se usa otra réplica; si faltan réplicas y no alcanza para reconstruir, se informa error.

3) Eliminar un archivo
	- El cliente solicita eliminación al coordinador.
	- El coordinador marca las entradas de la tabla de bloques usadas por ese archivo como libres y envía solicitudes a los nodos para borrar los archivos de bloque.
	- Actualiza `FileManager` y libera espacio.

4) Consultas y metadatos
	- La GUI puede pedir la tabla de bloques, la lista de archivos, y los detalles de un archivo (bloques y nodos donde están).

## Comportamiento de nodos y heartbeat

- Cada `storage_node` periódicamente envía un heartbeat al coordinador con su `node_id`, `free_space` y estado.
- El coordinador mantiene la lista de nodos con timestamp de último heartbeat. Si un nodo no responde en `X` segundos, se marca como caído.

## Componentes en el repositorio (mapeo a archivos)

- `common/file_utils.py`: funciones para partir y reconstruir archivos (bloques de 1 MB). Aquí añadiremos funciones para generar checksums por bloque y metadatos.
- `common/models.py`: `BlockEntry`, `FileEntry`, `NodeInfo`.
- `coordinator/block_table.py`: almacena la tabla global de bloques.
- `coordinator/file_manager.py`: administra metadatos de archivos.
- `coordinator/node_manager.py`: mantiene lista de nodos y espacio libre.
- `storage_node/storage_manager.py`: guarda/borra bloques en `espacioCompartido`.
- `gui/`: servidor web y plantillas.

## Integridad (checksums) y verificación

- Recomendación: calcular un checksum (p. ej. SHA-256) por bloque al partir el archivo. Guardar ese checksum en el `BlockEntry` y, al descargar, verificar que los bytes recuperados coincidan con el checksum.
- Si un checksum no coincide, intentar descargar otra réplica.

## Pruebas y notas

- `tests/test_file_utils.py` contiene ejemplos automáticos para partir y reconstruir archivos (ya existe un test básico). Lo usaremos para explicar paso a paso cómo `file_utils` funciona.
- `docs/notas_pruebas.md` debe contener instrucciones para configurar el `env`, instalar dependencias (`pip install -r requirements.txt`) y ejecutar `pytest`.

## Siguientes pasos (implementación incremental)

1. Completar la documentación de `file_utils` y añadir checksums y verificación automática (esto facilitará demostrar el flujo de subida/descarga localmente).
2. Escribir tests pedagógicos que muestren cómo partir un archivo grande, almacenarlo en carpetas simuladas de nodos (usar carpetas temporales que representen `espacioCompartido/nodeX`) y reconstruirlo.
3. Implementar endpoints básicos del `storage_node` y del `coordinator` para simular la comunicación.
4. Construir la GUI sobre esos endpoints.

---

Si te parece bien, el primer archivo práctico que implementemos y expliquemos con pruebas será `common/file_utils.py`: añadiremos cálculos de checksum, un CLI pequeño para partir/reconstruir con ejemplos, y tests que te muestren paso a paso cómo funciona. ¿Deseas que continúe con esa implementación ahora? (Respuesta: "sí" para que implemente `file_utils` con tests; "no" o pide otro archivo para empezar.)

