"main_window/docking_windows/project_tree_dock.py"
from PyQt6.QtWidgets import QDockWidget
from ..widgets.tree import CustomTreeWidget

class ProjectTreeDock(QDockWidget):
    """
    Dockable window to display the project file structure.
    """
    def __init__(self, main_window):
        """
        Initializes the Project Tree dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Project Tree", main_window)
        self.setObjectName("project_tree")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(CustomTreeWidget())
