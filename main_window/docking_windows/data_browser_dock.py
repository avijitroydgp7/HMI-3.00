from PyQt6.QtWidgets import QDockWidget, QTextEdit

class DataBrowserDock(QDockWidget):
    """
    Dockable window for browsing data sources and tags.
    """
    def __init__(self, main_window):
        """
        Initializes the Data Browser dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Data Browser", main_window)
        self.setObjectName("data_browser")

