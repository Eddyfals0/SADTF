# SADTF - Sistema de Almacenamiento Distribuido Tolerante a Fallas

**Proyecto final de Sistemas Operativos II - Eddyfals0**

Un sistema descentralizado que permite almacenar y administrar archivos grandes aprovechando la capacidad en disco duro de múltiples computadoras (n ≥ 2), con tolerancia a fallas mediante replicación de bloques.

---

## 📚 Documentación Rápida

- 📖 **README.md** ← Este archivo (visión general)
- 📊 **DIAGRAMA_FUNCIONAMIENTO.md** ← Flujos detallados con diagramas
- ⚡ **GUIA_RAPIDA.md** ← Cómo usar el sistema (3 pasos)
- 📑 **INDICE_DOCUMENTACION.md** ← Índice y navegación

---

## 🎯 ¿Qué es SADTF?

Un sistema donde **múltiples computadoras se conectan** para formar un cluster de almacenamiento distribuido:

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│ NODO 1   │    │ NODO 2   │    │ NODO 3   │
│ 50 MB    │───→│ 70 MB    │───→│ 100 MB   │
└──────────┘    └──────────┘    └──────────┘
      │              │              │
      └──────────────┼──────────────┘
              (RPC Communication)
              
Capacidad Total: 220 MB
```

### Características Principales

✅ **Tolerancia a Fallas**: Cada bloque se replica en 2 nodos  
✅ **Paginación**: Tabla de bloques (similar a tabla de páginas)  
✅ **Sincronización**: Heartbeat cada 5 segundos  
✅ **Interfaz Amigable**: CLI interactivo en cada nodo  
✅ **Descentralizado**: Sin nodo maestro, todos son iguales  

---

## 📁 Estructura del Proyecto

```
SADTF/
├── 📄 README.md                    ← Este archivo
├── 📄 DIAGRAMA_FUNCIONAMIENTO.md   ← Diagramas
├── 📄 GUIA_RAPIDA.md              ← Guía de uso
├── 📄 INDICE_DOCUMENTACION.md      ← Índice
│
├── 📄 requirements.txt              ← pytest, pytest-cov
├── 📄 setup_config.py               ← Generador de configs
│
├── 📁 config/
│   └── nodo_config.json             ← Configuración
│
├── 📁 nodo_descentralizado/         ← MÓDULOS PRINCIPALES (13 archivos)
│   ├── main.py                      ← Punto de entrada
│   ├── cli.py                       ← Interfaz de usuario
│   ├── api_archivos.py              ← Lógica PUT/GET/DELETE
│   ├── tabla_nodos.py               ← Registro de nodos
│   ├── tabla_bloques.py             ← Mapeo de bloques
│   ├── storage_manager.py           ← Lectura/escritura disco
│   ├── servidor_rpc.py              ← Servidor RPC
│   ├── cliente_rpc.py               ← Cliente RPC
│   ├── protocolo.py                 ← Formato de mensajes
│   ├── heartbeat.py                 ← Sincronización
│   ├── replicacion_meta.py          ← Sincronización metadatos
│   ├── utils_logger.py              ← Logging
│   └── __init__.py
│
├── 📁 espacioCompartido/            ← Almacenamiento físico
│   └── (bloques guardados aquí)
│
├── 📁 tests/                        ← Tests unitarios (14 tests)
│   ├── test_tabla_nodos.py          ← 6 tests
│   ├── test_tabla_bloques.py        ← 5 tests
│   ├── test_storage.py              ← 3 tests
│   └── __init__.py
│
├── 📁 docs/                         ← Documentación adicional
│   ├── diseno_arquitectura.md
│   └── notas_pruebas.md
│
└── 📁 env/                          ← Python virtual environment
    ├── pyvenv.cfg
    ├── Include/
    ├── Lib/
    └── Scripts/
