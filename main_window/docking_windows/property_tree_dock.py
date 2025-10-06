# main_window\docking_windows\property_tree_dock.py
from PyQt6.QtWidgets import QDockWidget
from ..widgets.tree import CustomTreeWidget

class PropertyTreeDock(QDockWidget):
    """
    Dockable window to display the properties of the selected object.
    """
    def __init__(self, main_window):
        """
        Initializes the Property Tree dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Property Tree", main_window)
        self.setObjectName("property_tree")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(CustomTreeWidget())
