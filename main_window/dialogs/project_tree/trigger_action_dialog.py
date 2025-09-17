"main_window/dialogs/project_tree/trigger_action_dialog.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class TriggerActionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Trigger Action List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Trigger Action List Dialog"))
        self.resize(300, 200)
