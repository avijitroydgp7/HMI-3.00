"main_window/widgets/gradient_widget.py"
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QRadioButton, QPushButton, QLabel
)
from PyQt6.QtGui import QColor, QPainter, QLinearGradient, QBrush
from PyQt6.QtCore import pyqtSignal, QPointF, Qt

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

class GradientPreviewWidget(QWidget):
    """A widget to display a single gradient preview."""
    def __init__(self, color1, color2, stops, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.color1 = color1
        self.color2 = color2
        self.stops = stops

    def set_gradient(self, color1, color2, stops):
        self.color1 = color1
        self.color2 = color2
        self.stops = stops
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        
        gradient = QLinearGradient(QPointF(rect.topLeft()), QPointF(rect.bottomRight()))
        if self.stops == "Horizontal":
            gradient.setStart(QPointF(rect.left(), rect.center().y()))
            gradient.setFinalStop(QPointF(rect.right(), rect.center().y()))
        elif self.stops == "Vertical":
            gradient.setStart(QPointF(rect.center().x(), rect.top()))
            gradient.setFinalStop(QPointF(rect.center().x(), rect.bottom()))
        elif self.stops == "Up Diagonal":
            gradient.setStart(QPointF(rect.bottomLeft()))
            gradient.setFinalStop(QPointF(rect.topRight()))
        elif self.stops == "Down Diagonal":
            gradient.setStart(QPointF(rect.topLeft()))
            gradient.setFinalStop(QPointF(rect.bottomRight()))

        gradient.setColorAt(0, self.color1)
        gradient.setColorAt(1, self.color2)
        
        painter.fillRect(rect, QBrush(gradient))
        painter.setPen(QColor("grey"))
        painter.drawRect(rect.adjusted(0, 0, -1, -1))

class GradientWidget(QWidget):
    """A widget for selecting and previewing gradient colors."""
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)

        # Color Selection
        color_group = QGroupBox("Color")
        color_layout = QGridLayout(color_group)
        self.color1_button = ColorPickerButton(QColor("#D0CECE"))
        self.color2_button = ColorPickerButton(QColor("#596978"))
        color_layout.addWidget(QLabel("Color1"), 0, 0)
        color_layout.addWidget(self.color1_button, 0, 1)
        color_layout.addWidget(QLabel("Color2"), 1, 0)
        color_layout.addWidget(self.color2_button, 1, 1)
        main_layout.addWidget(color_group)

        # Gradation Type and Variation
        bottom_layout = QHBoxLayout()
        gradation_group = QGroupBox("Gradation Type")
        gradation_layout = QVBoxLayout(gradation_group)
        self.radio_horizontal = QRadioButton("Horizontal")
        self.radio_vertical = QRadioButton("Vertical")
        self.radio_up_diagonal = QRadioButton("Up Diagonal")
        self.radio_down_diagonal = QRadioButton("Down Diagonal")
        self.radio_horizontal.setChecked(True)
        gradation_layout.addWidget(self.radio_horizontal)
        gradation_layout.addWidget(self.radio_vertical)
        gradation_layout.addWidget(self.radio_up_diagonal)
        gradation_layout.addWidget(self.radio_down_diagonal)
        bottom_layout.addWidget(gradation_group)
        
        variation_group = QGroupBox("Variation")
        variation_layout = QGridLayout(variation_group)
        
        c1 = self.color1_button.color()
        c2 = self.color2_button.color()
        self.preview1 = GradientPreviewWidget(c1, c2, "Horizontal")
        self.preview2 = GradientPreviewWidget(c1, c2, "Vertical")
        self.preview3 = GradientPreviewWidget(c1, c2, "Up Diagonal")
        self.preview4 = GradientPreviewWidget(c1, c2, "Down Diagonal")
        
        variation_layout.addWidget(self.preview1, 0, 0)
        variation_layout.addWidget(self.preview2, 0, 1)
        variation_layout.addWidget(self.preview3, 1, 0)
        variation_layout.addWidget(self.preview4, 1, 1)
        bottom_layout.addWidget(variation_group)
        
        main_layout.addLayout(bottom_layout)

        # Connections
        self.color1_button.color_changed.connect(self.update_previews)
        self.color2_button.color_changed.connect(self.update_previews)
        self.radio_horizontal.toggled.connect(self.update_previews)
        self.radio_vertical.toggled.connect(self.update_previews)
        self.radio_up_diagonal.toggled.connect(self.update_previews)
        self.radio_down_diagonal.toggled.connect(self.update_previews)

    def update_previews(self):
        """Updates all gradient previews based on current selections."""
        c1 = self.color1_button.color()
        c2 = self.color2_button.color()
        self.preview1.set_gradient(c1, c2, "Horizontal")
        self.preview2.set_gradient(c1, c2, "Vertical")
        self.preview3.set_gradient(c1, c2, "Up Diagonal")
        self.preview4.set_gradient(c1, c2, "Down Diagonal")