"main_window/dialogs/project_tree/recipe_dialog.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class RecipeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Recipe List")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Recipe List Dialog"))
        self.resize(300, 200)
