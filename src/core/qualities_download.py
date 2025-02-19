import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QLabel, QTextEdit
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.initUI()
    
    def initUI(self):
        # Widget principal y layout general
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # ------------------------
        # Línea 1: Campo URL y Select Box de modos
        # ------------------------
        url_layout = QHBoxLayout()
        
        # Campo de texto para ingresar la URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ingresa el URL del video")
        url_layout.addWidget(self.url_input)
        
        # Select box para elegir el modo de descarga
        self.mode_select = QComboBox()
        self.mode_select.addItems(["Listar resoluciones", "Mejor calidad", "Sólo audio"])
        url_layout.addWidget(self.mode_select)
        
        main_layout.addLayout(url_layout)
        
        # ------------------------
        # Línea 2: Botón Descargar (color verde)
        # ------------------------
        self.download_button = QPushButton("Descargar")
        self.download_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        main_layout.addWidget(self.download_button)
        
        # ------------------------
        # Sección: Miniatura, Título y Select Boxes adicionales
        # ------------------------
        section_layout = QVBoxLayout()
        
        # 1. Miniatura del video (placeholder de texto por ahora)
        self.thumbnail_label = QLabel("Miniatura del video")
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setFixedSize(320, 180)  # Tamaño sugerido para la miniatura
        self.thumbnail_label.setStyleSheet("border: 1px solid black;")
        section_layout.addWidget(self.thumbnail_label)
        
        # 2. Título del video
        self.title_label = QLabel("Título del video")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_layout.addWidget(self.title_label)
        
        # 3 y 4. Select Box para códec y otro para propiedades (Res, FPS, Size) en la misma línea
        codec_prop_layout = QHBoxLayout()
        
        self.codec_select = QComboBox()
        self.codec_select.addItems(["AVC", "VP9", "AV1"])
        codec_prop_layout.addWidget(self.codec_select)
        
        self.prop_select = QComboBox()
        self.prop_select.addItems(["Res", "FPS", "Size"])
        codec_prop_layout.addWidget(self.prop_select)
        
        section_layout.addLayout(codec_prop_layout)
        main_layout.addLayout(section_layout)
        
        # ------------------------
        # Logs: Área para mostrar los logs (se puede modificar luego)
        # ------------------------
        self.logs_text_edit = QTextEdit()
        self.logs_text_edit.setReadOnly(True)
        main_layout.addWidget(self.logs_text_edit)
        
        # Conexión de señales (por ejemplo, para el botón de descarga)
        # self.download_button.clicked.connect(self.handle_download)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())