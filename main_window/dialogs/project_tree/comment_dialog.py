# main_window\dialogs\project_tree\comment_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QDialogButtonBox,
    QSpinBox, QLineEdit, QTextEdit, QMessageBox, QGroupBox
)

class CommentDialog(QDialog):
    def __init__(self, parent=None, existing_comment_numbers=None, initial_data=None):
        super().__init__(parent)
        self.setWindowTitle("Comment Properties")
        self.comment_data = {}
        self.existing_comment_numbers = existing_comment_numbers if existing_comment_numbers is not None else []
        
        main_layout = QVBoxLayout(self)

        properties_group = QGroupBox("Comment Properties")
        form_layout = QFormLayout()
        properties_group.setLayout(form_layout)

        self.number_spinbox = QSpinBox()
        self.number_spinbox.setRange(1, 64000)
        form_layout.addRow(QLabel("Comment Number:"), self.number_spinbox)

        self.name_input = QLineEdit()
        self.name_input.setMaxLength(50)
        form_layout.addRow(QLabel("Comment Name:"), self.name_input)

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
        self.number_spinbox.setEnabled(False) # Number is not editable

    def accept(self):
        """
        Validates the user input and accepts the dialog if valid.
        """
        comment_number = self.number_spinbox.value()
        if self.number_spinbox.isEnabled() and comment_number in self.existing_comment_numbers:
            QMessageBox.warning(self, "Input Error", f"Comment number {comment_number} already exists.")
            return

        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Input Error", "Comment name cannot be empty.")
            return

        self.comment_data = {
            "number": comment_number,
            "name": self.name_input.text().strip(),
            "description": self.description_input.toPlainText()
        }
        super().accept()

    def get_comment_data(self):
        """
        Returns the entered comment data.
        """
        return self.comment_data

