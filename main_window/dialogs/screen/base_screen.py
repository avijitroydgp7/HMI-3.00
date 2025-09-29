"main_window/dialogs/screen/base_screen.py"
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class BaseScreenDialog(QDialog):
    """
    A dialog window for adding a new base screen.
    This is currently a placeholder.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Base Screen")
        self.layout = QVBoxLayout(self)
        self.label = QLabel("This is the Add New Base Screen Dialog.")
        self.layout.addWidget(self.label)

        # Add OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

        self.resize(400, 300)
