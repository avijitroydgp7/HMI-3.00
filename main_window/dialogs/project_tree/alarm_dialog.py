"main_window/dialogs/project_tree/alarm_dialog.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class AlarmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Alarm List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Alarm List Dialog"))
        self.resize(300, 200)
