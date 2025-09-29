# main_window/dialogs/screen/screen_design.py
import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDialogButtonBox,
    QRadioButton, QButtonGroup, QStackedWidget, QWidget, QGroupBox,
    QPushButton, QFileDialog, QLineEdit
)
from PyQt6.QtGui import (
    QColor, QPixmap, QIcon, QPainter, QLinearGradient, QBrush
)
from PyQt6.QtCore import Qt, QEvent, QPointF, QSize

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
        self.color_preview_button.setFixedHeight(40)
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
        self.gradient_preview_button.setFixedHeight(40)
        self.gradient_preview_button.clicked.connect(self._open_gradient_selector_dialog)
        layout.addWidget(self.gradient_preview_button)
        layout.addStretch()
        return widget

    def _open_gradient_selector_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Gradient")
        layout = QVBoxLayout(dialog)
        gradient_widget = GradientWidget(self.selected_gradient)
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
                
                color1_hex = preview.color1.name()
                color2_hex = preview.color2.name()
                
                if preview.stops == "Horizontal":
                    gradient_stops = "x1: 0, y1: 0, x2: 1, y2: 0"
                elif preview.stops == "Vertical":
                    gradient_stops = "x1: 0, y1: 0, x2: 0, y2: 1"
                elif preview.stops == "Up Diagonal":
                    gradient_stops = "x1: 0, y1: 1, x2: 1, y2: 0"
                else: # Down Diagonal
                    gradient_stops = "x1: 0, y1: 0, x2: 1, y2: 1"

                self.gradient_preview_button.setText("")
                self.gradient_preview_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: qlineargradient({gradient_stops}, stop: 0 {color1_hex}, stop: 1 {color2_hex});
                        border: 1px solid grey;
                        border-radius: 4px;
                    }}
                    QPushButton:hover {{
                        border: 2px solid #5B9BD5;
                    }}
                """)

    def _create_pattern_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.pattern_preview_button = QPushButton("Click to select pattern")
        self.pattern_preview_button.setFixedHeight(40)
        self.pattern_preview_button.clicked.connect(self._open_pattern_selector_dialog)
        layout.addWidget(self.pattern_preview_button)
        layout.addStretch()
        return widget

    def _open_pattern_selector_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Pattern")
        layout = QVBoxLayout(dialog)
        pattern_widget = PatternWidget(self.selected_pattern)
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
                
                icon_pixmap = QPixmap(150, 32)
                icon_pixmap.fill(Qt.GlobalColor.transparent)

                painter = QPainter(icon_pixmap)
                
                pattern_brush = QBrush(preview.fg_color, preview.pattern)
                
                painter.fillRect(icon_pixmap.rect(), preview.bg_color)
                painter.fillRect(icon_pixmap.rect(), pattern_brush)
                painter.end()
                
                self.pattern_preview_button.setText("")
                self.pattern_preview_button.setIcon(QIcon(icon_pixmap))
                self.pattern_preview_button.setIconSize(icon_pixmap.size())
                
                self.pattern_preview_button.setStyleSheet("""
                    QPushButton {
                        border: 1px solid grey;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        border: 2px solid #5B9BD5;
                    }
                """)

    def _create_image_widget(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Horizontal layout for the file path and browse button
        hbox = QHBoxLayout()
        
        # Label to show the file path
        self.image_path_label = QLineEdit()
        self.image_path_label.setPlaceholderText("No image selected")
        self.image_path_label.setReadOnly(True) # Make it non-editable
        
        # Browse button
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.open_image_dialog)
        
        # Add widgets to the horizontal layout
        hbox.addWidget(self.image_path_label)
        hbox.addWidget(browse_button)
        
        # Add the horizontal layout to the main vertical layout
        main_layout.addLayout(hbox)
        
        main_layout.addStretch() # Pushes the hbox to the top

        return widget

    def open_image_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select an Image", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.svg)"
        )
        if file_name:
            self.selected_image = file_name
            self.image_path_label.setText(file_name)