```

---

## 🚀 Inicio Rápido (3 Pasos)

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Crear Configuración para 3 Nodos
```bash
python setup_config.py 3 9000 50
```
Genera:
- `config/nodo_1_config.json` (puerto 9001, 50 MB)
- `config/nodo_2_config.json` (puerto 9002, 50 MB)
- `config/nodo_3_config.json` (puerto 9003, 50 MB)

### 3. Ejecutar (3 Terminales)

**Terminal 1:**
```bash
python -m nodo_descentralizado.main
```

**Terminal 2:**
```bash
cp config/nodo_2_config.json config/nodo_config.json
python -m nodo_descentralizado.main
```

**Terminal 3:**
```bash
cp config/nodo_3_config.json config/nodo_config.json
python -m nodo_descentralizado.main
```

---

## 📊 Cómo Funciona

### Subir Archivo (5 MB)
```
Usuario → Opción 1 en CLI
    ↓
Calcular bloques: 5 MB ÷ 1 MB = 5 bloques
    ↓
Asignar en tabla_bloques: [10, 11, 12, 13, 14]
    ↓
Guardar localmente en espacioCompartido/
    ↓
Replicar en otros nodos (vía RPC)
    ↓
Registrar en tabla_bloques:
  - Bloque 10: [nodo_1, nodo_2]
  - Bloque 11: [nodo_2, nodo_3]
  - etc...
    ↓
✅ "Archivo subido: file_xyz (5 bloques)"
```

### Descargar Archivo
```
Usuario → Opción 2 en CLI
    ↓
Buscar en tabla_bloques: bloques = [10, 11, 12, 13, 14]
    ↓
Para cada bloque:
  - Intentar leer localmente
  - Si no está, obtener de réplica vía RPC
    ↓
Juntar bloques en orden
    ↓
✅ Guardar archivo_xyz.pdf (5 MB)
```

### Tolerancia a Fallas
```
Si nodo_2 se cae:
  - Bloque 10 sigue en nodo_1 ✓
  - Bloque 11 sigue en nodo_3 ✓
  - Archivo completamente recuperable ✓
```

---

## 🔧 Componentes Principales

| Módulo | Propósito | Responsabilidad |
|--------|-----------|-----------------|
| **main.py** | Punto de entrada | Inicializa NodoDescentralizado |
| **cli.py** | Interfaz usuario | 8 opciones menú interactivo |
| **api_archivos.py** | Lógica de archivos | PUT/GET/DELETE de archivos |
| **tabla_nodos.py** | Registro de nodos | Quiénes están activos |
| **tabla_bloques.py** | Mapeo de bloques | Dónde está cada bloque |
| **storage_manager.py** | Almacenamiento | Lee/escribe disco |
| **servidor_rpc.py** | Servidor RPC | Acepta peticiones |
| **cliente_rpc.py** | Cliente RPC | Comunica con otros nodos |
| **protocolo.py** | Protocolo | Formato de mensajes JSON |
| **heartbeat.py** | Sincronización | Latido periódico (5s) |
| **replicacion_meta.py** | Sincronización | Sincroniza metadatos |
| **utils_logger.py** | Logging | Imprime logs ordenados |

---

## 💡 Conceptos Clave

### Bloque
- Unidad de almacenamiento = **1 MB**
- Archivo se divide en bloques
- Cada bloque tiene ID único (0-219 para 220 MB)

### Tabla de Bloques
- Mapeo: **Bloque ID → [Nodo réplica 1, Nodo réplica 2]**
- Similar a tabla de páginas en memoria virtual
- Total de entradas = Suma de capacidades de nodos

### Réplica
- **Copia de un bloque en otro nodo**
- Default: 2 replicas por bloque
- Tolera falla de 1 nodo

### Nodo
- Una computadora del cluster
- Tiene **espacioCompartido** (50-100 MB configurable)
- Corre servidor RPC en un puerto único

### Heartbeat
- **Latido periódico cada 5 segundos**
- Detecta nodos caídos
- Timeout: 15 segundos sin respuesta

---

## 📈 Ejemplo: Cluster de 3 Nodos

```
Configuración:
  nodo_1: 127.0.0.1:9001, capacidad 50 MB
  nodo_2: 127.0.0.1:9002, capacidad 70 MB
  nodo_3: 127.0.0.1:9003, capacidad 100 MB

