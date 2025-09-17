"main_window/dialogs/project_tree/project_information_dialog.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class ProjectInformationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Project Information")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Project Information Dialog"))
        self.resize(300, 200)
