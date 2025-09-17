# main_window/widgets/tree.py
from PyQt6.QtWidgets import QTreeWidget, QStyleFactory
from PyQt6.QtGui import QPalette, QColor

class CustomTreeWidget(QTreeWidget):
    """
    A custom QTreeWidget with default styling for the application.
    """
    def __init__(self, parent=None):
        """
        Initializes the CustomTreeWidget.
        """
        super().__init__(parent)
        self.setHeaderHidden(True)
        self._apply_styles()

    def _apply_styles(self):
        """
        Applies a consistent dark theme style to the tree widget,
        using the native Windows style for the tree structure.
        """
        # Apply the native Windows style for the classic tree view appearance
        self.setStyle(QStyleFactory.create("windows"))

        # Create and apply a custom palette for a dark theme with white elements
        palette = self.palette()
        dark_color = QColor(45, 45, 45)
        palette.setColor(QPalette.ColorRole.Window, dark_color)
        palette.setColor(QPalette.ColorRole.Base, dark_color)
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255)) # Item text
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))      # Item text
        palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 105, 189)) # Selection background
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255)) # Selected text
        # This role controls the color of the branch lines and +/- icons in the 'windows' style
        palette.setColor(QPalette.ColorRole.Dark, QColor(255, 255, 255))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QTreeWidget {
                border: none;
            }
        """)