Capacidad Total: 220 MB
Tabla de Bloques: 220 entradas (0-219)

Subir archivo de 5 MB:
  5 MB ÷ 1 MB = 5 bloques
  
  Bloque │ Contenido      │ Ubicación
  ───────┼────────────────┼──────────────────
    10   │ archivo[0]     │ nodo_1, nodo_2
    11   │ archivo[1]     │ nodo_2, nodo_3
    12   │ archivo[2]     │ nodo_1, nodo_3
    13   │ archivo[3]     │ nodo_2, nodo_1
    14   │ archivo[4]     │ nodo_3, nodo_2

Si nodo_2 se cae:
  ✅ Bloque 10 sigue en nodo_1
  ✅ Bloque 11 sigue en nodo_3
  ✅ Bloque 13 sigue en nodo_1
  ✅ Bloque 14 sigue en nodo_3
  → ARCHIVO COMPLETO Y RECUPERABLE
```

---

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=nodo_descentralizado
```

### Tests Disponibles
- **test_tabla_nodos.py**: 6 tests para TablaNodos
- **test_tabla_bloques.py**: 5 tests para TablaBloques
- **test_storage.py**: 3 tests para StorageManager

Total: **14 tests unitarios**

---

## 📝 Operaciones en CLI

1. **Subir archivo** → Seleccionar ruta local
2. **Descargar archivo** → Ingresar ID del archivo
3. **Eliminar archivo** → Confirmar eliminación
4. **Ver información** → Detalles de archivo (bloques y replicas)
5. **Listar archivos** → Tabla de todos los archivos
6. **Ver tabla de bloques** → Estado (total, usado, libre, %)
7. **Ver nodos activos** → Tabla de nodos del cluster
8. **Salir** → Terminar programa

---

## 🔧 Configuración Personalizada

Editar `config/nodo_config.json`:

```json
{
  "nodo_id": "nodo_1",
  "host": "127.0.0.1",
  "puerto": 9001,
  "capacidad_mb": 50,
  "espacioCompartido": "./espacioCompartido",
  "nodo_bootstrap": "127.0.0.1:9001",
  "heartbeat_intervalo": 5,
  "timeout_nodo": 15
}
```

### Script Automático
```bash
# Crear N nodos con capacidad K MB en puertos 9000+
python setup_config.py <N> <puerto_base> <capacidad_mb>

# Ejemplos:
python setup_config.py 3 9000 50      # 3 nodos de 50 MB
python setup_config.py 5 9000 100     # 5 nodos de 100 MB
```

---

## ⚠️ Troubleshooting

| Problema | Solución |
|----------|----------|
| "Puerto ya en uso" | Cambiar puerto en config/nodo_config.json |
| "No hay espacio disponible" | Aumentar capacidad_mb |
| "Nodo no responde" | Verificar firewall/conectividad |
| "Archivo no encontrado" | Usar opción 5 para listar archivos |

---

## 📊 Estadísticas del Proyecto

- **Líneas de código Python**: ~2000+
- **Líneas de documentación**: ~1100+
- **Módulos**: 13
- **Tests**: 14 (unitarios)
- **Documentos**: 4 (README, DIAGRAMA, GUIA, INDICE)

---

## 🎓 Recursos Adicionales

- 📖 **README.md** - Este archivo
- 📊 **DIAGRAMA_FUNCIONAMIENTO.md** - Flujos detallados
- ⚡ **GUIA_RAPIDA.md** - Uso rápido
- 📑 **INDICE_DOCUMENTACION.md** - Índice de navegación

---

## 📌 Requisitos

- Python 3.8+
- pytest (para tests)
- pytest-cov (para cobertura)
- Socket (built-in)
- JSON (built-in)
- Threading (built-in)

---

**Autor**: Eddyfals0  
**Materia**: Sistemas Operativos II  
**Año**: 2025  
**Estado**: ✅ Completo y Funcional
