"main_window/docking_windows/system_tree_dock.py"
from PyQt6.QtWidgets import QDockWidget
from ..widgets.tree import CustomTreeWidget

class SystemTreeDock(QDockWidget):
    """
    Dockable window to display system-level components and settings.
    """
    def __init__(self, main_window):
        """
        Initializes the System Tree dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("System Tree", main_window)
        self.setObjectName("system_tree")
        
        # Set a central widget to avoid rendering glitches.
        self.setWidget(CustomTreeWidget())
