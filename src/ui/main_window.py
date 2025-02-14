from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox
import sys

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
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.audio_checkbox)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_area)
        
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())