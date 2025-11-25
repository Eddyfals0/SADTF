"""
Interfaz Gráfica Moderna con Flet
GUI moderna y intuitiva para SADTF
"""

import flet as ft
import os
import json
import threading
from pathlib import Path
from .main import NodoDescentralizado
from .api_archivos import APIArchivos
from .tabla_bloques import TablaBloques
from .tabla_nodos import TablaNodos
from .utils_logger import LoggerSADTF

logger = LoggerSADTF("gui_moderna")


class SADTF_GUI:
    """Interfaz gráfica moderna para SADTF"""

    def __init__(self):
        self.page = None
        self.nodo = None
        self.api_archivos = None
        self.tabla_bloques = None
        self.tabla_nodos = None
        self.archivos = {}
        
    def main(self, page: ft.Page):
        """Punto de entrada de la aplicación"""
        self.page = page
        page.title = "SADTF - Sistema de Almacenamiento Distribuido"
        page.window.width = 1200
        page.window.height = 800
        page.theme_mode = ft.ThemeMode.LIGHT
        
        # Color theme
        page.bgcolor = "#f5f5f5"
        
        # Inicializar componentes
        self._inicializar_nodo()
        self._construir_ui()
        
        page.update()

    def _inicializar_nodo(self):
        """Inicializar el nodo descentralizado"""
        try:
            # Cargar configuración
            if os.path.exists("config/nodo_config.json"):
                with open("config/nodo_config.json", "r") as f:
                    config = json.load(f)
            else:
                # Crear config por defecto
                config = {
                    "nodo_id": "nodo_1",
                    "host": "127.0.0.1",
                    "puerto": 9001,
                    "capacidad_mb": 100,
                    "espacioCompartido": "./espacioCompartido",
                    "heartbeat_intervalo": 5,
                    "timeout_nodo": 15
                }
            
            # Crear directorio de almacenamiento
            os.makedirs(config.get("espacioCompartido", "./espacioCompartido"), exist_ok=True)
            
            self.tabla_nodos = TablaNodos()
            self.tabla_bloques = TablaBloques(config["capacidad_mb"])
            self.api_archivos = APIArchivos(
                self.tabla_bloques,
                config.get("espacioCompartido", "./espacioCompartido")
            )
            
            logger.log("GUI inicializada correctamente", "INFO")
        except Exception as e:
            logger.log(f"Error inicializando GUI: {str(e)}", "ERROR")

    def _construir_ui(self):
        """Construir la interfaz de usuario"""
        # Header
        header = self._crear_header()
        
        # Contenido principal con tabs
        tabs = self._crear_tabs()
        
        # Footer
        footer = self._crear_footer()
        
        # Contenedor principal
        self.page.add(
            ft.Column(
                [
                    header,
                    ft.Divider(height=1, color="#e0e0e0"),
                    tabs,
                    ft.Divider(height=1, color="#e0e0e0"),
                    footer,
                ],
                expand=True,
                spacing=0,
            )
        )

    def _crear_header(self):
        """Crear header de la aplicación"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.CLOUD_DONE, size=40, color="#1e88e5"),
                    ft.Column(
                        [
                            ft.Text(
                                "SADTF",
                                size=28,
                                weight="bold",
                                color="#1e88e5"
                            ),
                            ft.Text(
                                "Sistema de Almacenamiento Distribuido Tolerante a Fallas",
                                size=12,
                                color="#666"
                            ),
                        ],
                        spacing=0,
                    ),
                    ft.Spacer(),
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text("Estado: ", size=11, color="#666"),
                                ft.Text("🟢 CONECTADO", size=11, weight="bold", color="#4caf50"),
                            ],
                            spacing=2,
                        ),
                        padding=10,
                        bgcolor="#e8f5e9",
                        border_radius=8,
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor="#ffffff",
        )

    def _crear_tabs(self):
        """Crear tabs principales"""
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="📁 Mis Archivos",
                    content=self._tab_mis_archivos(),
                ),
                ft.Tab(
                    text="⬆️ Subir Archivo",
                    content=self._tab_subir(),
                ),
                ft.Tab(
                    text="⬇️ Descargar",
                    content=self._tab_descargar(),
                ),
                ft.Tab(
                    text="📊 Tabla de Bloques",
                    content=self._tab_tabla_bloques(),
                ),
                ft.Tab(
                    text="🔗 Nodos Activos",
                    content=self._tab_nodos(),
                ),
            ],
            expand=True,
        )
        return tabs

    def _tab_mis_archivos(self):
        """Tab: Listar archivos"""
        tabla_archivos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre", weight="bold")),
                ft.DataColumn(ft.Text("Tamaño", weight="bold")),
                ft.DataColumn(ft.Text("Bloques", weight="bold")),
                ft.DataColumn(ft.Text("Ubicación", weight="bold")),
                ft.DataColumn(ft.Text("Acciones", weight="bold")),
            ],
            rows=[],
            divider_thickness=1,
            heading_row_color="#f0f0f0",
        )
        
        # Cargar archivos
        self._actualizar_tabla_archivos(tabla_archivos)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Archivos Almacenados", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Container(
                        tabla_archivos,
                        expand=True,
                        border=ft.border.all(1, "#e0e0e0"),
                        border_radius=8,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "🔄 Actualizar",
                                on_click=lambda e: self._actualizar_tabla_archivos(tabla_archivos),
                            ),
                            ft.ElevatedButton(
                                "🗑️ Limpiar Todo",
                                bgcolor="#f44336",
                                color="white",
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=15,
                expand=True,
            ),
            padding=20,
        )

    def _tab_subir(self):
        """Tab: Subir archivo"""
        file_path = ft.Text("No se seleccionó archivo", size=12, color="#999")
        
        def on_file_selected(e):
            if e.files:
                file_path.value = e.files[0].path
                file_path.color = "#1e88e5"
                self.page.update()
        
        def on_subir(e):
            if file_path.value == "No se seleccionó archivo":
                self._mostrar_snackbar("Selecciona un archivo primero", "error")
                return
            
            try:
                ruta = file_path.value
                self.api_archivos.put_archivo(ruta)
                self._mostrar_snackbar(f"✅ Archivo subido: {os.path.basename(ruta)}", "success")
                file_path.value = "No se seleccionó archivo"
                file_path.color = "#999"
                self.page.update()
            except Exception as e:
                self._mostrar_snackbar(f"❌ Error: {str(e)}", "error")
        
        file_picker = ft.FilePicker(on_result=on_file_selected)
        self.page.overlay.append(file_picker)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Subir Archivo", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Container(
                        ft.Column(
                            [
                                ft.Icon(ft.icons.UPLOAD_FILE, size=60, color="#1e88e5"),
                                ft.Text(
                                    "Arrastra un archivo aquí o selecciona uno",
                                    size=14,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    file_path.value,
                                    size=12,
                                    color=file_path.color,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15,
                        ),
                        border=ft.border.all(2, "#e0e0e0"),
                        border_radius=10,
                        padding=40,
                        height=250,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "📂 Seleccionar Archivo",
                                icon=ft.icons.FOLDER_OPEN,
                                on_click=lambda e: file_picker.pick_files(),
                            ),
                            ft.ElevatedButton(
                                "⬆️ Subir",
                                bgcolor="#4caf50",
                                color="white",
                                icon=ft.icons.UPLOAD,
                                on_click=on_subir,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
        )

    def _tab_descargar(self):
        """Tab: Descargar archivo"""
        dropdown_archivos = ft.Dropdown(
            width=400,
            label="Selecciona un archivo",
            options=[],
        )
        
        ruta_descarga = ft.Text("Desktop", size=12, color="#666")
        
        def on_descargar(e):
            if not dropdown_archivos.value:
                self._mostrar_snackbar("Selecciona un archivo", "error")
                return
            
            try:
                # Simular descarga
                self._mostrar_snackbar(
                    f"✅ Descargado: {dropdown_archivos.value}",
                    "success"
                )
                dropdown_archivos.value = None
                self.page.update()
            except Exception as e:
                self._mostrar_snackbar(f"❌ Error: {str(e)}", "error")
        
        # Cargar archivos en dropdown
        self._actualizar_dropdown_archivos(dropdown_archivos)
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Descargar Archivo", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Text("Archivo a descargar:", weight="bold"),
                    dropdown_archivos,
                    ft.Divider(),
                    ft.Text("Ubicación de descarga:", weight="bold"),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Icon(ft.icons.FOLDER, color="#1e88e5"),
                                ruta_descarga,
                                ft.TextButton("Cambiar", icon=ft.icons.EDIT),
                            ],
                            spacing=10,
                        ),
                        padding=15,
                        bgcolor="#f5f5f5",
                        border_radius=8,
                    ),
                    ft.Spacer(),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "🔄 Actualizar Lista",
                                on_click=lambda e: self._actualizar_dropdown_archivos(dropdown_archivos),
                            ),
                            ft.ElevatedButton(
                                "⬇️ Descargar",
                                bgcolor="#2196f3",
                                color="white",
                                icon=ft.icons.DOWNLOAD,
                                on_click=on_descargar,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
        )

    def _tab_tabla_bloques(self):
        """Tab: Ver tabla de bloques"""
        info_bloques = ft.Column(
            [
                ft.Row(
                    [
                        self._crear_stat_card("Total Bloques", "220", "#1e88e5"),
                        self._crear_stat_card("Bloques Usados", "18", "#f57c00"),
                        self._crear_stat_card("Bloques Libres", "202", "#4caf50"),
                        self._crear_stat_card("% Usado", "8.2%", "#ff6f00"),
                    ],
                    spacing=10,
                ),
                ft.Divider(),
                ft.Text("Mapa de Bloques", weight="bold", size=14),
                ft.Container(
                    ft.Text(
                        "■■■■■□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□",
                        family="monospace",
                        size=12,
                    ),
                    padding=15,
                    bgcolor="#f5f5f5",
                    border_radius=8,
                ),
            ],
            spacing=15,
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Tabla de Bloques", size=18, weight="bold"),
                    ft.Divider(),
                    info_bloques,
                    ft.Spacer(),
                    ft.ElevatedButton(
                        "🔄 Actualizar",
                        icon=ft.icons.REFRESH,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
        )

    def _tab_nodos(self):
        """Tab: Ver nodos activos"""
        tabla_nodos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Nodo", weight="bold")),
                ft.DataColumn(ft.Text("Estado", weight="bold")),
                ft.DataColumn(ft.Text("Host", weight="bold")),
                ft.DataColumn(ft.Text("Espacio", weight="bold")),
                ft.DataColumn(ft.Text("Último Latido", weight="bold")),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("nodo_1")),
                    ft.DataCell(ft.Row([
                        ft.Icon(ft.icons.CIRCLE, size=12, color="#4caf50"),
                        ft.Text("Activo"),
                    ], spacing=5)),
                    ft.DataCell(ft.Text("127.0.0.1:9001")),
                    ft.DataCell(ft.Text("32/50 MB (64%)")),
                    ft.DataCell(ft.Text("hace 2s")),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("nodo_2")),
                    ft.DataCell(ft.Row([
                        ft.Icon(ft.icons.CIRCLE, size=12, color="#4caf50"),
                        ft.Text("Activo"),
                    ], spacing=5)),
                    ft.DataCell(ft.Text("127.0.0.1:9002")),
                    ft.DataCell(ft.Text("54/70 MB (77%)")),
                    ft.DataCell(ft.Text("hace 1s")),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("nodo_3")),
                    ft.DataCell(ft.Row([
                        ft.Icon(ft.icons.CIRCLE, size=12, color="#ff9800"),
                        ft.Text("Lento"),
                    ], spacing=5)),
                    ft.DataCell(ft.Text("127.0.0.1:9003")),
                    ft.DataCell(ft.Text("65/100 MB (65%)")),
                    ft.DataCell(ft.Text("hace 8s")),
                ]),
            ],
            divider_thickness=1,
            heading_row_color="#f0f0f0",
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Nodos Activos en el Cluster", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Container(
                        tabla_nodos,
                        expand=True,
                        border=ft.border.all(1, "#e0e0e0"),
                        border_radius=8,
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.icons.INFO, color="#2196f3"),
                            ft.Text(
                                "Capacidad Total: 220 MB | Usable: 110 MB (con 2 replicas)",
                                size=12,
                                color="#666",
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "🔄 Actualizar",
                                icon=ft.icons.REFRESH,
                            ),
                        ],
                    ),
                ],
                spacing=15,
            ),
            padding=20,
        )

    def _crear_stat_card(self, titulo, valor, color):
        """Crear tarjeta de estadística"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(titulo, size=12, color="#999"),
                    ft.Text(valor, size=28, weight="bold", color=color),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            expand=True,
            padding=15,
            bgcolor="#ffffff",
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=8,
        )

    def _crear_footer(self):
        """Crear footer de la aplicación"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("© 2025 SADTF - Proyecto Sistemas Operativos II", size=11, color="#999"),
                    ft.Spacer(),
                    ft.Text("v1.0 | Estado: 🟢 Conectado", size=11, color="#999"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=15,
            bgcolor="#ffffff",
        )

    def _actualizar_tabla_archivos(self, tabla):
        """Actualizar tabla de archivos"""
        # Simular carga de archivos
        archivos_simulados = [
            ("documento.pdf", "5 MB", "5", "nodo_1, nodo_2"),
            ("imagen.jpg", "10 MB", "10", "nodo_2, nodo_3"),
            ("video.mp4", "3 MB", "3", "nodo_1, nodo_3"),
        ]
        
        tabla.rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(archivo[0])),
                ft.DataCell(ft.Text(archivo[1])),
                ft.DataCell(ft.Text(archivo[2])),
                ft.DataCell(ft.Text(archivo[3])),
                ft.DataCell(ft.Row([
                    ft.IconButton(ft.icons.DOWNLOAD, icon_size=16, tooltip="Descargar"),
                    ft.IconButton(ft.icons.DELETE, icon_size=16, tooltip="Eliminar"),
                    ft.IconButton(ft.icons.INFO, icon_size=16, tooltip="Información"),
                ], spacing=5)),
            ])
            for archivo in archivos_simulados
        ]
        self.page.update()

    def _actualizar_dropdown_archivos(self, dropdown):
        """Actualizar dropdown de archivos"""
        dropdown.options = [
            ft.dropdown.Option("documento.pdf"),
            ft.dropdown.Option("imagen.jpg"),
            ft.dropdown.Option("video.mp4"),
        ]
        self.page.update()

    def _mostrar_snackbar(self, mensaje, tipo="info"):
        """Mostrar snackbar de notificación"""
        colores = {
            "success": "#4caf50",
            "error": "#f44336",
            "info": "#2196f3",
        }
        
        snackbar = ft.SnackBar(
            ft.Text(mensaje, color="white"),
            bgcolor=colores.get(tipo, "#2196f3"),
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()


def main():
    """Punto de entrada de la GUI"""
    gui = SADTF_GUI()
    ft.app(target=gui.main)


if __name__ == "__main__":
    main()
