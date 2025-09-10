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
        new_action = QAction(qta.icon('ei.file-new'),"New", self)
        open_action = QAction(qta.icon('fa5.folder-open'),"Open", self)
        save_action = QAction(qta.icon('fa5.save'),"Save", self)
        save_as_action = QAction(qta.icon('mdi.content-save-all-outline'),"Save As", self)
        run_action = QAction(qta.icon('msc.run-all'),"Run", self)
        close_tab_action = QAction(qta.icon('fa5.window-close'),"Close Tab", self)
        close_all_tabs_action = QAction(qta.icon('mdi.close-box-multiple'),"Close All Tabs", self)
        exit_action = QAction(qta.icon('mdi.exit-to-app'),"Exit", self)

        new_action.setShortcut("Ctrl+N")
        open_action.setShortcut("Ctrl+O")
        save_action.setShortcut("Ctrl+S")
        save_as_action.setShortcut("Ctrl+Shift+S")
        run_action.setShortcut("F4")
        close_tab_action.setShortcut("Ctrl+W")
        close_all_tabs_action.setShortcut("Ctrl+Shift+W")
        exit_action.setShortcut("Ctrl+Q")

        # Exit action
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
        undo_action = QAction(qta.icon('fa5s.undo-alt'),"Undo", self)
        redo_action = QAction(qta.icon('fa5s.redo-alt'),"Redo", self)
        cut_action = QAction(qta.icon('fa5s.cut'),"Cut", self)
        copy_action = QAction(qta.icon('fa5.copy'),"Copy", self)
        paste_action = QAction(qta.icon('mdi6.content-paste'),"Paste", self)
        dublicate_action = QAction(qta.icon('fa5.clone'),"Dublicate", self)
        consecutive_copy_action = QAction("Consecutive Copy", self)
        select_all_action = QAction("Select All", self)
        delete_action = QAction(qta.icon('mdi.delete'),"Delete", self)
        stacking_order_action = QAction("Stacking Order", self)
        align_action = QAction(qta.icon('fa6s.align-center'),"Align", self)
        wrap_action = QAction("Wrap", self)
        flip_action = QAction("Flip", self)
        
        undo_action.setShortcut("Ctrl+Z")
        redo_action.setShortcut("Ctrl+Y")
        cut_action.setShortcut("Ctrl+X")
        copy_action.setShortcut("Ctrl+C")
        paste_action.setShortcut("Ctrl+V")
        dublicate_action.setShortcut("Ctrl+D")
        consecutive_copy_action.setShortcut("Ctrl+Shift+C")
        select_all_action.setShortcut("Ctrl+V")
        delete_action.setShortcut("Del")

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

