"""
GUI SIMPLIFICADA - SADTF
Interfaz gráfica muy sencilla: un botón para conectar y ya
"""

import flet as ft
import os
import json
import threading
from pathlib import Path
from .auto_config import AutoConfig
from .utils_logger import LoggerSADTF

logger = LoggerSADTF("gui_simple")


class SADTFSimpleGUI:
    """GUI súper sencilla con un botón para conectar"""

    def __init__(self):
        self.page = None
        self.conectado = False
        self.config = None
        self.auto_config = AutoConfig()

    def main(self, page: ft.Page):
        """Interfaz principal"""
        self.page = page
        page.title = "🎨 SADTF - Almacenamiento Distribuido"
        page.window.width = 600
        page.window.height = 700
        page.theme_mode = ft.ThemeMode.LIGHT

        # Cargar config automática
        self.config = self.auto_config.cargar_o_crear()
        self.auto_config.mostrar_info()

        # Construir UI
        self._construir_ui()
        page.update()

    def _construir_ui(self):
        """Construir interfaz"""
        self.page.clean()

        # Información del nodo
        info_nodo = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.CLOUD_DONE, size=80, color="#1e88e5"),
                    ft.Text(
                        "SADTF",
                        size=40,
                        weight="bold",
                        color="#1e88e5",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Sistema de Almacenamiento Distribuido",
                        size=14,
                        color="#666",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=30,
        )

        # Tarjeta de información
        tarjeta_info = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.COMPUTER, size=20, color="#1e88e5"),
                            ft.Text("Tu Nodo:", weight="bold", size=14),
                        ],
                        spacing=10,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text("ID:", size=12, color="#666", width=80),
                                        ft.Text(
                                            self.config.get("nodo_id", "?"),
                                            size=12,
                                            weight="bold",
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.Text("IP:", size=12, color="#666", width=80),
                                        ft.Text(
                                            self.config.get("host", "?"),
                                            size=12,
                                            weight="bold",
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.Text("Puerto:", size=12, color="#666", width=80),
                                        ft.Text(
                                            str(self.config.get("puerto", "?")),
                                            size=12,
                                            weight="bold",
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.Text("Espacio:", size=12, color="#666", width=80),
                                        ft.Text(
                                            f"{self.config.get('capacidad_mb', 100)} MB",
                                            size=12,
                                            weight="bold",
                                        ),
                                    ]
                                ),
                            ],
                            spacing=8,
                        ),
                        padding=15,
                        bgcolor="#f5f5f5",
                        border_radius=8,
                    ),
                ],
                spacing=12,
            ),
            padding=20,
            bgcolor="#ffffff",
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=10,
        )

        # Botón de conexión
        boton_conectar = ft.ElevatedButton(
            "🚀 CONECTAR AL CLUSTER",
            width=300,
            height=60,
            bgcolor="#4caf50",
            color="white",
            on_click=self._conectar_cluster,
        )

        estado_conexion = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CIRCLE, size=16, color="#999"),
                            ft.Text(
                                "Desconectado",
                                size=14,
                                color="#999",
                                weight="bold",
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Text(
                        "Haz clic en 'CONECTAR' para unirte al cluster",
                        size=12,
                        color="#999",
                    ),
                ],
                spacing=5,
            ),
            padding=15,
            bgcolor="#fff3cd",
            border_radius=8,
        )

        self.estado_text = estado_conexion.content.controls[0].controls[1]
        self.estado_icon = estado_conexion.content.controls[0].controls[0]
        self.estado_container = estado_conexion

        # Tabs para mostrar cuando está conectado
        tabs_conectado = ft.Tabs(
            selected_index=0,
            visible=False,
            tabs=[
                ft.Tab(
                    text="📁 Mis Archivos",
                    content=self._tab_archivos(),
                ),
                ft.Tab(
                    text="⬆️ Subir",
                    content=self._tab_subir(),
                ),
                ft.Tab(
                    text="⬇️ Descargar",
                    content=self._tab_descargar(),
                ),
                ft.Tab(
                    text="📊 Estado",
                    content=self._tab_estado(),
                ),
            ],
        )

        self.tabs_conectado = tabs_conectado

        # Contenedor principal
        contenedor_principal = ft.Column(
            [
                info_nodo,
                tarjeta_info,
                ft.Divider(height=20),
                ft.Center(boton_conectar),
                self.estado_container,
                ft.Divider(height=20),
                tabs_conectado,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
        )

        # Agregar a página
        self.page.add(
            ft.Container(
                contenedor_principal,
                padding=20,
                expand=True,
            )
        )

    def _conectar_cluster(self, e):
        """Conectar al cluster"""
        def conectar_thread():
            try:
                # Simular conexión
                self.estado_icon.name = ft.Icons.CIRCLE
                self.estado_icon.color = "#ffc107"
                self.estado_text.value = "Conectando..."
                self.estado_text.color = "#ffc107"
                self.page.update()

                # Aquí iría la lógica real de conexión
                import time
                time.sleep(2)

                # Conexión exitosa
                self.estado_icon.name = ft.Icons.CIRCLE
                self.estado_icon.color = "#4caf50"
                self.estado_text.value = "🟢 Conectado al Cluster"
                self.estado_text.color = "#4caf50"
                self.estado_container.bgcolor = "#e8f5e9"

                self.tabs_conectado.visible = True
                self.conectado = True

                self._mostrar_snackbar(
                    f"✅ Conectado como {self.config.get('nodo_id')}",
                    "success",
                )

                self.page.update()

            except Exception as ex:
                self.estado_icon.color = "#f44336"
                self.estado_text.value = f"❌ Error: {str(ex)}"
                self.estado_text.color = "#f44336"
                self.estado_container.bgcolor = "#ffebee"
                self._mostrar_snackbar(f"Error: {str(ex)}", "error")
                self.page.update()

        # Ejecutar en thread para no bloquear UI
        thread = threading.Thread(target=conectar_thread, daemon=True)
        thread.start()

    def _tab_archivos(self):
        """Pestaña: Mis Archivos"""
        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Archivo", weight="bold")),
                ft.DataColumn(ft.Text("Tamaño", weight="bold")),
                ft.DataColumn(ft.Text("Acciones", weight="bold")),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("documento.pdf")),
                    ft.DataCell(ft.Text("5 MB")),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.DOWNLOAD, icon_size=16),
                        ft.IconButton(ft.Icons.DELETE, icon_size=16),
                    ], spacing=5)),
                ]),
            ],
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Archivos almacenados en el cluster", weight="bold"),
                    tabla,
                    ft.ElevatedButton("🔄 Actualizar"),
                ],
                spacing=15,
            ),
            padding=20,
        )

    def _tab_subir(self):
        """Pestaña: Subir Archivo"""
        def on_file_pick(e):
            if e.files:
                filename.value = e.files[0].path
                self.page.update()

        file_picker = ft.FilePicker(on_result=on_file_pick)
        self.page.overlay.append(file_picker)

        filename = ft.Text("No se seleccionó archivo", color="#999")

        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.UPLOAD_FILE, size=60, color="#1e88e5"),
                    ft.Text("Selecciona un archivo para subir", weight="bold"),
                    filename,
                    ft.ElevatedButton(
                        "📂 Seleccionar Archivo",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=lambda e: file_picker.pick_files(),
                    ),
                    ft.ElevatedButton(
                        "⬆️ Subir",
                        bgcolor="#4caf50",
                        color="white",
                        icon=ft.Icons.UPLOAD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=20,
        )

    def _tab_descargar(self):
        """Pestaña: Descargar"""
        dropdown = ft.Dropdown(
            label="Selecciona archivo",
            width=400,
            options=[
                ft.dropdown.Option("documento.pdf"),
                ft.dropdown.Option("imagen.jpg"),
            ],
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Descargar archivo del cluster", weight="bold"),
                    dropdown,
                    ft.ElevatedButton(
                        "⬇️ Descargar",
                        bgcolor="#2196f3",
                        color="white",
                        icon=ft.Icons.DOWNLOAD,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
        )

    def _tab_estado(self):
        """Pestaña: Estado del Cluster"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Estado del Cluster", weight="bold"),
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Nodos Activos", size=12, color="#666"),
                                        ft.Text("3", size=28, weight="bold", color="#4caf50"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                expand=True,
                                padding=15,
                                bgcolor="#f5f5f5",
                                border_radius=8,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Espacio Usado", size=12, color="#666"),
                                        ft.Text("45 MB", size=28, weight="bold", color="#ff9800"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                expand=True,
                                padding=15,
                                bgcolor="#f5f5f5",
                                border_radius=8,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Espacio Libre", size=12, color="#666"),
                                        ft.Text("175 MB", size=28, weight="bold", color="#4caf50"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                expand=True,
                                padding=15,
                                bgcolor="#f5f5f5",
                                border_radius=8,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
        )

    def _mostrar_snackbar(self, mensaje, tipo="info"):
        """Mostrar notificación"""
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
    """Ejecutar GUI"""
    gui = SADTFSimpleGUI()
    ft.app(target=gui.main)


if __name__ == "__main__":
    main()
