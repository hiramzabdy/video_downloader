from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt6.QtCore import QThread, pyqtSignal
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.downloader import download_video_and_audio

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)
    
    def __init__(self, url, download_mode):
        super().__init__()
        self.url = url
        self.download_mode = download_mode
    
    def run(self):
        try:
            downloads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "downloads"))
            os.makedirs(downloads_path, exist_ok=True)
            
            download_video_and_audio(url=self.url, output_folder=downloads_path, download_mode=self.download_mode)
            self.progress_signal.emit("Descarga completada.\n")
        except Exception as e:
            self.progress_signal.emit(f"Error: {e}\n")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Descargador de Videos")
        self.setGeometry(100, 100, 500, 200)
        
        layout = QVBoxLayout()
        
        # Input y selector de modo en la misma línea
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ingrese la URL del video")
        
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Listar resoluciones", "Mejor calidad", "Sólo audio"])
        
        layout.addWidget(QLabel("URL del video:"))
        layout.addWidget(self.url_input)
        layout.addWidget(QLabel("Modo:"))
        layout.addWidget(self.mode_selector)
        
        # Botón Go!
        self.go_button = QPushButton("Go!")
        self.go_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.go_button.clicked.connect(self.handle_go_button)
        layout.addWidget(self.go_button)
        
        # Área de progreso de descarga
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        
        self.setLayout(layout)

    def handle_go_button(self):
        url = self.url_input.text().strip()
        mode = self.mode_selector.currentText()
        
        if not url:
            self.log_area.append("Por favor, ingrese una URL válida.\n")
            return
        
        if mode == "Listar resoluciones":
            self.download_thread = DownloadThread(url=url, download_mode="select")
            self.download_thread.progress_signal.connect(self.log_area.append)
            self.download_thread.start()
        elif mode == "Mejor calidad":
            self.download_thread = DownloadThread(url=url, download_mode="quality")
            self.download_thread.progress_signal.connect(self.log_area.append)
            self.download_thread.start()
        elif mode == "Sólo audio":
            self.download_thread = DownloadThread(url=url, download_mode="audio")
            self.download_thread.progress_signal.connect(self.log_area.append)
            self.download_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())