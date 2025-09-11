import sys
from PyQt6.QtWidgets import QMainWindow, QCheckBox
from PyQt6.QtCore import Qt, QSize

# Import the menu classes from the new modules
from .menus.file_menu import FileMenu
from .menus.edit_menu import EditMenu
from .menus.search_replace_menu import SearchReplaceMenu
from .menus.view_menu import ViewMenu
from .menus.screen_menu import ScreenMenu
from .menus.common_menu import CommonMenu
from .menus.figure_menu import FigureMenu
from .menus.object_menu import ObjectMenu

# Import the toolbar classes
# from .toolbars.window_display_toolbar import WindowDisplayToolbar
from .toolbars.view_toolbar import ViewToolbar
from .toolbars.screen_toolbar import ScreenToolbar
from .toolbars.edit_toolbar import EditToolbar
from .toolbars.alignment_toolbar import AlignmentToolbar
from .toolbars.figure_toolbar import FigureToolbar
from .toolbars.object_toolbar import ObjectToolbar
# from .toolbars.debug_toolbar import DebugToolbar


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

        self.setIconSize(QSize(24, 24))

        # Create the menu bar by instantiating the menu classes
        self._create_menu_bar()
        # Create the toolbars
        self._create_toolbars()

    def _create_menu_bar(self):
        """
        Creates the menu bar for the main window by instantiating
        the dedicated class for each menu.
        """
        menu_bar = self.menuBar()
        
        # Instantiate each menu class to build the menu bar
        self.file_menu = FileMenu(self, menu_bar)
        self.edit_menu = EditMenu(self, menu_bar)
        self.search_replace_menu = SearchReplaceMenu(self, menu_bar)
        self.view_menu = ViewMenu(self, menu_bar)
        self.screen_menu = ScreenMenu(self, menu_bar)
        self.common_menu = CommonMenu(self, menu_bar)
        self.figure_menu = FigureMenu(self, menu_bar)
        self.object_menu = ObjectMenu(self, menu_bar)

    def _create_toolbars(self):
        """Creates the toolbars for the main window."""
        self.toolbars = {}
        # self.toolbars["Window Display"] = WindowDisplayToolbar(self)
        self.toolbars["View"] = ViewToolbar(self, self.view_menu)
        self.toolbars["Screen"] = ScreenToolbar(self, self.screen_menu)
        self.toolbars["Edit"] = EditToolbar(self, self.edit_menu)
        self.toolbars["Alignment"] = AlignmentToolbar(self, self.edit_menu)
        self.toolbars["Figure"] = FigureToolbar(self, self.figure_menu)
        self.toolbars["Object"] = ObjectToolbar(self, self.object_menu)
        # self.toolbars["Debug"] = DebugToolbar(self)
        
        for toolbar in self.toolbars.values():
            self.addToolBar(toolbar)
            toolbar.setIconSize(self.iconSize())
            
        # Connect the toggle actions from the view menu
        for action in self.view_menu.tool_bar_menu.actions():
            widget = action.defaultWidget()
            checkbox = widget.findChild(QCheckBox)
            if checkbox:
                toolbar_name = action.text()
                if toolbar_name in self.toolbars:
                    # Use a lambda to capture the toolbar name correctly
                    checkbox.toggled.connect(
                        lambda checked, name=toolbar_name: self.toggle_toolbar(checked, name)
                    )

    def toggle_toolbar(self, checked, name):
        """Shows or hides the toolbar with the given name."""
        if name in self.toolbars:
            self.toolbars[name].setVisible(checked)

