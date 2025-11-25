# 📖 MANUAL DE USUARIO - SADTF

**Sistema de Almacenamiento Distribuido Tolerante a Fallas**

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
4. [OPCIÓN A: Interfaz Gráfica Moderna (Recomendado)](#opción-a-interfaz-gráfica-moderna-recomendado)
5. [OPCIÓN B: Interfaz CLI (Terminal)](#opción-b-interfaz-cli-terminal)
6. [Ejemplos Prácticos](#ejemplos-prácticos)
7. [Troubleshooting](#troubleshooting)
8. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 📝 Introducción

SADTF es un sistema que permite a múltiples computadoras trabajar juntas para almacenar archivos de manera segura y eficiente. Si uno de los equipos se apaga, tus archivos siguen siendo accesibles porque están guardados en copias en otros equipos.

### Analogía Simple

Imagina que tienes 3 amigos:
- **Amigo 1**: Tiene 50 MB de espacio
- **Amigo 2**: Tiene 70 MB de espacio  
- **Amigo 3**: Tiene 100 MB de espacio

Juntos pueden guardar hasta 220 MB. Si quieres guardar un archivo de 5 MB:
- Se divide en 5 partes de 1 MB
- Cada parte se guarda en 2 amigos diferentes
- Si un amigo desaparece, los otros siguen teniendo tus archivos ✅

---

## 🔧 Requisitos Previos

### Software Necesario
- ✅ **Python 3.8 o superior**
- ✅ **pip** (gestor de paquetes de Python)
- ✅ **Windows, macOS o Linux**

### Verificar Instalación

```bash
# Verificar Python
python --version

# Verificar pip
pip --version
```

---

## 📥 Instalación

### 1️⃣ Descargar el Proyecto

```bash
# Clonar repositorio (si está en GitHub)
git clone https://github.com/tu_usuario/SADTF.git
cd SADTF
```

O simplemente descargar y extraer la carpeta `SADTF`.

### 2️⃣ Instalar Dependencias

```bash
# En la carpeta raíz del proyecto
pip install -r requirements.txt
```

Este comando instala:
- `pytest` - Para pruebas
- `pytest-cov` - Para cobertura de tests

### 3️⃣ Verificar Instalación

```bash
# Listar carpetas del proyecto
ls -la

# Debería mostrar:
# config/
# nodo_descentralizado/
# espacioCompartido/
# tests/
# docs/
# requirements.txt
# setup_config.py
# README.md
# etc.
```

---

## 🎨 OPCIÓN A: Interfaz Gráfica Moderna (RECOMENDADO)

### ⭐ ¿Por qué usar la GUI?

✅ **Fácil de usar** - No necesitas terminal  
✅ **Visual** - Ver archivos, bloques y nodos en vivo  
✅ **Intuitiva** - Drag & drop, botones claros  
✅ **Moderna** - Diseño profesional y atractivo  
✅ **Todas las funciones** - Igual que CLI pero mejor

### Paso 1: Instalar

```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar

```bash
python gui.py
```

**¡Eso es todo!** Se abre una ventana hermosa automáticamente.

### Interfaz Gráfica

```
┌──────────────────────────────────────────────┐
│ 🎨 SADTF - Almacenamiento Distribuido       │
├──────────────────────────────────────────────┤
│                                              │
│  [📁] [⬆️] [⬇️] [📊] [🔗]                   │
│  Mis Archivos | Subir | Descargar | ...     │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Tabla de tus archivos                 │  │
│  │  documento.pdf    5 MB      ⬇️ 🗑️ ℹ️  │  │
│  │  imagen.jpg      10 MB      ⬇️ 🗑️ ℹ️  │  │
│  │                                        │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  [🔄 Actualizar]  [🗑️ Limpiar]              │
│                                              │
└──────────────────────────────────────────────┘
```

### Pestañas Disponibles

| Pestaña | Función |
|---------|---------|
| **📁 Mis Archivos** | Ver todos tus archivos, descargar, eliminar |
| **⬆️ Subir Archivo** | Subir nuevo archivo (drag & drop) |
| **⬇️ Descargar** | Descargar archivo existente |
| **📊 Tabla de Bloques** | Ver uso de espacio y bloques |
| **🔗 Nodos Activos** | Monitorear nodos del cluster |

### Operaciones

#### 1️⃣ Ver Tus Archivos (📁)

```
Abre la pestaña "📁 Mis Archivos"

Verás tabla con:
  • Nombre del archivo
  • Tamaño
  • Cantidad de bloques
  • Ubicación (qué nodos tienen copias)
  • Botones: Descargar | Eliminar | Información
```

#### 2️⃣ Subir Archivo (⬆️)

```
Opción A - Botón:
  1. Haz clic en [📂 Seleccionar Archivo]
  2. Elige archivo
  3. Haz clic [⬆️ Subir]
  4. ✅ ¡Listo!

Opción B - Drag & Drop:
  1. Arrastra archivo directamente
  2. Suelta en la zona gris
  3. Haz clic [⬆️ Subir]
  4. ✅ ¡Listo!
```

#### 3️⃣ Descargar Archivo (⬇️)

```
1. Abre pestaña "⬇️ Descargar"
2. Selecciona archivo del dropdown
3. (Opcional) Cambia ubicación
4. Haz clic [⬇️ Descargar]
5. ✅ Guardado en tu PC
```

#### 4️⃣ Ver Tabla de Bloques (📊)

```
Información mostrada:
  • Total bloques: 220
  • Bloques usados: 18
  • Bloques libres: 202
  • % Usado: 8.2%
  • Mapa visual: ■■■■■□□□□□...
```

#### 5️⃣ Ver Nodos (🔗)

```
Tabla de nodos con:
  • ID de nodo (nodo_1, nodo_2, etc.)
  • Estado: 🟢 Vivo | 🟡 Lento | 🔴 Caído
  • Host y puerto
  • Espacio disponible (MB y %)
  • Último heartbeat (respuesta)
```

### ℹ️ Para Más Detalles

Lee: [`INTERFAZ_GRAFICA.md`](INTERFAZ_GRAFICA.md)

---

## 🖥️ OPCIÓN B: Interfaz CLI (Terminal)

### ⭐ ¿Cuándo usar CLI?

- Cuando prefieres terminal
- Para scripting automatizado
- Para usar simultáneamente múltiples nodos en tu PC

### Configuración

### Entender el archivo de Configuración

El archivo `config/nodo_config.json` contiene la configuración de cada nodo:

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

| Parámetro | Significado | Valor |
|-----------|-------------|-------|
| `nodo_id` | Identificador único del nodo | "nodo_1", "nodo_2", etc. |
| `host` | Dirección IP del nodo | "127.0.0.1" (local) |
| `puerto` | Puerto para comunicación | 9001, 9002, 9003, etc. |
| `capacidad_mb` | Espacio disponible en MB | 50, 70, 100, etc. |
| `espacioCompartido` | Carpeta de almacenamiento | "./espacioCompartido" |
| `nodo_bootstrap` | Primer nodo a contactar | "127.0.0.1:9001" |
| `heartbeat_intervalo` | Segundos entre latidos | 5 (recomendado) |
| `timeout_nodo` | Segundos sin respuesta para marcar como caído | 15 (recomendado) |

### 📥 Generar Configuración Automáticamente

Para crear configuración para **N nodos** con capacidad **K MB** en puertos comenzando en **9000**:

```bash
# Crear 3 nodos con 50 MB cada uno
python setup_config.py 3 9000 50

# Crear 5 nodos con 100 MB cada uno
python setup_config.py 5 9000 100
```

**Esto genera:**
- `config/nodo_1_config.json`
- `config/nodo_2_config.json`
- `config/nodo_3_config.json`

### 🚀 Ejecutar el Sistema (CLI)

Editar `config/nodo_config.json`:

```json
{
  "espacioCompartido": "C:\\Users\\Eduar\\Desktop\\bloques_nodo_1"
}
```

---

## 🚀 Ejecutar el Sistema

### Paso 1: Crear Configuración para 3 Nodos

```bash
python setup_config.py 3 9000 50
```

### Paso 2: Abrir 3 Terminales

**Terminal 1 - Nodo 1:**
```bash
cd C:\Users\Eduar\Documents\Universidad\TAREAS\SEMESTRE_7\Sistemas_operativos_2\Proyecto_final\SADTF\SADTF
python -m nodo_descentralizado.main
```

**Terminal 2 - Nodo 2:**
```bash
# Copiar config de nodo 2
copy config\nodo_2_config.json config\nodo_config.json

# Ejecutar nodo 2
python -m nodo_descentralizado.main
```

**Terminal 3 - Nodo 3:**
```bash
# Copiar config de nodo 3
copy config\nodo_3_config.json config\nodo_config.json

# Ejecutar nodo 3
python -m nodo_descentralizado.main
```

### Resultado Esperado

Cada terminal mostrará:
```
[INFO] Nodo iniciado: nodo_1
[INFO] Escuchando en 127.0.0.1:9001
[INFO] Espacio disponible: 50 MB
[INFO] Conectando con otros nodos...
[INFO] Nodos activos: 3

=== MENÚ PRINCIPAL ===
1. Subir archivo
2. Descargar archivo
3. Eliminar archivo
4. Ver información de archivo
5. Listar archivos
6. Ver tabla de bloques
7. Ver nodos activos
8. Salir

Selecciona una opción:
```

---

### 💻 Interfaz de Usuario (CLI - Terminal)

### Menú Principal

```
=== MENÚ PRINCIPAL ===
1. Subir archivo
2. Descargar archivo
3. Eliminar archivo
4. Ver información de archivo
5. Listar archivos
6. Ver tabla de bloques
7. Ver nodos activos
8. Salir

Selecciona una opción: _
```

Escribe el número (1-8) y presiona **ENTER**.

---

## 📌 Operaciones Disponibles

### 1️⃣ Subir Archivo

**Opción:** `1`

```
Selecciona una opción: 1

Ingresa la ruta del archivo:
C:\Users\Eduar\Downloads\documento.pdf

✅ Archivo subido exitosamente
   - Nombre: documento.pdf
   - Tamaño: 5 MB
   - Bloques: 5
   - Ubicación: bloques [10, 11, 12, 13, 14]
   - Replicas: Nodos [nodo_1, nodo_2], [nodo_2, nodo_3], ...
```

**¿Qué pasa?**
1. El archivo se divide en bloques de 1 MB
2. Cada bloque se guarda en la carpeta `espacioCompartido/`
3. Se crea una copia (réplica) en otro nodo
4. Se guarda información del archivo en la tabla de bloques

---

### 2️⃣ Descargar Archivo

**Opción:** `2`

```
Selecciona una opción: 2

Archivos disponibles:
[1] documento.pdf (5 MB, 5 bloques)
[2] imagen.jpg (10 MB, 10 bloques)
[3] video.mp4 (50 MB, 50 bloques)

Selecciona el archivo (número o nombre):
1

¿Dónde deseas guardar el archivo?
C:\Users\Eduar\Desktop\documento_descargado.pdf

✅ Archivo descargado exitosamente en:
   C:\Users\Eduar\Desktop\documento_descargado.pdf
```

**¿Qué pasa?**
1. Se buscan los bloques en la tabla
2. Se obtienen de este nodo (si los tiene) o de otro nodo con réplica
3. Se recomponen en orden
4. Se guarda en la ubicación solicitada

---

### 3️⃣ Eliminar Archivo

**Opción:** `3`

```
Selecciona una opción: 3

Archivos disponibles:
[1] documento.pdf (5 MB, 5 bloques)
[2] imagen.jpg (10 MB, 10 bloques)

Selecciona el archivo a eliminar:
1

¿Estás seguro de que deseas eliminar documento.pdf? (s/n):
s

✅ Archivo eliminado exitosamente
   - Se liberaron 5 bloques
   - Se eliminaron replicas en otros nodos
```

**¿Qué pasa?**
1. Se marca como libre en la tabla de bloques
2. Se elimina del almacenamiento local
3. Se notifica a otros nodos para eliminar replicas
4. Se libera espacio para nuevos archivos

---

### 4️⃣ Ver Información de Archivo

**Opción:** `4`

```
Selecciona una opción: 4

Archivos disponibles:
[1] documento.pdf
[2] imagen.jpg

Selecciona archivo:
1

╔═══════════════════════════════════════╗
║     INFORMACIÓN DEL ARCHIVO           ║
╠═══════════════════════════════════════╣
║ Nombre: documento.pdf                 ║
║ Tamaño: 5 MB                          ║
║ Bloques: 5                            ║
║ Fecha de creación: 2025-11-25         ║
╠═══════════════════════════════════════╣
║     UBICACIÓN DE BLOQUES              ║
╠═════╦════════════╦════════════════════╣
║ ID  ║ Ubicación  ║ Replicas           ║
╠═════╬════════════╬════════════════════╣
║ 10  ║ nodo_1 ✓   ║ nodo_2 ✓           ║
║ 11  ║ nodo_2 ✓   ║ nodo_3 ✓           ║
║ 12  ║ nodo_1 ✓   ║ nodo_3 ✓           ║
║ 13  ║ nodo_2 ✓   ║ nodo_1 ✓           ║
║ 14  ║ nodo_3 ✓   ║ nodo_2 ✓           ║
╚═════╩════════════╩════════════════════╝
```

---

### 5️⃣ Listar Archivos

**Opción:** `5`

```
Selecciona una opción: 5

╔════════════════════════════════════════════════════╗
║          ARCHIVOS ALMACENADOS (3)                  ║
╠════╦═════════════════╦═════════╦════════════════════╣
║ ID ║ Nombre          ║ Tamaño  ║ Bloques            ║
╠════╬═════════════════╬═════════╬════════════════════╣
║ 1  ║ documento.pdf   ║ 5 MB    ║ [10, 11, 12, 13]   ║
║ 2  ║ imagen.jpg      ║ 10 MB   ║ [20-29]            ║
║ 3  ║ video.mp4       ║ 50 MB   ║ [40-89]            ║
╚════╩═════════════════╩═════════╩════════════════════╝

Espacio usado: 65 MB / 150 MB (43%)
```

---

### 6️⃣ Ver Tabla de Bloques

**Opción:** `6`

```
Selecciona una opción: 6

╔═══════════════════════════════════════════╗
║      TABLA DE BLOQUES - nodo_1            ║
╠═══════════════════════════════════════════╣
║ Total de bloques: 50                      ║
║ Bloques usados: 18                        ║
║ Bloques libres: 32                        ║
║ Porcentaje usado: 36%                     ║
╠═══════════════════════════════════════════╣
║ Bloques libres disponibles para:          ║
║   - 32 más bloques de 1 MB                ║
║   - 0 archivos grandes (> 32 MB)          ║
╠═══════════════════════════════════════════╣
║ Mapa visual (■ usado, □ libre):           ║
║ ■■■■□□□□■■■■■□□□□□□□□□□■■□□□□■■■■■■■■■  ║
╚═══════════════════════════════════════════╝
```

---

### 7️⃣ Ver Nodos Activos

**Opción:** `7`

```
Selecciona una opción: 7

╔══════════════════════════════════════════════════════════════╗
║              NODOS ACTIVOS EN EL CLUSTER (3)                ║
╠════╦═════════╦═══════════╦════════════╦════════════════════╣
║ ID ║ Estado  ║ Espacio   ║ Conexión   ║ Último Heartbeat   ║
╠════╬═════════╬═══════════╬════════════╬════════════════════╣
║ 1  ║ 🟢 Vivo ║ 32 / 50MB ║ 127.0.0.1: ║ hace 2 segundos    ║
║    ║         ║ (64%)     ║ 9001       ║                    ║
╠════╬═════════╬═══════════╬════════════╬════════════════════╣
║ 2  ║ 🟢 Vivo ║ 54 / 70MB ║ 127.0.0.1: ║ hace 1 segundo     ║
║    ║         ║ (77%)     ║ 9002       ║                    ║
╠════╬═════════╬═══════════╬════════════╬════════════════════╣
║ 3  ║ 🟡 Lento║ 65 / 100MB║ 127.0.0.1: ║ hace 8 segundos    ║
║    ║         ║ (65%)     ║ 9003       ║ (timeout en 7s)    ║
╚════╩═════════╩═══════════╩════════════╩════════════════════╝

Capacidad total del cluster: 150 MB
Capacidad usable: 75 MB (con 2 replicas)
```

---

### 8️⃣ Salir

**Opción:** `8`

```
Selecciona una opción: 8

Desconectando del cluster...
Esperando confirmación de otros nodos...
✅ Nodo desconectado correctamente

Adiós!
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Usar GUI (La Forma Fácil)

```bash
# Paso 1: En nodo_1, seleccionar opción 1 (Subir archivo)
Ingresa la ruta del archivo:
C:\Users\Eduar\Downloads\documento.pdf
✅ Archivo subido exitosamente

# Paso 2: En nodo_2, seleccionar opción 2 (Descargar archivo)
Selecciona el archivo:
1
¿Dónde deseas guardar?
C:\Users\Eduar\Desktop\copia.pdf
✅ Archivo descargado exitosamente
```

### Ejemplo 2: Simular Caída de Nodo

```bash
# Paso 1: Tener 3 nodos corriendo
nodo_1 ✓
nodo_2 ✓
nodo_3 ✓

# Paso 2: Cerrar una terminal (Ctrl+C en nodo_2)
nodo_1 ✓
nodo_2 ✗ (cerrado)
nodo_3 ✓

# Paso 3: Intentar descargar en nodo_1
✅ Archivo aún descargable (obtiene bloques de nodo_3)
```

### Ejemplo 3: Ver Tolerancia a Fallas

```bash
# Opción 4: Ver información de archivo
Bloque 10: nodo_1 ✓, nodo_2 ✓
Bloque 11: nodo_2 ✓, nodo_3 ✓
Bloque 12: nodo_1 ✓, nodo_3 ✓

# Si cae nodo_2:
Bloque 10: nodo_1 ✓, nodo_2 ✗ → ACCESIBLE
Bloque 11: nodo_2 ✗, nodo_3 ✓ → ACCESIBLE
Bloque 12: nodo_1 ✓, nodo_3 ✓ → ACCESIBLE
```

---

## 🆘 Troubleshooting

### Problema: "Puerto ya en uso"

```
ERROR: [Errno 48] Address already in use
```

**Solución:**
```bash
# Opción 1: Cambiar puerto en config
# Editar config/nodo_config.json
"puerto": 9004  # Cambiar a otro puerto

# Opción 2: Matar proceso en puerto
# Windows
netstat -ano | findstr :9001
taskkill /PID 1234 /F

# Linux/macOS
lsof -ti:9001 | xargs kill -9
```

---

### Problema: "No hay espacio disponible"

```
ERROR: No hay bloques libres disponibles
```

**Solución:**
```bash
# Opción 1: Aumentar capacidad
"capacidad_mb": 100  # Cambiar a 100 en lugar de 50

# Opción 2: Eliminar archivos
# Usar opción 3 del menú para eliminar archivos

# Opción 3: Agregar más nodos
python setup_config.py 5 9000 50  # Crear 5 nodos
```

---

### Problema: "Nodo no responde"

```
WARNING: nodo_2 no responde
Reintentando en 5 segundos...
```

**Solución:**
```bash
# Verificar conectividad
ping 127.0.0.1

# Reiniciar el nodo
# 1. Cerrar terminal (Ctrl+C)
# 2. Volver a ejecutar: python -m nodo_descentralizado.main
```

---

### Problema: "Archivo no encontrado"

```
ERROR: El archivo especificado no existe
```

**Solución:**
```bash
# Verificar ruta
# Usar opción 5 para listar archivos disponibles
# Comprobar que el archivo fue subido correctamente
```

---

### Problema: "Error al replicar"

```
WARNING: Error al replicar bloque 10 en nodo_2
```

**Solución:**
```bash
# Verificar que todos los nodos están corriendo
# Opción 7: Ver nodos activos

# Reiniciar el nodo problemático
# El sistema reintentará automáticamente
```

---

## ❓ Preguntas Frecuentes

### P: ¿Cuántos nodos necesito como mínimo?

**R:** Mínimo 2 nodos. Con 1 nodo no hay replicación y no habría tolerancia a fallas.

---

### P: ¿Puedo agregar más nodos después de iniciar?

**R:** Sí, genera nuevas configuraciones con `setup_config.py` y ejecuta nuevos nodos. El sistema los detectará automáticamente.

---

### P: ¿Qué pasa si se apaga mi computadora?

**R:** Los bloques almacenados en esa computadora se pierden, pero como existen replicas en otros nodos, los archivos siguen siendo recuperables (parcialmente si es un nodo crítico).

---

### P: ¿Puedo usar archivos más grandes de 100 MB?

**R:** Sí, puedes aumentar la capacidad de los nodos en la configuración o agregar más nodos.

---

### P: ¿Los archivos se comprimen?

**R:** No, se guardan como están. Si un archivo pesa 5 MB, ocupa 5 MB (dividido en 5 bloques de 1 MB).

---

### P: ¿Puedo cambiar el tamaño de bloque?

**R:** Actualmente es de 1 MB. Para cambiar, modifica `protocolo.py`:
```python
TAMAÑO_BLOQUE = 1024 * 1024  # 1 MB
```

---

### P: ¿Qué pasa con los metadatos si un nodo cae?

**R:** Se sincronizan automáticamente. Cuando el nodo vuelve, se actualiza con los metadatos de otros nodos.

---

### P: ¿Es seguro? ¿Se encriptan los archivos?

**R:** En esta versión básica, no hay encriptación. Es un prototipo educativo. Para producción, implementa SSL/TLS.

---

### P: ¿Puedo correr todo en una sola computadora?

**R:** Sí, como en los ejemplos anteriores. Los 3 nodos en una PC simulan 3 computadoras diferentes.

---

### P: ¿Cómo hago backup de los archivos?

**R:** Los archivos están distribuidos en la carpeta `espacioCompartido/` de cada nodo. Haz backup de esas carpetas.

---

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs en la terminal
2. Consulta [DIAGRAMA_FUNCIONAMIENTO.md](DIAGRAMA_FUNCIONAMIENTO.md)
3. Lee [README.md](README.md)
4. Revisa esta guía nuevamente

---

**Manual de Usuario v1.0**  
**Actualizado:** 25 de noviembre de 2025  
**Proyecto:** SADTF - Sistema de Almacenamiento Distribuido Tolerante a Fallas
