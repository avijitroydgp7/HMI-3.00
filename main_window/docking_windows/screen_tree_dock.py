# main_window\docking_windows\screen_tree_dock.py
from PyQt6.QtWidgets import QDockWidget, QTreeWidgetItem, QMenu, QDialog
from PyQt6.QtCore import Qt
from ..dialogs.screen.screen_design import ScreenDesignDialog
from ..dialogs.screen.base_screen import BaseScreenDialog
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
        self.main_window = main_window
        self.setObjectName("screen_tree")

        self.tree_widget = CustomTreeWidget()
        self.setWidget(self.tree_widget)
        
        self._populate_tree()

        # Connect signals for context menus and double clicks
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_widget.itemDoubleClicked.connect(self.handle_double_click)
        
        # Counters for new items
        self.window_screen_count = 0
        self.template_screen_count = 0
        self.widgets_screen_count = 0

    def _populate_tree(self):
        """
        Populates the tree with the initial screen structure.
        """
        # Add Screen Design as a top-level item
        self.screen_design_item = QTreeWidgetItem(self.tree_widget, ["Screen Design"])
        self.screen_design_item.setIcon(0, IconService.get_icon('screen-design'))

        # A single root for all other screens
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
        Handles double-click events on tree items to open screens.
        """
        if item == self.screen_design_item:
            self.open_screen_design()
        
        # Check if the double-clicked item is a screen (a child of one of the root nodes)
        parent = item.parent()
        if parent in [self.base_screens_root, self.window_screens_root, self.template_screens_root, self.widgets_screens_root]:
            screen_data = item.data(0, Qt.ItemDataRole.UserRole)
            if screen_data:
                self.main_window.open_screen(screen_data)

    def open_screen_design(self):
        """
        Opens the screen design dialog.
        """
        dialog = ScreenDesignDialog(self)
        dialog.exec()

    def get_existing_screen_numbers(self):
        """
        Retrieves all existing screen numbers from the data stored in the tree items.
        """
        numbers = []
        for i in range(self.base_screens_root.childCount()):
            child_item = self.base_screens_root.child(i)
            item_data = child_item.data(0, Qt.ItemDataRole.UserRole)
            if isinstance(item_data, dict) and "number" in item_data:
                numbers.append(item_data["number"])
        return numbers

    def add_main_screen(self):
        """
        Opens a dialog to get screen details and adds a new base screen to the tree.
        """
        existing_numbers = self.get_existing_screen_numbers()
        dialog = BaseScreenDialog(self, existing_screen_numbers=existing_numbers)
        
        if dialog.exec():
            data = dialog.get_screen_data()
            
            # Create the display text for the tree item
            new_item_text = f"[B] - {data['number']} - {data['name']}"
            new_item = QTreeWidgetItem(self.base_screens_root, [new_item_text])
            
            # Store the dictionary of screen data with the tree item
            new_item.setData(0, Qt.ItemDataRole.UserRole, data)
            
            new_item.setIcon(0, IconService.get_icon('screen-base-white'))
            self.base_screens_root.setExpanded(True)

            # Open the new screen in the main canvas
            self.main_window.open_screen(data)

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

