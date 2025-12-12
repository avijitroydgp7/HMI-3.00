# main_window\dialogs\screen\window_screen.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QDialogButtonBox,
    QSpinBox, QLineEdit, QTextEdit, QMessageBox,
    QWidget, QHBoxLayout, QGroupBox
)
from PySide6.QtCore import Qt

class WindowScreenDialog(QDialog):
    """
    A dialog window for adding or editing a new window screen with position and size properties.
    """
    def __init__(self, parent=None, existing_screen_numbers=None, initial_data=None):
        super().__init__(parent)
        self.setWindowTitle("Window Screen Properties")

        self.existing_screen_numbers = existing_screen_numbers if existing_screen_numbers is not None else []
        self.screen_data = {}

        main_layout = QVBoxLayout(self)

        screen_properties_group = QGroupBox("Screen Properties")
        screen_form_layout = QFormLayout()
        screen_properties_group.setLayout(screen_form_layout)

        self.screen_number_spinbox = QSpinBox()
        self.screen_number_spinbox.setRange(1, 64000)
        screen_form_layout.addRow("Screen Number:", self.screen_number_spinbox)

        self.screen_name_input = QLineEdit()
        self.screen_name_input.setMaxLength(50)
        screen_form_layout.addRow("Screen Name:", self.screen_name_input)
        
        self.description_input = QTextEdit()
        self.description_input.setFixedHeight(60)
        screen_form_layout.addRow("Description:", self.description_input)

        main_layout.addWidget(screen_properties_group)

        window_properties_group = QGroupBox("Window Properties")
        window_form_layout = QFormLayout()
        window_properties_group.setLayout(window_form_layout)
        
        self.x_spinbox = QSpinBox()
        self.x_spinbox.setRange(0, 8000)
        self.y_spinbox = QSpinBox()
        self.y_spinbox.setRange(0, 8000)
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 8000)
        self.width_spinbox.setValue(640)
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 8000)
        self.height_spinbox.setValue(480)

        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel("X:"))
        position_layout.addWidget(self.x_spinbox)
        position_layout.addSpacing(20)
        position_layout.addWidget(QLabel("Y:"))
        position_layout.addWidget(self.y_spinbox)
        window_form_layout.addRow("Position:", position_layout)

        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Width:"))
        size_layout.addWidget(self.width_spinbox)
        size_layout.addSpacing(20)
        size_layout.addWidget(QLabel("Height:"))
        size_layout.addWidget(self.height_spinbox)
        window_form_layout.addRow("Size:", size_layout)

        main_layout.addWidget(window_properties_group)
        main_layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)
        
        self.resize(400, 380)

        if initial_data:
            self.load_screen_data(initial_data)
        
    def load_screen_data(self, data):
        self.screen_number_spinbox.setValue(data.get("number", 1))
        self.screen_number_spinbox.setEnabled(False) # Don't allow editing number
        self.screen_name_input.setText(data.get("name", ""))
        self.description_input.setPlainText(data.get("description", ""))
        self.x_spinbox.setValue(data.get("x", 0))
        self.y_spinbox.setValue(data.get("y", 0))
        self.width_spinbox.setValue(data.get("width", 640))
        self.height_spinbox.setValue(data.get("height", 480))

    def accept(self):
        if self.screen_number_spinbox.isEnabled():
            screen_number = self.screen_number_spinbox.value()
            if screen_number in self.existing_screen_numbers:
                QMessageBox.warning(self, "Input Error", f"Screen number {screen_number} already exists.")
                return

        if not self.screen_name_input.text().strip():
            QMessageBox.warning(self, "Input Error", "Screen name cannot be empty.")
            return

        self.screen_data = {
            "number": self.screen_number_spinbox.value(),
            "name": self.screen_name_input.text().strip(),
            "description": self.description_input.toPlainText(),
            "x": self.x_spinbox.value(),
            "y": self.y_spinbox.value(),
            "width": self.width_spinbox.value(),
            "height": self.height_spinbox.value(),
            "type": "window"
        }
        super().accept()

    def get_screen_data(self):
        return self.screen_data

