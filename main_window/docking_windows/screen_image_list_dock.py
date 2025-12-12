# main_window\docking_windows\screen_image_list_dock.py
from PySide6.QtWidgets import QDockWidget
from ..widgets.tree import CustomTreeWidget

class ScreenImageListDock(QDockWidget):
    """
    Dockable window to display a list of images used in the project.
    """
    def __init__(self, main_window):
        """
        Initializes the Screen Image List dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Screen Image List", main_window)
        self.setObjectName("screen_image_list")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(CustomTreeWidget())
