# main_window\docking_windows\controller_list_dock.py
from PyQt6.QtWidgets import QDockWidget, QTextEdit

class ControllerListDock(QDockWidget):
    """
    Dockable window to display a list of connected controllers.
    """
    def __init__(self, main_window):
        """
        Initializes the Controller List dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Controller List", main_window)
        self.setObjectName("controller_list")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(QTextEdit("Controller List"))
