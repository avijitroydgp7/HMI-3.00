# screen\base\canvas_base_screen.py
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QPixmap, QPen, QFont
from PyQt6.QtCore import Qt, QRectF, pyqtSignal


class CanvasWidget(QGraphicsWidget):
    """
    A QGraphicsWidget that represents the actual content of the screen.
    This widget handles the drawing of the background and any content on the screen.
    """
    def __init__(self, screen_data):
        super().__init__()
        self.screen_data = screen_data
        width = self.screen_data.get("width", 1920)
        height = self.screen_data.get("height", 1080)
        self.setGeometry(0, 0, width, height)
        self.update_background()

    def update_background(self):
        """Updates the background based on the screen's design data."""
        self.update()  # Trigger a repaint

    def paint(self, painter, option, widget=None):
        """Paint the background and content of the screen."""
        design_data = self.screen_data.get("design")
        rect = self.boundingRect()

        # Default background
        painter.fillRect(rect, QColor("lightgrey"))

        if design_data:
            style_type = design_data.get("type")
            
            if style_type == "color":
                color = QColor(design_data.get("color", "#F15B5B"))
                painter.fillRect(rect, color)
            
            elif style_type == "gradient":
                grad_data = design_data.get("gradient")
                if grad_data:
                    gradient = QLinearGradient(0, 0, rect.width(), rect.height())
                    gradient.setColorAt(0, QColor(grad_data['color1']))
                    gradient.setColorAt(1, QColor(grad_data['color2']))
                    painter.fillRect(rect, QBrush(gradient))

            elif style_type == "pattern":
                patt_data = design_data.get("pattern")
                if patt_data:
                    fg_color = QColor(patt_data["fg_color"])
                    bg_color = QColor(patt_data["bg_color"])
                    painter.fillRect(rect, bg_color)
                    brush = QBrush(fg_color, patt_data["pattern"])
                    painter.fillRect(rect, brush)
            
            elif style_type == "image":
                path = design_data.get("image_path")
                if path:
                    pixmap = QPixmap(path)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(rect.size().toSize(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        x = rect.x() + (rect.width() - scaled_pixmap.width()) / 2
                        y = rect.y() + (rect.height() - scaled_pixmap.height()) / 2
                        painter.drawPixmap(int(x), int(y), scaled_pixmap)

class CanvasBaseScreen(QGraphicsView):
    """
    A QGraphicsView that acts as a container for a screen, providing zoom and pan functionality.
    """
    zoom_changed = pyqtSignal(float)

    def __init__(self, screen_data, parent=None):
        super().__init__(parent)
        self.screen_data = screen_data
        self.zoom_factor = 1.0

        # Create a scene and the canvas widget
        self.scene = QGraphicsScene(self)
        self.canvas_widget = CanvasWidget(self.screen_data)
        self.scene.addItem(self.canvas_widget)
        self.setScene(self.scene)
        
        # Configure the view
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.fit_screen()

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        """Handle key press events for zooming and panning."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Plus or event.key() == Qt.Key.Key_Equal:
                self.zoom_in()
                event.accept()
            elif event.key() == Qt.Key.Key_Minus:
                self.zoom_out()
                event.accept()
            elif event.key() == Qt.Key.Key_0:
                self.fit_screen()
                event.accept()
            else:
                super().keyPressEvent(event)
        elif event.key() == Qt.Key.Key_Space:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            event.accept()
        else:
            super().keyPressEvent(event)
            
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
        else:
            super().keyReleaseEvent(event)

    def zoom(self, factor):
        """Apply a zoom factor to the view, respecting min/max limits."""
        new_zoom_factor = self.zoom_factor * factor
        
        # Clamp the zoom factor between a minimum (e.g., 10%) and maximum (1000%)
        if 0.1 <= new_zoom_factor <= 10.0:
            self.zoom_factor = new_zoom_factor
            self.resetTransform()
            self.scale(self.zoom_factor, self.zoom_factor)
            self.zoom_changed.emit(self.zoom_factor)

    def zoom_in(self):
        """Zoom in by a predefined factor."""
        self.zoom(1.1)

    def zoom_out(self):
        """Zoom out by a predefined factor."""
        self.zoom(0.9)
        
    def set_zoom_level(self, level_str):
        """Set zoom to a specific percentage (e.g., "100%"), respecting limits."""
        try:
            level = float(level_str.strip('%')) / 100.0
            # Clamp the level to the allowed range (10% to 1000%)
            clamped_level = max(0.1, min(level, 10.0))
            
            if self.zoom_factor != clamped_level:
                self.zoom_factor = clamped_level
                self.resetTransform()
                self.scale(self.zoom_factor, self.zoom_factor)
                self.zoom_changed.emit(self.zoom_factor)

        except (ValueError, ZeroDivisionError):
            pass

    def fit_screen(self):
        """Fit the entire screen content within the view."""
        self.fitInView(self.canvas_widget.boundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom_factor = self.transform().m11()
        self.zoom_changed.emit(self.zoom_factor)
