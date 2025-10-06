# main_window\dialogs\project_tree\tag_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class TagDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Tag List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Tag List Dialog"))
        self.resize(300, 200)
