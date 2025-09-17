"main_window/menus/screen_menu.py"
from PyQt6.QtGui import QAction
from ..services.icon_service import IconService

class ScreenMenu:
    """
    Creates the 'Screen' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        self.main_window = main_window
        screen_menu = menu_bar.addMenu("&Screen")
        
        # New Screen Submenu
        new_screen_icon = IconService.get_icon('screen-new')
        new_screen_menu = screen_menu.addMenu(new_screen_icon, "New Screen")
        self.base_screen_action = QAction(IconService.get_icon('screen-base'), "Base Screen", self.main_window)
        new_screen_menu.addAction(self.base_screen_action)
        self.window_screen_action = QAction(IconService.get_icon('screen-window'), "Window Screen", self.main_window)
        new_screen_menu.addAction(self.window_screen_action)
        self.template_screen_action = QAction(IconService.get_icon('screen-template'), "Template Screen", self.main_window)
        new_screen_menu.addAction(self.template_screen_action)
        self.widgets_action = QAction(IconService.get_icon('screen-widgets'), "Widgets", self.main_window)
        new_screen_menu.addAction(self.widgets_action)

        open_screen_icon = IconService.get_icon('screen-open')
        close_screen_icon = IconService.get_icon('screen-close')
        close_all_screens_icon = IconService.get_icon('screen-close-all')
        screen_design_icon = IconService.get_icon('screen-design')
        screen_property_icon = IconService.get_icon('screen-property')
        
        self.open_screen_action = QAction(open_screen_icon, "Open Screen", self.main_window)
        screen_menu.addAction(self.open_screen_action)
        self.close_screen_action = QAction(close_screen_icon, "Close Screen", self.main_window)
        screen_menu.addAction(self.close_screen_action)
        self.close_all_screens_action = QAction(close_all_screens_icon, "Close All Screens", self.main_window)
        screen_menu.addAction(self.close_all_screens_action)
        screen_menu.addSeparator()
        self.screen_design_action = QAction(screen_design_icon, "Screen Design...", self.main_window)
        screen_menu.addAction(self.screen_design_action)
        self.screen_property_action = QAction(screen_property_icon, "Screen Property...", self.main_window)
        screen_menu.addAction(self.screen_property_action)
