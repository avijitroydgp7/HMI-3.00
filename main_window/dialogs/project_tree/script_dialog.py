"main_window/dialogs/project_tree/script_dialog.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class ScriptDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Script List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Script List Dialog"))
        self.resize(300, 200)
