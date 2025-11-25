# 🆘 MANUAL DE SOLUCIÓN DE ERRORES - GUI SADTF

## ❌ Errores Comunes y Soluciones

---

### Error 1: "ModuleNotFoundError: No module named 'flet'"

**Mensajes que ves:**
```
ModuleNotFoundError: No module named 'flet'
```

**Solución:**

```bash
# Paso 1: Asegúrate de estar en la carpeta del proyecto
cd C:\Users\Eduar\Documents\Universidad\TAREAS\SEMESTRE_7\Sistemas_operativos_2\Proyecto_final\SADTF\SADTF

# Paso 2: Instala Flet
pip install flet

# O instala todo de nuevo:
pip install -r requirements.txt

# Paso 3: Verifica que está instalado
pip show flet
```

**Si sigue fallando:**
```bash
# Desinstala e reinstala
pip uninstall flet -y
pip install --upgrade flet
```

---

### Error 2: "The application failed to initialize"

**Causa:** Problemas con Flet en Windows

**Solución:**

```bash
# Opción 1: Usar versión estable de Flet
pip install flet==0.20.0

# Opción 2: Actualizar todo
pip install --upgrade flet PyQt5 cryptography

# Opción 3: Si usas Python 3.8
pip install --upgrade flet
python -m flet hello_world
```

---

### Error 3: "Address already in use"

**Mensajes que ves:**
```
ERROR: [Errno 48] Address already in use
```

**Causa:** El puerto ya está siendo usado

**Solución:**

```bash
# Opción 1: Cambiar puerto automáticamente
# (La nueva GUI lo hace automática)

# Opción 2: Liberar puerto (Windows)
netstat -ano | findstr :5000
taskkill /PID [número] /F

# Opción 3: Esperar 30 segundos
# A veces toma tiempo liberar el puerto
```

---

### Error 4: "La GUI no se abre"

**Síntomas:**
- Ejecutas `python gui.py` pero no pasa nada
- O aparece y desaparece en 1 segundo

**Soluciones:**

```bash
# Solución 1: Ver el error en terminal
python gui.py

# Si hay error, verás el mensaje

# Solución 2: Usar Python completo
python -m nodo_descentralizado.gui_moderna

# Solución 3: Reinstalar Flet
pip install --upgrade flet --force-reinstall

# Solución 4: Usar virtual environment limpio
deactivate
python -m venv env_new
env_new\Scripts\activate
pip install -r requirements.txt
python gui.py
```

---

### Error 5: "No se puede conectar a otros nodos"

**Síntomas:**
- GUI abre pero dice "Desconectado"
- No aparecen nodos activos

**Soluciones:**

```bash
# Solución 1: Asegurar que nodo_1 está corriendo
# En otra terminal:
python -m nodo_descentralizado.main

# Solución 2: Verificar puerto correcto
# En config/nodo_config.json
"puerto": 9001
"host": "127.0.0.1"

# Solución 3: Firewall de Windows
# Permitir Python en Firewall
# Settings → Firewall → Permitir app → Python
```

---

### Error 6: "json.decoder.JSONDecodeError"

**Causa:** Config corrompida

**Solución:**

```bash
# Solución 1: Eliminar config y recrear
del config\nodo_config.json
python setup_config.py 1 9000 50

# Solución 2: Verificar JSON válido
# Abre config\nodo_config.json
# Debe ser JSON válido (sin comillas mal)
```

---

### Error 7: "RuntimeError: Event loop is closed"

**Causa:** Problema con Flet y asyncio

**Solución:**

```bash
# Actualizar Flet
pip install --upgrade flet

# Reiniciar Python completamente
# Cierra todas las terminales de Python
# Abre nueva terminal

python gui.py
```

---

### Error 8: "PermissionError: [Errno 13] Permission denied"

**Causa:** Sin permisos para crear carpetas/archivos

**Solución:**

```bash
# Solución 1: Ejecutar como administrador
# Haz clic derecho en terminal → Ejecutar como administrador

# Solución 2: Cambiar permisos de carpeta
# Carpeta: SADTF
# Clic derecho → Propiedades → Seguridad
# Editar → Permitir control total

# Solución 3: Cambiar ubicación de espacioCompartido
# config/nodo_config.json
"espacioCompartido": "C:\\temp\\bloques"
```

---

## ✅ Checklist de Solución Rápida

Si la GUI no funciona, sigue este orden:

```
1. ¿Instalaste flet?
   pip install -r requirements.txt
   ↓
2. ¿Ejecutas desde carpeta correcta?
   cd SADTF
   ↓
3. ¿Python 3.8+?
   python --version
   ↓
4. ¿Virtual environment activado? (si lo tienes)
   env\Scripts\activate
   ↓
5. ¿Puerto libre?
   netstat -ano | findstr :5000
   ↓
6. Intenta:
   python gui.py
   ↓
7. ¿Aún falla? Reinstala todo:
   pip install --upgrade flet --force-reinstall
   python gui.py
```

---

## 🆘 Si Nada Funciona

**Plan B: Usa CLI en lugar de GUI**

```bash
# En lugar de:
python gui.py

# Usa:
python setup_config.py 1 9000 50
python -m nodo_descentralizado.main
```

---

## 📞 Información de Debug

Si necesitas reporte de error:

```bash
# Ejecuta esto y copia el error:
python -c "import flet; print(flet.__version__)"
python --version
```

**Envía:**
- ✅ Error completo (copiar todo)
- ✅ Sistema operativo (Windows)
- ✅ Versión Python
- ✅ Qué hiciste antes del error

---

## 💡 Tips Útiles

### Limpiar Cache de Flet
```bash
pip cache purge
pip install -r requirements.txt
```

### Usar Proxy (si está en red corporativa)
```bash
pip install -r requirements.txt --proxy [user:passwd@]proxy.server:port
```

### Instalar Versión Específica
```bash
pip install flet==0.20.0
```

### Ver logs de Flet
```bash
set FLET_DEBUG=1
python gui.py
```

---

**Manual de Errores v1.0**  
**Última actualización:** 25 de noviembre de 2025
