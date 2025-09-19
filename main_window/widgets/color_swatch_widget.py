"main_window/widgets/color_swatch_widget.py"
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QFrame, QDialog
)
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import pyqtSignal, QSize
from .color_selector import ColorSelector

class ColorButton(QPushButton):
    """A button that displays a color and emits a signal when clicked."""
    color_clicked = pyqtSignal(QColor)

    def __init__(self, color, parent=None):
        super().__init__(parent)
        if isinstance(color, str):
            self._color = QColor(color)
        else:
            self._color = color
        
        self.setFixedSize(24, 24)
        self.setStyleSheet(f"background-color: {self._color.name()}; border: 1px solid lightgrey;")
        self.clicked.connect(self._emit_color)

    def color(self):
        """Returns the QColor of the button."""
        return self._color

    def setColor(self, color):
        """Sets a new color for the button and updates its appearance."""
        if isinstance(color, str):
            self._color = QColor(color)
        else:
            self._color = color
        self.setStyleSheet(f"background-color: {self._color.name()}; border: 1px solid lightgrey;")

    def _emit_color(self):
        self.color_clicked.emit(self._color)

class ColorSwatchWidget(QWidget):
    """A widget that displays a grid of color swatches."""
    color_selected = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # UI Setup
        self._setup_ui()

    def _setup_ui(self):
        """Initializes the UI components of the widget."""
        # Theme Colors
        self.layout.addWidget(QLabel("Theme Colors"))
        self.layout.addLayout(self._create_theme_colors_grid())

        # Standard Colors
        self.layout.addWidget(QLabel("Standard Colors"))
        self.layout.addLayout(self._create_standard_colors_row())
        
        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)

        # Additional Buttons
        self.layout.addLayout(self._create_action_buttons())

    def _create_color_button(self, color):
        """Factory method for creating and connecting a ColorButton."""
        button = ColorButton(color)
        button.color_clicked.connect(self.color_selected)
        return button

    def _generate_shades(self, base_hex):
        """Generates a list of 5 shades for a given base color."""
        shades = []
        base_color = QColor(base_hex)
        
        for i in range(1, 6):
            if base_hex == "#FFFFFF":
                lightness = 255 - (i * 25)
                shades.append(QColor(lightness, lightness, lightness))
            elif base_hex == "#000000":
                lightness = i * 25
                shades.append(QColor(lightness, lightness, lightness))
            else:
                h, s, l, a = base_color.getHslF()
                lightness_factor = 1 - (i * 0.15)
                new_l = max(0, l * lightness_factor)
                shades.append(QColor.fromHslF(h, s, new_l, a))
        return shades

    def _create_theme_colors_grid(self):
        """Creates the grid layout for theme colors and their shades."""
        grid = QGridLayout()
        grid.setSpacing(2)
        
        base_colors = [
            "#FFFFFF", "#000000", "#E7E6E6", "#44546A",
            "#5B9BD5", "#ED7D31", "#A5A5A5", "#FFC000",
            "#4472C4", "#70AD47"
        ]

        for col, base_hex in enumerate(base_colors):
            # Add base color button
            grid.addWidget(self._create_color_button(base_hex), 0, col)
            
            # Add shades
            for row, shade_color in enumerate(self._generate_shades(base_hex), 1):
                grid.addWidget(self._create_color_button(shade_color), row, col)
        
        return grid

    def _create_standard_colors_row(self):
        """Creates the horizontal layout for standard colors."""
        layout = QHBoxLayout()
        layout.setSpacing(2)
        
        colors = [
            "#C00000", "#FF0000", "#FFC000", "#FFFF00",
            "#92D050", "#00B050", "#00B0F0", "#0070C0",
            "#002060", "#7030A0"
        ]

        for color_hex in colors:
            layout.addWidget(self._create_color_button(color_hex))
        layout.addStretch()

        return layout

    def _create_action_buttons(self):
        """Creates the layout for the 'No Fill' and 'More Colors' buttons."""
        buttons_layout = QHBoxLayout()
        no_fill_button = QPushButton("No Fill")
        no_fill_button.clicked.connect(lambda: self.color_selected.emit(QColor("transparent")))
        
        more_colors_button = QPushButton("More Colors...")
        more_colors_button.clicked.connect(self.open_color_selector)

        buttons_layout.addWidget(no_fill_button)
        buttons_layout.addWidget(more_colors_button)
        return buttons_layout

    def open_color_selector(self):
        """Opens the advanced color selector dialog."""
        color = ColorSelector.getColor(parent=self)
        if color.isValid():
            self.color_selected.emit(color)
            parent = self.parent()
            if isinstance(parent, QDialog):
                parent.accept()

