from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox
from PyQt6.QtCore import QThread, pyqtSignal
import sys
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.downloader import download_video


class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)
    
    def __init__(self, url, audio_only):
        super().__init__()
        self.url = url
        self.audio_only = audio_only
    
    def run(self):
        try:
            downloads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "downloads"))
            os.makedirs(downloads_path, exist_ok=True)
            download_video(self.url, output_folder=downloads_path, audio_only=self.audio_only)
            self.progress_signal.emit("Descarga completada.\n")
        except Exception as e:
            self.progress_signal.emit(f"Error: {e}\n")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Descargador de Videos")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.url_label = QLabel("URL del video:")
        self.url_input = QLineEdit()
        
        self.audio_checkbox = QCheckBox("Descargar solo audio")
        
        self.download_button = QPushButton("Descargar")
        self.download_button.clicked.connect(self.start_download)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.audio_checkbox)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_area)
        
        self.setLayout(layout)

    def start_download(self):
        url = self.url_input.text().strip()
        audio_only = self.audio_checkbox.isChecked()
        
        if not url:
            self.log_area.append("Por favor, ingrese una URL.\n")
            return
        
        self.log_area.append(f"Iniciando descarga de: {url}\n")
        self.download_thread = DownloadThread(url, audio_only)
        self.download_thread.progress_signal.connect(self.log_area.append)
        self.download_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
