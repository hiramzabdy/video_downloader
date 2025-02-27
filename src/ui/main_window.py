from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.downloader import download_video_and_audio

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)
    download_progress = pyqtSignal(int)
    
    def __init__(self, url, download_mode):
        super().__init__()
        self.url = url
        self.download_mode = download_mode
    
    def run(self):
        try:
            downloads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "downloads"))
            os.makedirs(downloads_path, exist_ok=True)
            
            download_video_and_audio(
                url=self.url, 
                output_folder=downloads_path, 
                download_mode=self.download_mode, 
                progress_callback=lambda p: self.download_progress.emit(p)
            )
            self.progress_signal.emit("Descarga completada.\n")
        except Exception as e:
            self.progress_signal.emit(f"Error: {e}\n")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Descargador de Videos")
        self.setGeometry(100, 100, 500, 250)  # Ajustamos el tamaño
        
        layout = QVBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Ingrese la URL del video")
        
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Listar resoluciones", "Mejor calidad", "Sólo audio"])
        
        layout.addWidget(QLabel("URL del video:"))
        layout.addWidget(self.url_input)
        layout.addWidget(QLabel("Modo:"))
        layout.addWidget(self.mode_selector)
        
        self.go_button = QPushButton("Go!")
        self.go_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.go_button.clicked.connect(self.handle_go_button)
        layout.addWidget(self.go_button)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)

    def handle_go_button(self):
        url = self.url_input.text().strip()
        mode = self.mode_selector.currentText()
        
        if not url:
            self.log_area.append("Por favor, ingrese una URL válida.\n")
            return
        
        self.download_thread = DownloadThread(url=url, download_mode="quality" if mode == "Mejor calidad" else "audio" if mode == "Sólo audio" else "select")
        
        self.download_thread.progress_signal.connect(self.log_area.append)
        self.download_thread.download_progress.connect(self.progress_bar.setValue)  # Conectar progreso
        self.download_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())