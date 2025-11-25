# Notas de pruebas

Anotar casos de prueba, resultados y observaciones aquí.

## Ejecutar pruebas locales

1. Activar el entorno virtual: (Windows PowerShell)

```powershell
.\env\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Ejecutar pytest para los tests de `file_utils`:

```powershell
pytest tests/test_file_utils_demo.py -q
```

Esto ejecuta dos pruebas: una que divide y reconstruye un archivo (~2.5 MB),
y otra que corrompe un bloque para demostrar que la verificación por checksum
detecta la corrupción.

## Uso CLI de `file_utils`

Dividir un archivo:

```powershell
python -m common.file_utils split ruta/al/archivo destino/bloques
```

Reconstruir a partir del manifest generado:

```powershell
python -m common.file_utils rebuild destino/bloques/nombre.manifest.json salida
```

