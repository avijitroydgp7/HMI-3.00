from PyQt6.QtWidgets import QTreeWidget

class CustomTreeWidget(QTreeWidget):
    """
    A custom QTreeWidget that inherits the application's style.
    """
    def __init__(self, parent=None):
        """
        Initializes the CustomTreeWidget.
        """
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setStyleSheet("""
            QTreeWidget {
                border: none;
            }
        """)

