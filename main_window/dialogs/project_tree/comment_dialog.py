# main_window\dialogs\project_tree\comment_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QDialogButtonBox,
    QSpinBox, QLineEdit, QTextEdit, QMessageBox, QGroupBox
)

class CommentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Comment")
        
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
