# main_window\dialogs\project_tree\tag_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QDialogButtonBox,
    QSpinBox, QLineEdit, QTextEdit, QMessageBox, QGroupBox
)

class TagDialog(QDialog):
    def __init__(self, parent=None, existing_tag_numbers=None, initial_data=None):
        super().__init__(parent)
        self.setWindowTitle("Tag Properties")
        self.tag_data = {}
        self.existing_tag_numbers = existing_tag_numbers if existing_tag_numbers is not None else []
        
        main_layout = QVBoxLayout(self)

        properties_group = QGroupBox("Tag Properties")
        form_layout = QFormLayout()
        properties_group.setLayout(form_layout)

        self.number_spinbox = QSpinBox()
        self.number_spinbox.setRange(1, 64000)
        form_layout.addRow(QLabel("Tag Number:"), self.number_spinbox)

        self.name_input = QLineEdit()
        self.name_input.setMaxLength(50)
        form_layout.addRow(QLabel("Tag Name:"), self.name_input)

        self.description_input = QTextEdit()
        self.description_input.setFixedHeight(80)
        form_layout.addRow(QLabel("Description:"), self.description_input)

        main_layout.addWidget(properties_group)
        main_layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)
        
        self.resize(400, 250)

        if initial_data:
            self.load_data(initial_data)

    def load_data(self, data):
        """Loads existing data into the dialog for editing."""
        self.number_spinbox.setValue(data.get("number", 1))
        self.name_input.setText(data.get("name", ""))
        self.description_input.setPlainText(data.get("description", ""))
        self.number_spinbox.setEnabled(False)  # Number is not editable

    def accept(self):
        """
        Validates the user input and accepts the dialog if valid.
        """
        tag_number = self.number_spinbox.value()
        if self.number_spinbox.isEnabled() and tag_number in self.existing_tag_numbers:
            QMessageBox.warning(self, "Input Error", f"Tag number {tag_number} already exists.")
            return

        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Input Error", "Tag name cannot be empty.")
            return

        self.tag_data = {
            "number": tag_number,
            "name": self.name_input.text().strip(),
            "description": self.description_input.toPlainText()
        }
        super().accept()

    def get_tag_data(self):
        """
        Returns the entered tag data.
        """
        return self.tag_data

