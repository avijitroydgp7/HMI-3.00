"screen/base/canvas_base_screen.py"
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QPixmap
from PyQt6.QtCore import Qt

class CanvasBaseScreen(QWidget):
    """
    A widget representing a single screen on the design canvas.
    This screen is resizable and its background can be styled.
    """
    def __init__(self, screen_data, parent=None):
        super().__init__(parent)
        self.screen_data = screen_data

        # Make the widget resizable
        self.setMinimumSize(200, 150)

        # Example: display screen name
        layout = QVBoxLayout(self)
        self.label = QLabel(f"Screen: {self.screen_data.get('name', 'N/A')}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.setAutoFillBackground(True)
        self.update_background()

    def update_background(self):
        """Updates the background based on the screen's design data."""
        design_data = self.screen_data.get("design")
        p = self.palette()
        
        if not design_data:
            p.setColor(self.backgroundRole(), QColor("lightgrey"))
            self.setPalette(p)
            return

        style_type = design_data.get("type")

        if style_type == "color":
            color = QColor(design_data.get("color", "#F15B5B"))
            p.setColor(self.backgroundRole(), color)
        
        elif style_type == "gradient":
            grad_data = design_data.get("gradient")
            if grad_data:
                gradient = QLinearGradient(0, 0, self.width(), self.height())
                gradient.setColorAt(0, QColor(grad_data['color1']))
                gradient.setColorAt(1, QColor(grad_data['color2']))
                p.setBrush(self.backgroundRole(), QBrush(gradient))

        elif style_type in ["pattern", "image"]:
            # These are handled by paintEvent, so we might not need to set a palette brush
            # or we could set a base color. For now, we'll let paintEvent handle it fully.
            pass
        
        self.setPalette(p)
        self.update() # Trigger a repaint

    def paintEvent(self, event):
        """Override paintEvent to handle complex backgrounds like patterns and images."""
        painter = QPainter(self)
        design_data = self.screen_data.get("design")

        # First, call the superclass paintEvent for basic background rendering if needed
        super().paintEvent(event)

        if design_data:
            style_type = design_data.get("type")
            
            if style_type == "pattern":
                patt_data = design_data.get("pattern")
                if patt_data:
                    fg_color = QColor(patt_data["fg_color"])
                    bg_color = QColor(patt_data["bg_color"])
                    painter.fillRect(self.rect(), bg_color)
                    brush = QBrush(fg_color, patt_data["pattern"])
                    painter.fillRect(self.rect(), brush)
            
            elif style_type == "image":
                path = design_data.get("image_path")
                if path:
                    pixmap = QPixmap(path)
                    if not pixmap.isNull():
                        # Scale pixmap to fit the widget while keeping aspect ratio
                        scaled_pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        # Center the image
                        x = (self.width() - scaled_pixmap.width()) / 2
                        y = (self.height() - scaled_pixmap.height()) / 2
                        painter.drawPixmap(int(x), int(y), scaled_pixmap)
        
        # We need to draw the children (like the label) over our custom background
        # A simple way is to not call super().paintEvent() at all and manage everything,
        # but that can be complex. Or, draw children after custom painting.
        # For simple widgets, not calling super() at the end is often fine.

    def resizeEvent(self, event):
        """Handle resize to update gradient or other size-dependent drawing."""
        self.update_background()
        super().resizeEvent(event)
