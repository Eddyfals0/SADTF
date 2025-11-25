#!/usr/bin/env python3
"""
Ejecutor de GUI SADTF - Versión Simple
Script principal para ejecutar la interfaz gráfica sencilla
"""

import sys
import os

# Agregar ruta del proyecto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nodo_descentralizado.gui_simple import main

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 Iniciando SADTF - GUI Simplificada")
    print("=" * 60)
    print()
    print("La aplicación se abrirá en una ventana separada...")
    print("Cierra la ventana para terminar.")
    print()

    try:
        main()
    except ImportError as e:
        print(f"❌ Error: Falta instalar 'flet'")
        print(f"   Ejecuta: pip install -r requirements.txt")
        print(f"   Detalles: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al iniciar la GUI: {str(e)}")
        sys.exit(1)
