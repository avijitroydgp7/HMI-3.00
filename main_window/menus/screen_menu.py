from PyQt6.QtGui import QAction
import qtawesome as qta

class ScreenMenu:
    """
    Creates the 'Screen' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        self.main_window = main_window
        screen_menu = menu_bar.addMenu("&Screen")
        
        # New Screen Submenu
        new_screen_icon = qta.icon('fa5s.desktop', 'fa5s.plus', options=[{'color': '#5f6368'}, {'color': '#34a853', 'scale_factor': 0.5}])
        new_screen_menu = screen_menu.addMenu(new_screen_icon, "New Screen")
        self.base_screen_action = QAction(qta.icon('fa5s.file'), "Base Screen", self.main_window)
        new_screen_menu.addAction(self.base_screen_action)
        self.window_screen_action = QAction(qta.icon('fa5s.window-maximize'), "Window Screen", self.main_window)
        new_screen_menu.addAction(self.window_screen_action)
        self.report_action = QAction(qta.icon('fa5s.file-invoice'), "Report", self.main_window)
        new_screen_menu.addAction(self.report_action)

        open_screen_icon = qta.icon('fa5s.desktop', 'fa5s.folder-open', options=[{'color': '#5f6368'}, {'color': '#fbbc05', 'scale_factor': 0.5, 'offset': (0.1, 0.1)}])
        close_screen_icon = qta.icon('fa5s.desktop', 'fa5s.times-circle', options=[{'color': '#5f6368'}, {'color': '#ea4335', 'scale_factor': 0.5}])
        close_all_screens_icon = qta.icon('fa5.window-close', 'fa5s.window-close', options=[{'color':'#ea4335'}, {'color':'#c5221f'}])
        screen_design_icon = qta.icon('fa5s.palette', options=[{'color': '#4285f4'}])
        screen_property_icon = qta.icon('fa5s.cog', options=[{'color': '#5f6368'}])
        
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
