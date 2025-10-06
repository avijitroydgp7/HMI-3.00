# main_window\docking_windows\library_dock.py
from PyQt6.QtWidgets import QDockWidget
from ..widgets.tree import CustomTreeWidget

class LibraryDock(QDockWidget):
    """
    Dockable window to display a library of reusable components.
    """
    def __init__(self, main_window):
        """
        Initializes the Library dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Library", main_window)
        self.setObjectName("library")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(CustomTreeWidget())
