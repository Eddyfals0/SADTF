# SADTF - Sistema de Almacenamiento Distribuido Tolerante a Fallas

**Proyecto final de Sistemas Operativos II - Eddyfals0**

Un sistema descentralizado que permite almacenar y administrar archivos grandes aprovechando la capacidad en disco duro de múltiples computadoras (n ≥ 2), con tolerancia a fallas mediante replicación de bloques.

---

## ⚡ INICIO EN 2 MINUTOS

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar
python gui.py

# 3. Haz clic en [🚀 CONECTAR AL CLUSTER]
# ¡LISTO! Ya estás en el cluster
```

**Eso es todo. Auto-configurable, sin terminales, sin configuración manual.**

### ✨ Características de la GUI Simple

✅ Auto-detección de IP y puerto  
✅ Un botón para conectar  
✅ Ver archivos en tabla  
✅ Subir/descargar con botones  
✅ Monitoreo del cluster  

---

## 📚 Documentación

| Documento | Contenido |
|-----------|----------|
| **⚡ INICIO_RAPIDO.md** | **Cómo empezar en 2 minutos** ⭐ |
| **🎨 INTERFAZ_GRAFICA.md** | Guía completa de la GUI |
| **📖 MANUAL_USUARIO.md** | Manual completo con ejemplos |
| **🆘 MANUAL_ERRORES.md** | Solución de errores comunes |
| **📊 DIAGRAMA_FUNCIONAMIENTO.md** | Flujos técnicos |
| **📑 INDICE_DOCUMENTACION.md** | Índice de navegación |

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
✅ **Interfaz Gráfica**: GUI moderna con Flet  
✅ **Descentralizado**: Sin nodo maestro, todos son iguales  
✅ **Auto-configuración**: Detecta IP, puerto y nombre automáticamente  

---

## 📁 Estructura del Proyecto

```
SADTF/
├── 📄 README.md                    ← Este archivo
├── 📄 INICIO_RAPIDO.md            ← Cómo empezar (2 min)
├── 📄 INTERFAZ_GRAFICA.md         ← Guía de GUI
├── 📄 MANUAL_USUARIO.md           ← Manual completo
├── 📄 MANUAL_ERRORES.md           ← Solución de errores
├── 📄 DIAGRAMA_FUNCIONAMIENTO.md  ← Flujos técnicos
├── 📄 INDICE_DOCUMENTACION.md     ← Índice
│
├── 📄 requirements.txt             ← flet, pytest, pytest-cov
├── 📄 gui.py                       ← Ejecutor de GUI (RECOMENDADO)
├── 📄 setup_config.py              ← Generador de configs
│
├── 📁 config/
│   └── nodo_config.json            ← Auto-generado
│
├── 📁 nodo_descentralizado/        ← MÓDULOS PRINCIPALES
│   ├── gui_simple.py               ← GUI simplificada
│   ├── gui_moderna.py              ← GUI moderna (opcional)
│   ├── auto_config.py              ← Auto-configuración
│   ├── main.py                     ← CLI principal
│   ├── api_archivos.py             ← Lógica PUT/GET/DELETE
│   ├── tabla_nodos.py              ← Registro de nodos
│   ├── tabla_bloques.py            ← Mapeo de bloques
│   ├── storage_manager.py          ← Lectura/escritura disco
│   ├── servidor_rpc.py             ← Servidor RPC
│   ├── cliente_rpc.py              ← Cliente RPC
│   ├── protocolo.py                ← Formato de mensajes
│   ├── heartbeat.py                ← Sincronización
│   ├── replicacion_meta.py         ← Sincronización metadatos
│   ├── utils_logger.py             ← Logging
│   └── __init__.py
│
├── 📁 espacioCompartido/           ← Almacenamiento físico
│   └── (bloques guardados aquí)
│
├── 📁 tests/                       ← Tests unitarios (14 tests)
│   ├── test_tabla_nodos.py
│   ├── test_tabla_bloques.py
│   ├── test_storage.py
│   └── __init__.py
│
├── 📁 docs/                        ← Documentación adicional
│   ├── diseno_arquitectura.md
│   └── notas_pruebas.md
│
└── 📁 env/                         ← Virtual environment
```

---

## 🚀 Cómo Usar

### OPCIÓN 1: GUI Simple (Recomendado) ⭐

**Super fácil, sin configuración:**

```bash
python gui.py
```

- Se abre interfaz automáticamente
- Detecta tu IP y puerto
- Un botón para conectar
- ¡Listo!

### OPCIÓN 2: GUI Moderna (Más funciones)

```bash
python -m nodo_descentralizado.gui_moderna
```

### OPCIÓN 3: CLI en Terminal (Para múltiples nodos)

```bash
# Crear 3 nodos con 50 MB cada uno
python setup_config.py 3 9000 50

# Terminal 1
python -m nodo_descentralizado.main

# Terminal 2
copy config\nodo_2_config.json config\nodo_config.json
python -m nodo_descentralizado.main

# Terminal 3
copy config\nodo_3_config.json config\nodo_config.json
python -m nodo_descentralizado.main
```

---

## 📊 Características

| Característica | GUI Simple | GUI Moderna | CLI |
|---|---|---|---|
| Facilidad | ✅ Muy fácil | ✅ Fácil | ⚠️ Media |
| Auto-configuración | ✅ Sí | ⚠️ Manual | ❌ No |
| Un botón conectar | ✅ Sí | ❌ No | ❌ No |
| Ver archivos | ✅ Tabla | ✅ Tabla | ✅ Texto |
| Subir/descargar | ✅ Botones | ✅ Botones | ✅ Menú |
| Monitoreo cluster | ✅ Visual | ✅ Tablas | ✅ Texto |
| Múltiples nodos | ❌ 1 PC | ❌ 1 PC | ✅ 3+ PCs |

---

## 💡 Ejemplos

### Ejemplo 1: Una sola PC

```bash
python gui.py
```

Se configura automáticamente y puedes subir/descargar archivos.

### Ejemplo 2: Múltiples PCs (Red)

**PC 1:**
```bash
python gui.py  # Detecta 192.168.1.100:9001
```

**PC 2:**
```bash
python gui.py  # Detecta 192.168.1.101:9001
```

**PC 3:**
```bash
python gui.py  # Detecta 192.168.1.102:9001
```

Todos se conectan automáticamente. ✅

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=nodo_descentralizado
```

**Resultados:** 14 tests unitarios ✅

---

## 📈 Estadísticas del Proyecto

- **Módulos:** 13 (Python)
- **Líneas de código:** ~2000+
- **Tests:** 14 unitarios
- **Documentación:** 7 archivos (50+ KB)
- **Interfaz:** GUI + CLI
- **Características:** Auto-config, Replicación, Heartbeat, RPC

---

## 🔧 Requisitos

- Python 3.8+
- pip
- Dependencias: `pip install -r requirements.txt`

---

## 📞 Soporte

¿Problemas?

1. Lee **INICIO_RAPIDO.md** (2 minutos)
2. Consulta **MANUAL_ERRORES.md** (soluciones comunes)
3. Revisa **INTERFAZ_GRAFICA.md** (uso de GUI)

---

## 🎓 Educación

Proyecto final del curso **Sistemas Operativos II**

Conceptos aplicados:
- Sistemas distribuidos
- Comunicación RPC (Remote Procedure Call)
- Replicación de datos
- Tolerancia a fallas
- Tabla de páginas (paginación)
- Sincronización entre procesos
- Detección de nodos caídos

---

**SADTF v1.0**  
**© 2025 - Eddyfals0**  
**Proyecto Educativo**
