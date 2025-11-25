# 🎨 GUÍA DE INTERFAZ GRÁFICA - SADTF

**Interfaz Moderna con Flet - Manual Completo**

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Inicio Rápido](#inicio-rápido)
4. [Características Principales](#características-principales)
5. [Interfaz Usuario](#interfaz-usuario)
6. [Operaciones](#operaciones-disponibles)
7. [Ejemplos Prácticos](#ejemplos-prácticos)
8. [Ventajas de la GUI](#ventajas-de-la-gui)

---

## 🎯 Introducción

La **Interfaz Gráfica Moderna (GUI)** es la forma más sencilla y visual de interactuar con SADTF. Es ideal para:

- ✅ **Principiantes** - No necesitas terminal ni comandos
- ✅ **Uso Visual** - Ver archivos, bloques y nodos en tiempo real
- ✅ **Arrastrar & Soltar** - Drag & drop para subir archivos
- ✅ **Intuitiva** - Diseño moderno y fácil de entender
- ✅ **Todas las Operaciones** - Todo lo que puedes hacer en CLI, ahora en la GUI

---

## 💾 Instalación

### Requisitos
- Python 3.8+
- pip

### Paso 1: Instalar Dependencias

```bash
# En la carpeta raíz de SADTF
pip install -r requirements.txt
```

Esto instala:
- `flet>=0.20.0` - Framework para la GUI moderna
- `pytest>=7.0.0` - Testing
- `pytest-cov>=4.0.0` - Cobertura de tests

### Verificar Instalación

```bash
# Comprobar que Flet está instalado
pip show flet
```

---

## 🚀 Inicio Rápido

### Opción 1: Ejecutar GUI (Más Simple)

```bash
python gui.py
```

**Eso es todo.** Se abrirá una ventana moderna automáticamente.

### Opción 2: Ejecutar desde Python

```bash
python -m nodo_descentralizado.gui_moderna
```

### Resultado

Se abre una ventana hermosa con:

```
┌─────────────────────────────────────────────────┐
│ 🎨 SADTF - Sistema de Almacenamiento Distribuido │
│                                                 │
│  [ 📁 Mis Archivos ][ ⬆️ Subir ][ ⬇️ Descargar] │
│  [ 📊 Tabla de Bloques ][ 🔗 Nodos Activos ]    │
│                                                 │
│  Tus archivos aparecen aquí...                  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Características Principales

### 1. ✨ Diseño Moderno
- Colores profesionales (azul, verde, naranja)
- Iconos intuitivos
- Interfaz limpia y organizada

### 2. 📑 Múltiples Pestañas
- 📁 Mis Archivos
- ⬆️ Subir Archivo
- ⬇️ Descargar
- 📊 Tabla de Bloques
- 🔗 Nodos Activos

### 3. ⚡ Interactividad
- Tablas con datos actualizables
- Botones contextuales
- Notificaciones en tiempo real

### 4. 🔄 Actualizaciones en Vivo
- Monitoreo de nodos
- Estado de bloques
- Información de archivos

---

## 💻 Interfaz Usuario

### Estructura de la Ventana

```
┌─────────────────────────────────────────────────────────┐
│ [Icon] SADTF  Sistema de Almacenamiento...  Estado: 🟢  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [📁] [⬆️] [⬇️] [📊] [🔗]                        │   │
│  │ Mis Archivos | Subir Archivo | Descargar | ... │   │
│  │                                                 │   │
│  │  Contenido de la pestaña seleccionada...       │   │
│  │                                                 │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ © 2025 SADTF | v1.0 | Estado: 🟢 Conectado            │
└─────────────────────────────────────────────────────────┘
```

### Componentes Principales

| Elemento | Función |
|----------|---------|
| **Header** | Título, estado de conexión |
| **Tabs/Pestañas** | Acceso a diferentes secciones |
| **Content Area** | Contenido principal (tablas, formularios) |
| **Buttons** | Acciones (guardar, actualizar, etc.) |
| **Status Bar** | Información y versión |

---

## 📌 Operaciones Disponibles

### Pestaña 1: 📁 Mis Archivos

**Vista de tabla de todos tus archivos almacenados:**

```
┌────────────────────────────────────────────────────────┐
│                   Archivos Almacenados                 │
├──────────┬──────────┬──────────┬──────────┬────────────┤
│ Nombre   │ Tamaño   │ Bloques  │ Ubicación│ Acciones   │
├──────────┼──────────┼──────────┼──────────┼────────────┤
│ doc.pdf  │ 5 MB     │ 5        │ nodo_1,2 │ ⬇️ 🗑️ ℹ️   │
│ img.jpg  │ 10 MB    │ 10       │ nodo_2,3 │ ⬇️ 🗑️ ℹ️   │
│ vid.mp4  │ 3 MB     │ 3        │ nodo_1,3 │ ⬇️ 🗑️ ℹ️   │
└──────────┴──────────┴──────────┴──────────┴────────────┘

[🔄 Actualizar]  [🗑️ Limpiar Todo]
```

**Acciones disponibles:**
- **⬇️ Descargar** - Guardar archivo en tu PC
- **🗑️ Eliminar** - Eliminar archivo del cluster
- **ℹ️ Información** - Ver detalles del archivo
- **🔄 Actualizar** - Recargar lista de archivos

---

### Pestaña 2: ⬆️ Subir Archivo

**Interfaz intuitiva para subir archivos:**

```
┌─────────────────────────────────────┐
│        Subir Archivo                │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐   │
│  │  📤 Arrastra aquí o selecciona│   │
│  │        un archivo             │   │
│  │                               │   │
│  │  ruta/documento.pdf           │   │
│  └──────────────────────────────┘   │
│                                     │
│  [📂 Seleccionar]  [⬆️ Subir]       │
│                                     │
└─────────────────────────────────────┘

Esperando archivo...
```

**Características:**
- 📤 **Drag & Drop** - Arrastra archivos directamente
- 📂 **Selector** - Botón para explorar archivos
- 🟢 **Visual Feedback** - Vees la ruta del archivo
- ⚡ **Rápido** - Sube directamente sin confirmaciones extras

**Paso a Paso:**

1. Haz clic en **[📂 Seleccionar Archivo]**
2. Elige el archivo que quieras subir
3. Haz clic en **[⬆️ Subir]**
4. ¡Listo! Recibirás una notificación ✅

---

### Pestaña 3: ⬇️ Descargar

**Descarga archivos fácilmente:**

```
┌─────────────────────────────────────┐
│       Descargar Archivo             │
├─────────────────────────────────────┤
│                                     │
│ Archivo a descargar:                │
│ [▼ Selecciona un archivo]           │
│   • documento.pdf                   │
│   • imagen.jpg                      │
│   • video.mp4                       │
│                                     │
│ Ubicación de descarga:              │
│ 📁 Desktop                          │
│ [Cambiar]                           │
│                                     │
│ [🔄 Actualizar]  [⬇️ Descargar]    │
│                                     │
└─────────────────────────────────────┘
```

**Cómo funciona:**

1. Abre pestaña **⬇️ Descargar**
2. Selecciona archivo del dropdown
3. (Opcional) Cambia ubicación
4. Haz clic en **[⬇️ Descargar]**
5. Archivo guardado en tu PC ✅

---

### Pestaña 4: 📊 Tabla de Bloques

**Visualiza el estado del almacenamiento:**

```
┌──────────────────────────────────────────┐
│         Tabla de Bloques                 │
├──────────────────────────────────────────┤
│                                          │
│  Total Bloques: 220  │  Usados: 18      │
│  Bloques Libres: 202 │  % Usado: 8.2%   │
│                                          │
│  Mapa de Bloques:                        │
│  ■■■■■□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□  │
│                                          │
│  Leyenda:                                │
│  ■ = Usado   □ = Libre                  │
│                                          │
│  [🔄 Actualizar]                        │
│                                          │
└──────────────────────────────────────────┘
```

**Información mostrada:**
- **Total Bloques** - Capacidad total (220 = 3 nodos x ~73 MB)
- **Bloques Usados** - Actualmente ocupados
- **Bloques Libres** - Disponibles para subir
- **% Usado** - Porcentaje de uso
- **Mapa Visual** - Representación gráfica

---

### Pestaña 5: 🔗 Nodos Activos

**Monitorea todos los nodos del cluster:**

```
┌────────────────────────────────────────────────────┐
│        Nodos Activos en el Cluster (3)             │
├─────┬────────┬─────────┬────────────┬──────────────┤
│ ID  │ Estado │ Host    │ Espacio    │ Último Latido│
├─────┼────────┼─────────┼────────────┼──────────────┤
│nodo1│ 🟢 Vivo│ 127.0..1│32/50 (64%)│ hace 2s      │
│nodo2│ 🟢 Vivo│ 127.0..2│54/70 (77%)│ hace 1s      │
│nodo3│ 🟡 Lent│ 127.0..3│65/100(65%)│ hace 8s (7s)│
└─────┴────────┴─────────┴────────────┴──────────────┘

Capacidad Total: 220 MB | Usable: 110 MB (2 replicas)

[🔄 Actualizar]
```

**Indicadores:**
- 🟢 **Verde** - Nodo respondiendo normalmente
- 🟡 **Amarillo** - Nodo lento (poco tiempo antes de timeout)
- 🔴 **Rojo** - Nodo caído (sin conexión)

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Subir un Archivo

```
1. Abre GUI:    python gui.py

2. Pestaña:     ⬆️ Subir Archivo

3. Selecciona:  [📂] → Elige documento.pdf

4. Sube:        [⬆️ Subir]

5. Resultado:   ✅ Archivo subido: documento.pdf
                   5 bloques | Replicas en nodo_1, nodo_2
```

### Ejemplo 2: Descargar un Archivo

```
1. Pestaña:     ⬇️ Descargar

2. Selecciona:  documento.pdf (del dropdown)

3. Descarga:    [⬇️ Descargar]

4. Resultado:   ✅ Descargado en C:\Users\...\Desktop
```

### Ejemplo 3: Monitorear Nodos

```
1. Pestaña:     🔗 Nodos Activos

2. Observa:     
   nodo_1: 🟢 Vivo, 64% espacio
   nodo_2: 🟢 Vivo, 77% espacio
   nodo_3: 🟡 Lento, 8s sin respuesta

3. Clic:        [🔄 Actualizar] cada 5 segundos
```

---

## 🎁 Ventajas de la GUI

| Característica | CLI | GUI |
|---|---|---|
| Curva de aprendizaje | ⚠️ Media | ✅ Fácil |
| Visualización de datos | ⚠️ Texto | ✅ Tablas |
| Velocidad | ✅ Rápido | ✅ Rápido |
| Intuitiva | ⚠️ No | ✅ Sí |
| Drag & Drop | ❌ No | ✅ Sí |
| Monitoreo en vivo | ⚠️ Con comandos | ✅ Automático |
| Múltiples operaciones | ⚠️ Pasar entre nodos | ✅ Una ventana |
| Atractiva | ⚠️ Verde en negro | ✅ Moderna |

---

## 🆘 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'flet'"

```
pip install -r requirements.txt
```

### Problema: "La GUI no se abre"

```bash
# Verificar que flet está instalado
pip show flet

# Reinstalar si es necesario
pip install --upgrade flet
```

### Problema: "Archivos no aparecen en la tabla"

```bash
# Haz clic en [🔄 Actualizar]
# O espera 5 segundos para actualización automática
```

### Problema: "Nodos no aparecen activos"

```bash
# Verifica que los nodos están corriendo:
python -m nodo_descentralizado.main

# En otra terminal:
python gui.py
```

---

## 📞 Soporte

¿Problemas con la GUI?

1. Revisa que Flet está instalado: `pip show flet`
2. Verifica que los nodos están activos
3. Intenta cerrar y abrir la GUI nuevamente
4. Consulta los logs en la terminal

---

## 🔮 Próximas Mejoras (Roadmap)

- ✨ Exportar/importar configuraciones
- 📊 Gráficos de uso de espacio
- 🔐 Autenticación de usuarios
- 🌐 Modo remoto (conectar a otros clusters)
- 📱 Versión móvil con Flutter
- 🎬 Animaciones durante transferencias

---

**Guía de GUI v1.0**  
**Interfaz gráfica moderna para SADTF**  
**© 2025 - Proyecto Sistemas Operativos II**
