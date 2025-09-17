# main_window/dialogs/screen/screen_design.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class ScreenDesignDialog(QDialog):
    """
    A dialog window for creating a screen design template.
    This is currently a placeholder.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Screen Design Template")
        self.layout = QVBoxLayout(self)
        self.label = QLabel("This is the Screen Design Template Dialog.")
        self.layout.addWidget(self.label)
        
        # Add OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

        self.resize(400, 300)
