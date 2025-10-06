# main_window\docking_windows\ip_address_dock.py
from PyQt6.QtWidgets import QDockWidget, QTextEdit

class IPAddressDock(QDockWidget):
    """
    Dockable window to manage and display IP addresses of devices.
    """
    def __init__(self, main_window):
        """
        Initializes the IP Address dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("IP Address", main_window)
        self.setObjectName("ip_address")

        # Set a central widget to avoid rendering glitches.
        self.setWidget(QTextEdit("IP Address"))
