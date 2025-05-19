import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot, QTimer
import json

class VehicleTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rastreador de Veículos")
        self.setGeometry(100, 100, 1200, 800)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.map_view = QWebEngineView()
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath("map.html")))
        self.layout.addWidget(self.map_view)

        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Cole o link do Google Maps aqui...")
        self.layout.addWidget(self.link_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome ou ID do veículo...")
        self.layout.addWidget(self.name_input)

        self.add_button = QPushButton("Adicionar Veículo")
        self.add_button.clicked.connect(self.add_vehicle)
        self.layout.addWidget(self.add_button)

        self.vehicle_list = QListWidget()
        self.layout.addWidget(self.vehicle_list)

    def extract_coords(self, url):
        match = re.search(r"q=([-\d.]+),([-\d.]+)", url)
        if match:
            return float(match.group(1)), float(match.group(2))
        return None

    @pyqtSlot()
    def add_vehicle(self):
        url = self.link_input.text()
        name = self.name_input.text() or f"Veículo {self.vehicle_list.count() + 1}"
        coords = self.extract_coords(url)
        if coords:
            lat, lng = coords
            self.map_view.page().runJavaScript(f"addVehicle('{name}', {lat}, {lng});")
            self.vehicle_list.addItem(f"{name}: {lat}, {lng}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = VehicleTracker()
    tracker.show()
    sys.exit(app.exec_())