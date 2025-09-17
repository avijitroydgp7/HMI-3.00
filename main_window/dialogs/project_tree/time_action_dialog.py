"main_window/dialogs/project_tree/time_action_dialog.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class TimeActionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Time Action List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Time Action List Dialog"))
        self.resize(300, 200)
