import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStyleFactory
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import qtawesome as qta

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
        self.setGeometry(0,0, 1920, 1080)
        self.setWindowState(Qt.WindowState.WindowMaximized)

        # Create the menu bar
        self._create_menu_bar()

        # You can add widgets and layouts here in the future

    def _create_menu_bar(self):
        """
        Creates the menu bar for the main window.
        """
        menu_bar = self.menuBar()

        # --- File Menu ---
        file_menu = menu_bar.addMenu("&File")

        # New, Open, Save actions
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        save_as_action = QAction("Save As", self)
        run_action = QAction("Run", self)

        # Exit action
        close_tab_action = QAction("Close Tab", self)
        close_all_tabs_action = QAction("Close All Tabs", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close) # Connects the action to closing the window

        # Add actions to the File menu
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(run_action)
        file_menu.addSeparator() # Adds a separator line
        file_menu.addAction(close_tab_action)
        file_menu.addAction(close_all_tabs_action)
        file_menu.addSeparator() # Adds a separator line
        file_menu.addAction(exit_action)



        # --- Edit Menu ---
        edit_menu = menu_bar.addMenu("&Edit")

        # Cut, Copy, Paste actions
        undo_action = QAction("Undo", self)
        redo_action = QAction("Redo", self)
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)
        dublicate_action = QAction("Dublicate", self)
        consecutive_copy_action = QAction("Consecutive Copy", self)
        select_all_action = QAction("Select All", self)
        delete_action = QAction("Delete", self)
        stacking_order_action = QAction("Stacking Order", self)
        align_action = QAction("Align", self)
        wrap_action = QAction("Wrap", self)
        flip_action = QAction("Flip", self)

        # Add actions to the Edit menu
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator() # Adds a separator line
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator() # Adds a separator line
        edit_menu.addAction(dublicate_action)
        edit_menu.addAction(consecutive_copy_action)
        edit_menu.addSeparator() # Adds a separator line
        edit_menu.addAction(select_all_action)
        edit_menu.addAction(delete_action)
        edit_menu.addSeparator() # Adds a separator line
        edit_menu.addAction(stacking_order_action)
        edit_menu.addAction(align_action)
        edit_menu.addAction(wrap_action)
        edit_menu.addAction(flip_action)

        # --- Search / replace ---
        search_replace_menu = menu_bar.addMenu("&Search/Replace")



        # --- View ---
        view_menu = menu_bar.addMenu("&View")



        # --- Screen ---
        screen_menu = menu_bar.addMenu("&Screen")



        # --- Common ---
        common_menu = menu_bar.addMenu("&Common")



        # --- Figure ---
        figure_menu = menu_bar.addMenu("&Figure")



        # --- Object ---
        object_menu = menu_bar.addMenu("&Object")



        # --- Communication ---
        commucation_menu = menu_bar.addMenu("&Communication")



        # --- Diagnostics ---
        diagostics_menu = menu_bar.addMenu("&Diagnostics")



        # --- Tools ---
        tools_menu = menu_bar.addMenu("&Tools")



        # --- Help ---
        help_menu = menu_bar.addMenu("&Help")




if __name__ == '__main__':
    # This part is for testing the window independently
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

