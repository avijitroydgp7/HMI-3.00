# main_window\dialogs\project_tree\animation_dialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

class AnimationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Animation List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Animation List Dialog"))
        self.resize(300, 200)
