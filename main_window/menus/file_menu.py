"main_window/menus/file_menu.py"
from PyQt6.QtGui import QAction
from ..services.icon_service import IconService

class FileMenu:
    """
    Creates the 'File' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        file_menu = menu_bar.addMenu("&File")

        # Create multicolor icons
        new_icon = IconService.get_icon('file-new')
        open_icon = IconService.get_icon('folder-open')
        save_icon = IconService.get_icon('file-save')
        save_as_icon = IconService.get_icon('file-save-as')
        run_icon = IconService.get_icon('run')
        close_tab_icon = IconService.get_icon('window-close')
        close_all_tabs_icon = IconService.get_icon('windows-close')
        exit_icon = IconService.get_icon('exit')

        # New, Open, Save actions
        self.new_action = QAction(new_icon,"New", main_window)
        self.open_action = QAction(open_icon,"Open", main_window)
        self.save_action = QAction(save_icon,"Save", main_window)
        self.save_as_action = QAction(save_as_icon,"Save As", main_window)
        run_action = QAction(run_icon,"Run", main_window)
        close_tab_action = QAction(close_tab_icon,"Close Tab", main_window)
        close_all_tabs_action = QAction(close_all_tabs_icon,"Close All Tabs", main_window)
        exit_action = QAction(exit_icon,"Exit", main_window)

        self.new_action.setShortcut("Ctrl+N")
        self.open_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        run_action.setShortcut("F4")
        close_tab_action.setShortcut("Ctrl+W")
        close_all_tabs_action.setShortcut("Ctrl+Shift+W")
        exit_action.setShortcut("Ctrl+Q")

        # Connect actions to slots
        self.new_action.triggered.connect(main_window.new_project)
        self.open_action.triggered.connect(main_window.open_project)
        self.save_action.triggered.connect(main_window.save_project)
        self.save_as_action.triggered.connect(main_window.save_project_as)

        # Exit action
        exit_action.triggered.connect(main_window.close)

        # Add actions to the File menu
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addAction(run_action)
        file_menu.addSeparator()
        file_menu.addAction(close_tab_action)
        file_menu.addAction(close_all_tabs_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
