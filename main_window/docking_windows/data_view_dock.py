# main_window\docking_windows\data_view_dock.py
from PyQt6.QtWidgets import QDockWidget, QTextEdit

class DataViewDock(QDockWidget):
    """
    Dockable window to view real-time data from tags.
    """
    def __init__(self, main_window):
        """
        Initializes the Data View dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Data View", main_window)
        self.setObjectName("data_view")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(QTextEdit("Data View"))
