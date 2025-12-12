# main_window\dialogs\project_tree\device_data_transfer_dialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

class DeviceDataTransferDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Device Data Transfer List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Device Data Transfer List Dialog"))
        self.resize(300, 200)
