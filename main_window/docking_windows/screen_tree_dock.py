"main_window/docking_windows/screen_tree_dock.py"
from PyQt6.QtWidgets import QDockWidget, QTreeWidget, QTreeWidgetItem

class ScreenTreeDock(QDockWidget):
    """
    Dockable window to display the hierarchy of screens in the project.
    """
    def __init__(self, main_window):
        """
        Initializes the Screen Tree dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Screen Tree", main_window)
        self.setObjectName("screen_tree")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(QTreeWidget())
