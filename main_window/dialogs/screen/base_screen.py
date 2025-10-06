# main_window\dialogs\screen\base_screen.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QDialogButtonBox,
    QSpinBox, QLineEdit, QTextEdit, QCheckBox, QPushButton, QMessageBox,
    QWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QPainter, QPixmap

from .screen_design import ScreenDesignDialog

class BaseScreenDialog(QDialog):
    """
    A dialog window for adding a new base screen with detailed options.
    """
    def __init__(self, parent=None, existing_screen_numbers=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Base Screen")
        

        # Store data from the dialog
        self.existing_screen_numbers = existing_screen_numbers if existing_screen_numbers is not None else []
        self.screen_design_data = None
        self.screen_data = {}

        # Main layout
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)

        # --- Screen Number ---
        self.screen_number_spinbox = QSpinBox()
        self.screen_number_spinbox.setRange(1, 64000)
        self.screen_number_spinbox.setToolTip("Enter a unique screen number between 1 and 64000.")
        form_layout.addRow(QLabel("Screen Number:"), self.screen_number_spinbox)

        # --- Screen Name ---
        self.screen_name_input = QLineEdit()
        self.screen_name_input.setMaxLength(50)
        self.screen_name_input.setToolTip("Enter a descriptive name for the screen (max 50 characters).")
        form_layout.addRow(QLabel("Screen Name:"), self.screen_name_input)

        # --- Screen Dimensions ---
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(100, 8000)
        self.width_spinbox.setValue(1024)
        self.width_spinbox.setToolTip("Set the width of the screen in pixels.")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(100, 8000)
        self.height_spinbox.setValue(768)
        self.height_spinbox.setToolTip("Set the height of the screen in pixels.")
        
        dim_layout = QHBoxLayout()
        dim_layout.addWidget(QLabel("Width:"))
        dim_layout.addWidget(self.width_spinbox)
        dim_layout.addSpacing(20)
        dim_layout.addWidget(QLabel("Height:"))
        dim_layout.addWidget(self.height_spinbox)
        
        dim_widget = QWidget()
        dim_widget.setLayout(dim_layout)
        form_layout.addRow(QLabel("Screen Dimensions:"), dim_widget)

        # --- Detail Description ---
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Maximum 500 characters")
        self.description_input.textChanged.connect(self.check_description_length)
        self.description_char_count = QLabel("0/500")
        self.description_char_count.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Use a widget to contain the text edit and character count
        description_widget = QWidget()
        description_layout = QVBoxLayout(description_widget)
        description_layout.setContentsMargins(0,0,0,0)
        description_layout.setSpacing(2)
        description_layout.addWidget(self.description_input)
        description_layout.addWidget(self.description_char_count)
        form_layout.addRow(QLabel("Detail Description:"), description_widget)

        # --- Security ---
        self.security_spinbox = QSpinBox()
        self.security_spinbox.setRange(0, 255)  # Default range, can be adjusted
        self.security_spinbox.setToolTip("Set the security level for this screen (0-255).")
        form_layout.addRow(QLabel("Security:"), self.security_spinbox)
        
        # --- Individual Screen Design ---
        self.design_checkbox = QCheckBox("Individual Set Screen Design")
        self.design_checkbox.setToolTip("Enable to set a custom design for this screen.")
        
        self.design_preview_button = QPushButton("No custom design set")
        self.design_preview_button.setEnabled(False)
        self.design_preview_button.setToolTip("Click to open the Screen Design Template")
        self.design_preview_button.clicked.connect(self._open_screen_design_dialog)
        self.design_checkbox.toggled.connect(self._toggle_design_options)
        
        form_layout.addRow(self.design_checkbox, self.design_preview_button)

        main_layout.addLayout(form_layout)

        # --- Dialog Buttons ---
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)
        
        self.setFixedSize(500, 450)

    def check_description_length(self):
        """Updates the character count label for the description."""
        length = len(self.description_input.toPlainText())
        self.description_char_count.setText(f"{length}/500")
        if length > 500:
            self.description_char_count.setStyleSheet("color: red;")
        else:
            self.description_char_count.setStyleSheet("")

    def _toggle_design_options(self, checked):
        """Enables the design button and opens the editor if it's the first time."""
        self.design_preview_button.setEnabled(checked)
        if checked and self.screen_design_data is None:
            self._open_screen_design_dialog()

    def _open_screen_design_dialog(self):
        """Opens the screen design dialog and updates the preview."""
        dialog = ScreenDesignDialog(self, initial_data=self.screen_design_data)
        if dialog.exec():
            self.screen_design_data = dialog.get_design_details()
            self._update_design_preview()

    def _update_design_preview(self):
        """Updates the preview button to reflect the selected screen design."""
        if not self.screen_design_data:
            self.design_preview_button.setText("No custom design set")
            self.design_preview_button.setStyleSheet("")
            return

        style_type = self.screen_design_data.get("type")
        
        if style_type == "color":
            color_str = self.screen_design_data.get("color", "#FFFFFF")
            color = QColor(color_str)
            text_color = "black" if color.lightnessF() > 0.5 else "white"
            self.design_preview_button.setText(f"Solid Color: {color.name()}")
            self.design_preview_button.setStyleSheet(f"background-color: {color.name()}; color: {text_color};")
        elif style_type == "gradient":
            grad = self.screen_design_data.get("gradient")
            if grad:
                c1 = QColor(grad['color1'])
                c2 = QColor(grad['color2'])
                c1_hex = c1.name()
                c2_hex = c2.name()
                self.design_preview_button.setText(f"Gradient: {grad['stops']}")
                self.design_preview_button.setStyleSheet(f"background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {c1_hex}, stop:1 {c2_hex});")
        elif style_type == "pattern":
             self.design_preview_button.setText("Pattern Selected")
             self.design_preview_button.setStyleSheet("")
        elif style_type == "image":
            path = self.screen_design_data.get("image_path", "")
            filename = path.split('/')[-1]
            self.design_preview_button.setText(f"Image: {filename}")
            self.design_preview_button.setStyleSheet("")
        else:
            self.design_preview_button.setText("Custom design set")
            self.design_preview_button.setStyleSheet("")

    def accept(self):
        """
        Validates the inputs, gathers the data, and then closes the dialog.
        """
        # Validate Screen Number uniqueness
        screen_number = self.screen_number_spinbox.value()
        if screen_number in self.existing_screen_numbers:
            QMessageBox.warning(self, "Input Error", f"Screen number {screen_number} already exists. Please choose a unique number.")
            return

        # Validate Screen Name is not empty
        if not self.screen_name_input.text().strip():
            QMessageBox.warning(self, "Input Error", "Screen name cannot be empty.")
            return
            
        # Validate Description Length
        if len(self.description_input.toPlainText()) > 500:
            QMessageBox.warning(self, "Input Error", "The detail description cannot exceed 500 characters.")
            return

        # If validation passes, gather data into the instance variable
        self.screen_data = {
            "number": self.screen_number_spinbox.value(),
            "name": self.screen_name_input.text().strip(),
            "width": self.width_spinbox.value(),
            "height": self.height_spinbox.value(),
            "description": self.description_input.toPlainText(),
            "security": self.security_spinbox.value(),
            "design": self.screen_design_data if self.design_checkbox.isChecked() else None
        }
        
        # Call the parent's accept() method to close the dialog with an accepted result
        super().accept()
        
    def get_screen_data(self):
        """Returns the screen data that was gathered when the dialog was accepted."""
        return self.screen_data
