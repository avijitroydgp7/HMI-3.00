import sys
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt

# Import the menu classes from the new modules
from .menus.file_menu import FileMenu
from .menus.edit_menu import EditMenu
from .menus.search_replace_menu import SearchReplaceMenu
from .menus.view_menu import ViewMenu
from .menus.screen_menu import ScreenMenu
from .menus.common_menu import CommonMenu
from .menus.figure_menu import FigureMenu
from .menus.object_menu import ObjectMenu


class MainWindow(QMainWindow):
    """
    This is the main window of the application.
    It inherits from QMainWindow.
    """
    def __init__(self):
        """
        Constructor for the MainWindow class.
        """
        super().__init__()

        # Set the window title
        self.setWindowTitle("HMI Designer")

        # Set the initial size of the window (width, height)
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowState(Qt.WindowState.WindowMaximized)

        # Create the menu bar by instantiating the menu classes
        self._create_menu_bar()

    def _create_menu_bar(self):
        """
        Creates the menu bar for the main window by instantiating
        the dedicated class for each menu.
        """
        menu_bar = self.menuBar()
        
        # Instantiate each menu class to build the menu bar
        FileMenu(self, menu_bar)
        EditMenu(self, menu_bar)
        SearchReplaceMenu(self, menu_bar)
        ViewMenu(self, menu_bar)
        ScreenMenu(self, menu_bar)
        CommonMenu(self, menu_bar)
        FigureMenu(self, menu_bar)
        ObjectMenu(self, menu_bar)