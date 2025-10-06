# main_window\dialogs\screen\template_screen.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class TemplateScreenDialog(QDialog):
    """
    A dialog window for adding a new template screen.
    This is currently a placeholder.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Template Screen")
        self.layout = QVBoxLayout(self)
        self.label = QLabel("This is the Add New Template Screen Dialog.")
        self.layout.addWidget(self.label)

        # Add OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

        self.resize(400, 300)
