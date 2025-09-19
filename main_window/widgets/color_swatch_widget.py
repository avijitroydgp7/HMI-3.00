"main_window/widgets/color_swatch_widget.py"
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QFrame
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

        # Theme Colors
        theme_label = QLabel("Theme Colors")
        self.layout.addWidget(theme_label)
        self.theme_colors_grid = self._create_theme_colors()
        self.layout.addLayout(self.theme_colors_grid)

        # Standard Colors
        standard_label = QLabel("Standard Colors")
        self.layout.addWidget(standard_label)
        self.standard_colors_grid = self._create_standard_colors()
        self.layout.addLayout(self.standard_colors_grid)
        
        # Separator Line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)

        # Additional Buttons
        buttons_layout = QHBoxLayout()
        self.no_fill_button = QPushButton("No Fill")
        self.no_fill_button.clicked.connect(lambda: self.color_selected.emit(QColor("transparent")))
        
        self.more_colors_button = QPushButton("More Colors...")
        self.more_colors_button.clicked.connect(self.open_color_selector)

        buttons_layout.addWidget(self.no_fill_button)
        buttons_layout.addWidget(self.more_colors_button)
        self.layout.addLayout(buttons_layout)

    def _create_theme_colors(self):
        grid = QGridLayout()
        grid.setSpacing(2)
        
        base_colors = [
            "#FFFFFF", "#000000", "#E7E6E6", "#44546A",
            "#5B9BD5", "#ED7D31", "#A5A5A5", "#FFC000",
            "#4472C4", "#70AD47"
        ]

        for col, base_hex in enumerate(base_colors):
            base_color = QColor(base_hex)
            
            # Add base color button
            button = ColorButton(base_hex)
            button.color_clicked.connect(self.color_selected)
            grid.addWidget(button, 0, col)
            
            for row in range(1, 6):
                lightness = 1 - (row * 0.15) 
                if base_hex == "#FFFFFF": # Handle white column separately
                    new_color = base_color.darker(100 + row * 10)
                else:
                    h, s, l, a = base_color.getHslF()
                    new_color = QColor.fromHslF(h, s, l * lightness)

                # Add theme color variant button
                button = ColorButton(new_color)
                button.color_clicked.connect(self.color_selected)
                grid.addWidget(button, row, col)
        
        return grid

    def _create_standard_colors(self):
        layout = QHBoxLayout()
        layout.setSpacing(2)
        
        colors = [
            "#C00000", "#FF0000", "#FFC000", "#FFFF00",
            "#92D050", "#00B050", "#00B0F0", "#0070C0",
            "#002060", "#7030A0"
        ]

        for color in colors:
            button = ColorButton(color)
            button.color_clicked.connect(self.color_selected)
            layout.addWidget(button)
        layout.addStretch()

        return layout

    def open_color_selector(self):
        color = ColorSelector.getColor(parent=self)
        if color.isValid():
            self.color_selected.emit(color)