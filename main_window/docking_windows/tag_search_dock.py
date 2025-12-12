# main_window\docking_windows\tag_search_dock.py
from PySide6.QtWidgets import QDockWidget, QTextEdit

class TagSearchDock(QDockWidget):
    """
    Dockable window for searching devices on the network.
    """
    def __init__(self, main_window):
        """
        Initializes the Device Search dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Tag Search", main_window)
        self.setObjectName("tag_search")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(QTextEdit("Tag Search"))
