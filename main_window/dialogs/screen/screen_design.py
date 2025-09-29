"main_window/dialogs/screen/screen_design.py"
import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDialogButtonBox,
    QRadioButton, QButtonGroup, QStackedWidget, QWidget, QGroupBox,
    QPushButton, QFileDialog
)
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtCore import Qt, QEvent

# Import the refactored widgets
from ...widgets.color_selector import ColorSelector
from ...widgets.gradient_widget import GradientWidget
from ...widgets.pattern_widget import PatternWidget

class ScreenDesignDialog(QDialog):
    """
    A dialog window for creating and configuring a screen design template,
    allowing users to choose between solid colors, gradients, patterns, or images for the fill.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Screen Design Template")
        
        # Initialize properties to hold the selected fill style
        self.selected_color = QColor("#FFFFFF")
        self.selected_gradient = None
        self.selected_pattern = None
        self.selected_image = None

        main_layout = QVBoxLayout(self)
        
        # --- Radio buttons for fill style ---
        fill_group_box = QGroupBox("Fill Style")
        fill_layout = QHBoxLayout()
        self.fill_color_radio = QRadioButton("Fill Colour")
        self.gradient_color_radio = QRadioButton("Gradient Colour")
        self.fill_pattern_radio = QRadioButton("Fill Pattern")
        self.fill_image_radio = QRadioButton("Fill Image")
        
        fill_layout.addWidget(self.fill_color_radio)
        fill_layout.addWidget(self.gradient_color_radio)
        fill_layout.addWidget(self.fill_pattern_radio)
        fill_layout.addWidget(self.fill_image_radio)
        fill_group_box.setLayout(fill_layout)
        
        self.radio_button_group = QButtonGroup()
        self.radio_button_group.addButton(self.fill_color_radio, 0)
        self.radio_button_group.addButton(self.gradient_color_radio, 1)
        self.radio_button_group.addButton(self.fill_pattern_radio, 2)
        self.radio_button_group.addButton(self.fill_image_radio, 3)
        self.fill_color_radio.setChecked(True)

        # --- Stacked widget for options based on radio selection ---
        self.stack = QStackedWidget()
        self.stack.addWidget(self._create_fill_color_widget())
        self.stack.addWidget(self._create_gradient_color_widget())
        self.stack.addWidget(self._create_pattern_widget())
        self.stack.addWidget(self._create_image_widget())
        
        self.radio_button_group.idClicked.connect(self.stack.setCurrentIndex)

        # --- OK and Cancel buttons ---
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout.addWidget(fill_group_box)
        main_layout.addWidget(self.stack)
        main_layout.addWidget(buttons)

        self.resize(550, 450)

    def _create_fill_color_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.color_preview_button = QPushButton()
        self.color_preview_button.setMinimumHeight(40)
        self.set_color_preview(self.selected_color)
        self.color_preview_button.clicked.connect(self._open_color_selector_dialog)
        layout.addWidget(self.color_preview_button)
        layout.addStretch()
        return widget

    def set_color_preview(self, color):
        self.selected_color = color
        text_color = "black" if color.lightnessF() > 0.5 else "white"
        hex_code = color.name(QColor.NameFormat.HexRgb).upper()
        self.color_preview_button.setText(f"{hex_code}\nClick to change")
        self.color_preview_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.name()};
                color: {text_color};
                border: 1px solid grey;
                border-radius: 4px;
                text-align: center;
                padding: 5px;
            }}
            QPushButton:hover {{
                border: 2px solid #5B9BD5;
            }}
        """)

    def _open_color_selector_dialog(self):
        color = ColorSelector.getColor(self.selected_color, self)
        if color.isValid():
            self.set_color_preview(color)

    def _create_gradient_color_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.gradient_preview_button = QPushButton("Click to select gradient")
        self.gradient_preview_button.setMinimumHeight(40)
        self.gradient_preview_button.clicked.connect(self._open_gradient_selector_dialog)
        layout.addWidget(self.gradient_preview_button)
        layout.addStretch()
        return widget

    def _open_gradient_selector_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Gradient")
        layout = QVBoxLayout(dialog)
        gradient_widget = GradientWidget()
        layout.addWidget(gradient_widget)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec():
            preview = gradient_widget.selected_preview
            if preview:
                self.selected_gradient = {
                    "color1": preview.color1,
                    "color2": preview.color2,
                    "stops": preview.stops
                }
                self.gradient_preview_button.setText("Gradient selected")

    def _create_pattern_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.pattern_preview_button = QPushButton("Click to select pattern")
        self.pattern_preview_button.setMinimumHeight(40)
        self.pattern_preview_button.clicked.connect(self._open_pattern_selector_dialog)
        layout.addWidget(self.pattern_preview_button)
        layout.addStretch()
        return widget

    def _open_pattern_selector_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Pattern")
        layout = QVBoxLayout(dialog)
        pattern_widget = PatternWidget()
        layout.addWidget(pattern_widget)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec():
            preview = pattern_widget.selected_pattern_preview
            if preview:
                self.selected_pattern = {
                    "pattern": preview.pattern,
                    "fg_color": preview.fg_color,
                    "bg_color": preview.bg_color
                }
                self.pattern_preview_button.setText("Pattern selected")

    def _create_image_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.image_preview = QLabel("Double-click to select image")
        self.image_preview.setMinimumSize(200, 200)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setStyleSheet("border: 1px solid #ccc; border-radius: 4px; background-color: white;")
        self.image_preview.installEventFilter(self)
        
        browse_button = QPushButton("Browse Image...")
        browse_button.clicked.connect(self.open_image_dialog)
        
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(browse_button)
        hbox.addStretch()
        
        layout.addLayout(hbox)
        layout.addWidget(self.image_preview, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        return widget

    def eventFilter(self, source, event):
        if source is self.image_preview and event.type() == QEvent.Type.MouseButtonDblClick:
            self.open_image_dialog()
            return True
        return super().eventFilter(source, event)

    def open_image_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select an Image", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.svg)"
        )
        if file_name:
            self.selected_image = file_name
            pixmap = QPixmap(file_name)
            self.image_preview.setPixmap(pixmap.scaled(
                self.image_preview.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
