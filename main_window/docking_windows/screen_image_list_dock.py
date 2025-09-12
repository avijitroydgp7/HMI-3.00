from PyQt6.QtWidgets import QDockWidget, QTreeWidget, QTreeWidgetItem

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