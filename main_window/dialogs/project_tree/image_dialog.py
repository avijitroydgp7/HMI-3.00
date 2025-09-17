"main_window/dialogs/project_tree/image_dialog.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class ImageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Image List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Image List Dialog"))
        self.resize(300, 200)
