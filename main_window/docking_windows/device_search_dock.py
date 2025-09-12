from PyQt6.QtWidgets import QDockWidget, QTextEdit

class DeviceSearchDock(QDockWidget):
    """
    Dockable window for searching devices on the network.
    """
    def __init__(self, main_window):
        """
        Initializes the Device Search dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Device Search", main_window)
        self.setObjectName("device_search")

