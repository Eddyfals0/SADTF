# Diseño de Arquitectura - SADTF

Sistema de Almacenamiento Distribuido Tolerante a Fallas (Descentralizado)

---

## 🏗️ Arquitectura General

```
┌──────────────┐  RPC   ┌──────────────┐  RPC   ┌──────────────┐
│   NODO 1     ├────────┤   NODO 2     ├────────┤   NODO 3     │
│ 9001 | 50MB  │        │ 9002 | 70MB  │        │ 9003 | 100MB │
└──────────────┘        └──────────────┘        └──────────────┘
     │                       │                       │
     └───────────────────────┼───────────────────────┘
            (Heartbeat cada 5 segundos)
```

**Características:**
- ✅ **Descentralizado**: Sin nodo maestro, todos son iguales
- ✅ **Replicación**: Cada bloque en 2 nodos diferentes
- ✅ **Tolerancia a fallas**: Puede funcionar con hasta 1 nodo caído
- ✅ **Sincronización**: Heartbeat + replicación de metadatos

---

## 📦 Componentes Principales

### 1. **main.py** - Punto de Entrada
```python
NodoDescentralizado():
  ├── Inicializa configuración (nodo_id, puerto, capacidad)
  ├── Crea TablaNodos
  ├── Crea TablaBloques
  ├── Crea StorageManager
  ├── Crea APIArchivos
  ├── Inicia ServidorRPC (escucha conexiones)
  ├── Inicia ServicioHeartbeat (latido cada 5s)
  └── Inicia InterfazCLI (menú usuario)
```

### 2. **TablaNodos** - Registro de Nodos

Estructura de datos que mantiene el estado de todos los nodos activos.

### 3. **TablaBloques** - Mapeo de Bloques (Paginación)

Similar a tabla de páginas en memoria virtual.

### 4. **StorageManager** - Almacenamiento Físico

Lee/escribe bloques del disco en `espacioCompartido/`.

### 5. **APIArchivos** - Lógica de Archivos

Implementa PUT (subir), GET (descargar), DELETE.

### 6. **ServidorRPC** - Servidor TCP

Escucha conexiones entrantes y maneja mensajes RPC.

### 7. **ClienteRPC** - Cliente TCP

Envía mensajes a otros nodos.

### 8. **ServicioHeartbeat** - Sincronización

Thread que corre cada 5 segundos para detectar nodos caídos.

### 9. **ReplicacionMetadatos** - Sincronización de Metadatos

Sincroniza tabla_nodos y tabla_bloques entre nodos.

---

## 🔄 Flujos Principales

### Subir Archivo (5 MB)

1. Usuario selecciona archivo
2. Particionar en bloques (5 MB ÷ 1 MB = 5 bloques)
3. Asignar bloques libres en tabla_bloques
4. Guardar localmente en espacioCompartido/
5. Registrar réplicas en tabla_bloques
6. Replicar en otros nodos vía RPC
7. ✅ Archivo subido

### Descargar Archivo

1. Usuario solicita archivo
2. Buscar bloques en tabla_bloques
3. Recuperar del nodo local (si existe)
4. Si no está, pedir a nodo con réplica vía RPC
5. Juntar bloques en orden
6. ✅ Retornar archivo

### Tolerancia a Fallas

Si nodo_2 se cae:
- Bloque 10 sigue en nodo_1 ✓
- Bloque 11 sigue en nodo_3 ✓
- Archivo completamente recuperable ✓

---

**Versión**: 1.0  
**Actualizado**: 2025-01-02  
**Estado**: ✅ Implementado

