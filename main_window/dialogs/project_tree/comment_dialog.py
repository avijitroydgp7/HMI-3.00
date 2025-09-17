"main_window/dialogs/project_tree/comment_dialog.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class CommentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Comment")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("New Comment Dialog"))
        self.resize(300, 200)
