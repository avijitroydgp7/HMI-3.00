# main_window/docking_windows/screen_tree_dock.py
from PyQt6.QtWidgets import QDockWidget, QTreeWidgetItem, QMenu, QDialog
from PyQt6.QtCore import Qt
from ..dialogs.screen.screen_design import ScreenDesignDialog
from ..dialogs.screen.main_screen import MainScreenDialog
from ..dialogs.screen.window_screen import WindowScreenDialog
from ..dialogs.screen.template_screen import TemplateScreenDialog
from ..dialogs.screen.widgets_screen import WidgetsScreenDialog
from ..services.icon_service import IconService
from ..widgets.tree import CustomTreeWidget

class ScreenTreeDock(QDockWidget):
    """
    Dockable window to display the hierarchy of screens in the project.
    """
    def __init__(self, main_window):
        """
        Initializes the Screen Tree dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Screen Tree", main_window)
        self.setObjectName("screen_tree")

        self.tree_widget = CustomTreeWidget()
        self.setWidget(self.tree_widget)
        
        self._populate_tree()

        # Connect signals for context menus and double clicks
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_widget.itemDoubleClicked.connect(self.handle_double_click)
        
        # Counters for new items
        self.main_screen_count = 0
        self.window_screen_count = 0
        self.template_screen_count = 0
        self.widgets_screen_count = 0

    def _populate_tree(self):
        """
        Populates the tree with the initial screen structure.
        """
        # A single root for all screens
        screens_root = QTreeWidgetItem(self.tree_widget, ["Screens"])
        screens_root.setIcon(0, IconService.get_icon('dock-screen-tree'))

        # Child categories from the single root
        self.base_screens_root = QTreeWidgetItem(screens_root, ["Base Screens"])
        self.base_screens_root.setIcon(0, IconService.get_icon('screen-base'))

        self.window_screens_root = QTreeWidgetItem(screens_root, ["Window Screens"])
        self.window_screens_root.setIcon(0, IconService.get_icon('screen-window'))

        self.template_screens_root = QTreeWidgetItem(screens_root, ["Template Screens"])
        self.template_screens_root.setIcon(0, IconService.get_icon('screen-template')) 

        self.widgets_screens_root = QTreeWidgetItem(screens_root, ["Widgets"])
        self.widgets_screens_root.setIcon(0, IconService.get_icon('screen-widgets')) 
        
        # Expand all items to show the structure
        screens_root.setExpanded(True)
        self.base_screens_root.setExpanded(True)
        self.window_screens_root.setExpanded(True)
        self.template_screens_root.setExpanded(True)
        self.widgets_screens_root.setExpanded(True)

    def show_context_menu(self, position):
        """
        Shows a context menu when an item is right-clicked.
        """
        item = self.tree_widget.itemAt(position)
        if not item:
            return

        menu = QMenu()
        
        # Context menu for "Base Screens" category
        if item == self.base_screens_root:
            add_main_screen_action = menu.addAction("Add New Base Screen")
            add_main_screen_action.triggered.connect(self.add_main_screen)
        
        # Context menu for "Window Screens" category
        elif item == self.window_screens_root:
            add_window_screen_action = menu.addAction("Add New Window Screen")
            add_window_screen_action.triggered.connect(self.add_window_screen)

        # Context menu for "Template Screens" category
        elif item == self.template_screens_root:
            add_template_screen_action = menu.addAction("Add New Template Screen")
            add_template_screen_action.triggered.connect(self.add_template_screen)
            
        # Context menu for "Widgets" category
        elif item == self.widgets_screens_root:
            add_widgets_screen_action = menu.addAction("Add New Widgets Screen")
            add_widgets_screen_action.triggered.connect(self.add_widgets_screen)

        if menu.actions():
            menu.exec(self.tree_widget.viewport().mapToGlobal(position))

    def handle_double_click(self, item, column):
        """
        Handles double-click events on tree items.
        """
        if item == self.base_screens_root:
            self.open_screen_design()

    def open_screen_design(self):
        """
        Opens the screen design dialog.
        """
        dialog = ScreenDesignDialog(self)
        dialog.exec()

    def add_main_screen(self):
        """
        Opens a dialog and adds a new base screen as a child of "Base Screens".
        """
        dialog = MainScreenDialog(self)
        if dialog.exec():
            self.main_screen_count += 1
            new_item = QTreeWidgetItem(self.base_screens_root, [f"Base Screen {self.main_screen_count}"])
            new_item.setIcon(0, IconService.get_icon('screen-base-white'))
            self.base_screens_root.setExpanded(True)

    def add_window_screen(self):
        """
        Opens a dialog and adds a new window screen as a child of "Window Screens".
        """
        dialog = WindowScreenDialog(self)
        if dialog.exec():
            self.window_screen_count += 1
            new_item = QTreeWidgetItem(self.window_screens_root, [f"Window Screen {self.window_screen_count}"])
            new_item.setIcon(0, IconService.get_icon('screen-window-white'))

    def add_template_screen(self):
        """
        Opens a dialog and adds a new template screen as a child of "Template Screens".
        """
        dialog = TemplateScreenDialog(self)
        if dialog.exec():
            self.template_screen_count += 1
            new_item = QTreeWidgetItem(self.template_screens_root, [f"Template Screen {self.template_screen_count}"])
            new_item.setIcon(0, IconService.get_icon('screen-template-white'))

    def add_widgets_screen(self):
        """
        Opens a dialog and adds a new widget as a child of "Widgets".
        """
        dialog = WidgetsScreenDialog(self)
        if dialog.exec():
            self.widgets_screen_count += 1
            new_item = QTreeWidgetItem(self.widgets_screens_root, [f"Widget {self.widgets_screen_count}"])
            new_item.setIcon(0, IconService.get_icon('screen-widgets-white'))

