"main_window/widgets/pattern_widget.py"
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QPushButton, QLabel, QFrame
)
from PyQt6.QtGui import QColor, QPainter, QBrush
from PyQt6.QtCore import pyqtSignal, Qt

from .color_selector import ColorSelector

class ColorPickerButton(QPushButton):
    """A button that displays a color and opens a color picker when clicked."""
    color_changed = pyqtSignal(QColor)

    def __init__(self, color='white', parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self.setFixedSize(120, 24)
        self._update_style()
        self.clicked.connect(self._open_color_picker)

    def color(self):
        """Returns the current QColor of the button."""
        return self._color

    def set_color(self, color):
        """Sets the button's color and emits a signal if it changes."""
        if self._color != color:
            self._color = color
            self._update_style()
            self.color_changed.emit(self._color)

    def _update_style(self):
        self.setStyleSheet(f"background-color: {self._color.name()}; border: 1px solid grey;")

    def _open_color_picker(self):
        """Opens the color selector dialog to choose a new color."""
        new_color = ColorSelector.getColor(self._color, self)
        if new_color.isValid():
            self.set_color(new_color)


class PatternPreviewWidget(QWidget):
    """A widget to display a single fill pattern."""
    def __init__(self, pattern, fg_color, bg_color, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.pattern = pattern
        self.fg_color = fg_color
        self.bg_color = bg_color

    def set_colors(self, fg_color, bg_color):
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        brush = QBrush(self.fg_color, self.pattern)
        painter.fillRect(self.rect(), self.bg_color)
        painter.fillRect(self.rect(), brush)
        painter.setPen(QColor("grey"))
        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))

class PatternWidget(QWidget):
    """A widget for selecting colors and a fill pattern."""
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        
        # Color selection
        color_group = QGroupBox("Color")
        color_layout = QGridLayout(color_group)
        self.fg_color_button = ColorPickerButton(QColor("black"))
        self.bg_color_button = ColorPickerButton(QColor("white"))
        color_layout.addWidget(QLabel("Foreground Color"), 0, 0)
        color_layout.addWidget(self.fg_color_button, 0, 1)
        color_layout.addWidget(QLabel("Background Color"), 1, 0)
        color_layout.addWidget(self.bg_color_button, 1, 1)
        main_layout.addWidget(color_group)

        # Pattern selection
        pattern_group = QGroupBox("Pattern")
        self.pattern_grid = QGridLayout(pattern_group)
        self.pattern_grid.setSpacing(5)
        self.pattern_buttons = []

        patterns = [
            Qt.BrushStyle.SolidPattern, Qt.BrushStyle.Dense1Pattern, Qt.BrushStyle.Dense2Pattern,
            Qt.BrushStyle.Dense3Pattern, Qt.BrushStyle.Dense4Pattern, Qt.BrushStyle.Dense5Pattern,
            Qt.BrushStyle.Dense6Pattern, Qt.BrushStyle.Dense7Pattern, Qt.BrushStyle.HorPattern,
            Qt.BrushStyle.VerPattern, Qt.BrushStyle.CrossPattern, Qt.BrushStyle.BDiagPattern,
            Qt.BrushStyle.FDiagPattern, Qt.BrushStyle.DiagCrossPattern
        ]
        
        self.pattern_previews = []
        for i, pattern in enumerate(patterns):
            row, col = divmod(i, 6)
            preview = PatternPreviewWidget(pattern, self.fg_color_button.color(), self.bg_color_button.color())
            self.pattern_grid.addWidget(preview, row, col)
            self.pattern_previews.append(preview)

        main_layout.addWidget(pattern_group)

        # Connections
        self.fg_color_button.color_changed.connect(self.update_pattern_colors)
        self.bg_color_button.color_changed.connect(self.update_pattern_colors)

    def update_pattern_colors(self):
        fg_color = self.fg_color_button.color()
        bg_color = self.bg_color_button.color()
        for preview in self.pattern_previews:
            preview.set_colors(fg_color, bg_color)