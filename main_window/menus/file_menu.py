from PyQt6.QtGui import QAction
import qtawesome as qta

class FileMenu:
    """
    Creates the 'File' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        file_menu = menu_bar.addMenu("&File")

        # Create multicolor icons
        new_icon = qta.icon('fa5s.file-alt', 'fa5s.plus-circle', options=[{'color': '#4285f4'}, {'color': '#34a853', 'scale_factor': 0.6}])
        open_icon = qta.icon('fa5s.folder', 'fa5.folder-open', options=[{'color': '#fbbc05'}, {'color': '#f8991d', 'opacity': 0.8}])
        save_icon = qta.icon('fa5.save', 'fa5s.save', options=[{'color': '#bbdefb'}, {'color': '#4285f4'}])
        save_as_icon = qta.icon('fa5s.save', 'fa5s.copy', options=[{'color': '#4285f4', 'offset': (0.15, 0.15), 'opacity': 0.7}, {'color': '#4285f4'}])
        run_icon = qta.icon('fa5s.play-circle', options=[{'color': '#34a853'}])
        close_tab_icon = qta.icon('fa5s.window-maximize', 'fa5s.times', options=[{'color': '#5f6368'}, {'color': '#ea4335', 'scale_factor': 0.5}])
        close_all_tabs_icon = qta.icon('fa5s.window-close', 'fa5.window-close', options=[{'color':'#ea4335', 'offset':(0.1, -0.1)}, {'color':'#c5221f'}])
        exit_icon = qta.icon('fa5s.sign-out-alt', options=[{'color': '#ea4335'}])

        # New, Open, Save actions
        new_action = QAction(new_icon,"New", main_window)
        open_action = QAction(open_icon,"Open", main_window)
        save_action = QAction(save_icon,"Save", main_window)
        save_as_action = QAction(save_as_icon,"Save As", main_window)
        run_action = QAction(run_icon,"Run", main_window)
        close_tab_action = QAction(close_tab_icon,"Close Tab", main_window)
        close_all_tabs_action = QAction(close_all_tabs_icon,"Close All Tabs", main_window)
        exit_action = QAction(exit_icon,"Exit", main_window)

        new_action.setShortcut("Ctrl+N")
        open_action.setShortcut("Ctrl+O")
        save_action.setShortcut("Ctrl+S")
        save_as_action.setShortcut("Ctrl+Shift+S")
        run_action.setShortcut("F4")
        close_tab_action.setShortcut("Ctrl+W")
        close_all_tabs_action.setShortcut("Ctrl+Shift+W")
        exit_action.setShortcut("Ctrl+Q")

        # Exit action
        exit_action.triggered.connect(main_window.close)

        # Add actions to the File menu
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(run_action)
        file_menu.addSeparator()
        file_menu.addAction(close_tab_action)
        file_menu.addAction(close_all_tabs_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

