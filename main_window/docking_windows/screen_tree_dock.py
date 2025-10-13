# main_window\docking_windows\screen_tree_dock.py
import copy
from PyQt6.QtWidgets import QDockWidget, QTreeWidgetItem, QMenu, QDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
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
        self._clipboard = None

        self.tree_widget = CustomTreeWidget()
        self.setWidget(self.tree_widget)
        
        self._populate_tree()

        # Connect signals for context menus and double clicks
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_widget.itemDoubleClicked.connect(self.handle_double_click)
        
        # Counters for new items
        self.template_screen_count = 0
        self.widgets_screen_count = 0

    def keyPressEvent(self, event):
        """Handle key press events for cut, copy, and paste."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            super().keyPressEvent(event)
            return

        item = selected_items[0]
        
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_screen(item)
            event.accept()
        elif event.matches(QKeySequence.StandardKey.Cut):
            self.cut_screen(item)
            event.accept()
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste_screen(item)
            event.accept()
        else:
            super().keyPressEvent(event)

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
        
        parent = item.parent()
        is_screen_item = parent in [self.base_screens_root, self.window_screens_root]

        if item == self.base_screens_root:
            add_main_screen_action = menu.addAction("Add New Base Screen")
            add_main_screen_action.triggered.connect(self.add_main_screen)
            paste_action = menu.addAction(IconService.get_icon('edit-paste'), "Paste")
            paste_action.setEnabled(self._clipboard is not None)
            paste_action.triggered.connect(lambda: self.paste_screen(item))
        
        elif item == self.window_screens_root:
            add_window_screen_action = menu.addAction("Add New Window Screen")
            add_window_screen_action.triggered.connect(self.add_window_screen)
            paste_action = menu.addAction(IconService.get_icon('edit-paste'), "Paste")
            paste_action.setEnabled(self._clipboard is not None and self._clipboard.get('type') == 'window')
            paste_action.triggered.connect(lambda: self.paste_screen(item))

        elif item == self.template_screens_root:
            add_template_screen_action = menu.addAction("Add New Template Screen")
            add_template_screen_action.triggered.connect(self.add_template_screen)
            
        elif item == self.widgets_screens_root:
            add_widgets_screen_action = menu.addAction("Add New Widgets Screen")
            add_widgets_screen_action.triggered.connect(self.add_widgets_screen)

        elif is_screen_item:
            open_action = menu.addAction(IconService.get_icon('screen-open'), "Open")
            open_action.triggered.connect(lambda: self.open_selected_screen(item))
            menu.addSeparator()
            cut_action = menu.addAction(IconService.get_icon('edit-cut'), "Cut")
            cut_action.triggered.connect(lambda: self.cut_screen(item))
            copy_action = menu.addAction(IconService.get_icon('edit-copy'), "Copy")
            copy_action.triggered.connect(lambda: self.copy_screen(item))
            paste_action = menu.addAction(IconService.get_icon('edit-paste'), "Paste")
            paste_action.setEnabled(self._clipboard is not None)
            paste_action.triggered.connect(lambda: self.paste_screen(item))
            menu.addSeparator()
            properties_action = menu.addAction(IconService.get_icon('screen-property'), "Properties")
            properties_action.triggered.connect(lambda: self.show_screen_properties(item))
            menu.addSeparator()
            delete_action = menu.addAction(IconService.get_icon('edit-delete'), "Delete")
            delete_action.triggered.connect(lambda: self.delete_screen(item))


        if menu.actions():
            menu.exec(self.tree_widget.viewport().mapToGlobal(position))

    def handle_double_click(self, item, column):
        """
        Handles double-click events on tree items to open screens.
        """
        if item == self.screen_design_item:
            self.open_screen_design()
        else:
            self.open_selected_screen(item)

    def open_selected_screen(self, item):
        if not item or not item.parent():
            return
            
        parent = item.parent()
        if parent in [self.base_screens_root, self.window_screens_root]:
            screen_data = item.data(0, Qt.ItemDataRole.UserRole)
            if screen_data:
                self.main_window.open_screen(screen_data)

    def open_screen_design(self):
        """
        Opens the screen design dialog and updates the project-wide template.
        """
        project_service = self.main_window.project_service
        template_data = project_service.get_screen_design_template()
        dialog = ScreenDesignDialog(self, initial_data=template_data)
        
        if dialog.exec():
            new_template_data = dialog.get_design_details()
            if new_template_data:
                project_service.set_screen_design_template(new_template_data)
                self.main_window.update_open_screens_from_template()

    def get_existing_screen_numbers(self, screen_type):
        """
        Retrieves all existing screen numbers for a specific screen type ('base' or 'window').
        """
        numbers = []
        root_item = None
        if screen_type == 'base':
            root_item = self.base_screens_root
        elif screen_type == 'window':
            root_item = self.window_screens_root
        
        if root_item:
            for i in range(root_item.childCount()):
                child_item = root_item.child(i)
                item_data = child_item.data(0, Qt.ItemDataRole.UserRole)
                if isinstance(item_data, dict) and "number" in item_data:
                    numbers.append(item_data["number"])
        return numbers


    def add_main_screen(self):
        """
        Opens a dialog to get screen details and adds a new base screen to the tree.
        """
        self._add_screen(BaseScreenDialog, self.base_screens_root, 'screen-base-white', "[B]", screen_type='base')

    def add_window_screen(self):
        """
        Opens a dialog and adds a new window screen as a child of "Window Screens".
        """
        self._add_screen(WindowScreenDialog, self.window_screens_root, 'screen-window-white', "[W]", screen_type='window')

    def _add_screen(self, dialog_class, parent_item, icon_name, prefix, screen_type, data_to_add=None):
        if data_to_add is None:
            existing_numbers = self.get_existing_screen_numbers(screen_type)
            dialog = dialog_class(self, existing_screen_numbers=existing_numbers)
            if not dialog.exec():
                return
            data = dialog.get_screen_data()
        else:
            data = data_to_add
        
        if not data: return
        
        new_item_text = f"{prefix} - {data['number']} - {data['name']}"
        new_item = QTreeWidgetItem(parent_item, [new_item_text])
        
        new_item.setData(0, Qt.ItemDataRole.UserRole, data)
        new_item.setIcon(0, IconService.get_icon(icon_name))
        parent_item.setExpanded(True)

        if data_to_add is None: # Only open if it's a new screen, not a paste
            self.main_window.open_screen(data)
            
    def cut_screen(self, item):
        self.copy_screen(item)
        self.delete_screen(item, confirm=False)

    def copy_screen(self, item):
        screen_data = item.data(0, Qt.ItemDataRole.UserRole)
        if screen_data:
            self._clipboard = copy.deepcopy(screen_data)

    def paste_screen(self, item):
        if not self._clipboard:
            return
            
        pasted_data = copy.deepcopy(self._clipboard)
        screen_type = pasted_data.get('type')
        
        # Find a new unique screen number within the correct category
        existing_numbers = self.get_existing_screen_numbers(screen_type)
        new_number = pasted_data['number']
        while new_number in existing_numbers:
            new_number += 1
        pasted_data['number'] = new_number
        pasted_data['name'] += " (copy)"
        
        if screen_type == 'base':
            self._add_screen(BaseScreenDialog, self.base_screens_root, 'screen-base-white', "[B]", screen_type, pasted_data)
        elif screen_type == 'window':
             self._add_screen(WindowScreenDialog, self.window_screens_root, 'screen-window-white', "[W]", screen_type, pasted_data)
             
    def show_screen_properties(self, item):
        screen_data = item.data(0, Qt.ItemDataRole.UserRole)
        if not screen_data:
            return
        
        screen_type = screen_data.get('type')
        existing_numbers = self.get_existing_screen_numbers(screen_type)
        current_number = screen_data.get("number")
        # Allow the current number to be "valid" for editing
        editable_numbers = [num for num in existing_numbers if num != current_number]

        dialog_class = BaseScreenDialog if screen_type == 'base' else WindowScreenDialog
        dialog = dialog_class(self, existing_screen_numbers=editable_numbers, initial_data=screen_data)

        if dialog.exec():
            updated_data = dialog.get_screen_data()
            item.setData(0, Qt.ItemDataRole.UserRole, updated_data)
            prefix = "[B]" if updated_data.get('type') == 'base' else "[W]"
            item.setText(0, f"{prefix} - {updated_data['number']} - {updated_data['name']}")
            
            screen_id = (screen_type, current_number)
            if self.main_window.is_screen_open(screen_id):
                self.main_window.close_screen_by_id(screen_id)
                self.main_window.open_screen(updated_data)

    def delete_screen(self, item, confirm=True):
        if not item or not item.parent():
            return

        screen_data = item.data(0, Qt.ItemDataRole.UserRole)
        if not screen_data:
            return

        reply = QMessageBox.StandardButton.Yes
        if confirm:
            reply = QMessageBox.question(self, "Delete Screen", 
                                         f"Are you sure you want to delete '{screen_data.get('name')}'?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            screen_number = screen_data.get('number')
            screen_type = screen_data.get('type')
            screen_id = (screen_type, screen_number)
            item.parent().removeChild(item)
            if screen_id is not None:
                self.main_window.close_screen_by_id(screen_id)


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

