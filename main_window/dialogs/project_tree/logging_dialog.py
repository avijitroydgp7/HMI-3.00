# main_window\dialogs\project_tree\logging_dialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

class LoggingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Logging List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Logging List Dialog"))
        self.resize(300, 200)
