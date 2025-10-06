# main_window\toolbars\screen_toolbar.py
from PyQt6.QtWidgets import QToolBar

class ScreenToolbar(QToolBar):
    def __init__(self, main_window, screen_menu):
        super().__init__("Screen", main_window)
        self.main_window = main_window
        
        # Add actions from the screen menu
        self.addAction(screen_menu.open_screen_action)
        self.addAction(screen_menu.close_screen_action)
        self.addSeparator()
        self.addAction(screen_menu.screen_design_action)
        self.addAction(screen_menu.screen_property_action)
