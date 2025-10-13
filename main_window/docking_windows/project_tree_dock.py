# main_window\docking_windows\project_tree_dock.py
import copy
from PyQt6.QtWidgets import QDockWidget, QTreeWidgetItem, QMenu, QDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from ..widgets.tree import CustomTreeWidget
from ..services.icon_service import IconService
from ..dialogs.project_tree.project_information_dialog import ProjectInformationDialog
from ..dialogs.project_tree.tag_dialog import TagDialog
from ..dialogs.project_tree.comment_dialog import CommentDialog
from ..dialogs.project_tree.alarm_dialog import AlarmDialog
from ..dialogs.project_tree.logging_dialog import LoggingDialog
from ..dialogs.project_tree.recipe_dialog import RecipeDialog
from ..dialogs.project_tree.script_dialog import ScriptDialog
from ..dialogs.project_tree.device_data_transfer_dialog import DeviceDataTransferDialog
from ..dialogs.project_tree.trigger_action_dialog import TriggerActionDialog
from ..dialogs.project_tree.time_action_dialog import TimeActionDialog
from ..dialogs.project_tree.image_dialog import ImageDialog
from ..dialogs.project_tree.animation_dialog import AnimationDialog
from project.comment.comment_table import CommentTable
from project.tag.tag_table import TagTable


class ProjectTreeDock(QDockWidget):
    """
    Dockable window to display the project file structure.
    """
    def __init__(self, main_window):
        """
        Initializes the Project Tree dock widget.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        super().__init__("Project Tree", main_window)
        self.main_window = main_window
        self.setObjectName("project_tree")
        self._clipboard = None

        self.tree_widget = CustomTreeWidget()
        self.setWidget(self.tree_widget)
        
        self._populate_tree()

        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_widget.itemDoubleClicked.connect(self.handle_double_click)

    def keyPressEvent(self, event):
        """Handle key press events for cut, copy, paste, and delete."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            super().keyPressEvent(event)
            return

        item = selected_items[0]
        
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_item(item)
            event.accept()
        elif event.matches(QKeySequence.StandardKey.Cut):
            self.cut_item(item)
            event.accept()
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste_item(item)
            event.accept()
        elif event.matches(QKeySequence.StandardKey.Delete):
             self.delete_item(item)
             event.accept()
        else:
            super().keyPressEvent(event)

    def _populate_tree(self):
        """
        Populates the tree with project items.
        """
        self.system_item = self._add_item("System", "dock-system-tree")
        self.screen_item = self._add_item("Screen", "dock-screen-tree")
        self.project_info_item = self._add_item("Project Information", "common-system-information")
        self.tag_item = self._add_item("Tag", "common-tags")
        self.comment_item = self._add_item("Comment", "common-comment")
        self.alarm_item = self._add_item("Alarm", "common-alarm")
        self.logging_item = self._add_item("Logging", "common-logging")
        self.recipe_item = self._add_item("Recipe", "object-recipe")
        self.script_item = self._add_item("Script", "common-script")
        self.device_data_transfer_item = self._add_item("Device Data Transfer", "common-tags-data-transfer")
        self.trigger_action_item = self._add_item("Trigger Action", "common-trigger-action")
        self.time_action_item = self._add_item("Time Action", "common-time-action")
        self.image_item = self._add_item("Image", "figure-image")
        self.animation_item = self._add_item("Animation", "object-animation")

    def _add_item(self, name, icon_name):
        item = QTreeWidgetItem(self.tree_widget, [name])
        item.setIcon(0, IconService.get_icon(icon_name))
        return item

    def handle_double_click(self, item, column):
        """
        Handles double-click events on tree items.
        """
        if item == self.system_item:
            self.main_window.set_dock_widget_visibility("system_tree", True)
        elif item == self.screen_item:
            self.main_window.set_dock_widget_visibility("screen_tree", True)
        elif item == self.project_info_item:
            dialog = ProjectInformationDialog(self)
            dialog.exec()
        elif item.parent() == self.comment_item:
            self.open_comment(item)
        elif item.parent() == self.tag_item:
            self.open_tag(item)


    def show_context_menu(self, position):
        """
        Shows a context menu when an item is right-clicked.
        """
        item = self.tree_widget.itemAt(position)
        if not item:
            return

        menu = QMenu()
        parent = item.parent()

        if item == self.tag_item:
            action = menu.addAction("Add New Tag List")
            action.triggered.connect(self.add_new_tag)
            menu.addSeparator()
            paste_action = menu.addAction(IconService.get_icon('edit-paste'), "Paste")
            paste_action.setEnabled(self._clipboard is not None and self._clipboard.get('type') == 'tag')
            paste_action.triggered.connect(lambda: self.paste_item(item))
            import_action = menu.addAction(IconService.get_icon('common-import'), "Import")
            import_action.triggered.connect(self.import_tags)
        elif parent == self.tag_item:
            open_action = menu.addAction(IconService.get_icon('screen-open'), "Open")
            open_action.triggered.connect(lambda: self.open_tag(item))
            menu.addSeparator()
            cut_action = menu.addAction(IconService.get_icon('edit-cut'), "Cut")
            cut_action.triggered.connect(lambda: self.cut_item(item))
            copy_action = menu.addAction(IconService.get_icon('edit-copy'), "Copy")
            copy_action.triggered.connect(lambda: self.copy_item(item))
            paste_action = menu.addAction(IconService.get_icon('edit-paste'), "Paste")
            paste_action.setEnabled(self._clipboard is not None and self._clipboard.get('type') == 'tag')
            paste_action.triggered.connect(lambda: self.paste_item(item))
            menu.addSeparator()
            properties_action = menu.addAction(IconService.get_icon('screen-property'), "Properties")
            properties_action.triggered.connect(lambda: self.show_tag_properties(item))
            menu.addSeparator()
            delete_action = menu.addAction(IconService.get_icon('edit-delete'), "Delete")
            delete_action.triggered.connect(lambda: self.delete_item(item))
        elif item == self.comment_item:
            action = menu.addAction("Add New Comment")
            action.triggered.connect(self.add_new_comment)
            menu.addSeparator()
            paste_action = menu.addAction(IconService.get_icon('edit-paste'), "Paste")
            paste_action.setEnabled(self._clipboard is not None and self._clipboard.get('type') == 'comment')
            paste_action.triggered.connect(lambda: self.paste_item(item))
            import_action = menu.addAction(IconService.get_icon('common-import'), "Import")
            import_action.triggered.connect(self.import_comments)
        elif parent == self.comment_item:
            open_action = menu.addAction(IconService.get_icon('screen-open'), "Open")
            open_action.triggered.connect(lambda: self.open_comment(item))
            menu.addSeparator()
            cut_action = menu.addAction(IconService.get_icon('edit-cut'), "Cut")
            cut_action.triggered.connect(lambda: self.cut_item(item))
            copy_action = menu.addAction(IconService.get_icon('edit-copy'), "Copy")
            copy_action.triggered.connect(lambda: self.copy_item(item))
            paste_action = menu.addAction(IconService.get_icon('edit-paste'), "Paste")
            paste_action.setEnabled(self._clipboard is not None and self._clipboard.get('type') == 'comment')
            paste_action.triggered.connect(lambda: self.paste_item(item))
            menu.addSeparator()
            properties_action = menu.addAction(IconService.get_icon('screen-property'), "Properties")
            properties_action.triggered.connect(lambda: self.show_comment_properties(item))
            menu.addSeparator()
            delete_action = menu.addAction(IconService.get_icon('edit-delete'), "Delete")
            delete_action.triggered.connect(lambda: self.delete_item(item))
        elif item == self.alarm_item:
            action = menu.addAction("Add New Alarm List")
            action.triggered.connect(lambda: self.open_dialog(AlarmDialog))
        elif item == self.logging_item:
            action = menu.addAction("Add New Logging List")
            action.triggered.connect(lambda: self.open_dialog(LoggingDialog))
        elif item == self.recipe_item:
            action = menu.addAction("Add New Recipe List")
            action.triggered.connect(lambda: self.open_dialog(RecipeDialog))
        elif item == self.script_item:
            action = menu.addAction("Add New Script List")
            action.triggered.connect(lambda: self.open_dialog(ScriptDialog))
        elif item == self.device_data_transfer_item:
            action = menu.addAction("Add New Device Data Transfer List")
            action.triggered.connect(lambda: self.open_dialog(DeviceDataTransferDialog))
        elif item == self.trigger_action_item:
            action = menu.addAction("Add New Trigger Action List")
            action.triggered.connect(lambda: self.open_dialog(TriggerActionDialog))
        elif item == self.time_action_item:
            action = menu.addAction("Add New Time Action List")
            action.triggered.connect(lambda: self.open_dialog(TimeActionDialog))
        elif item == self.image_item:
            action = menu.addAction("Add New Image List")
            action.triggered.connect(lambda: self.open_dialog(ImageDialog))
        elif item == self.animation_item:
            action = menu.addAction("Add New Animation List")
            action.triggered.connect(lambda: self.open_dialog(AnimationDialog))

        if not menu.isEmpty():
            menu.exec(self.tree_widget.viewport().mapToGlobal(position))
            
    def get_existing_comment_numbers(self):
        numbers = []
        for i in range(self.comment_item.childCount()):
            child = self.comment_item.child(i)
            data = child.data(0, Qt.ItemDataRole.UserRole)
            if data and 'number' in data:
                numbers.append(data['number'])
        return numbers

    def add_new_comment(self):
        existing_numbers = self.get_existing_comment_numbers()
        dialog = CommentDialog(self, existing_comment_numbers=existing_numbers)
        if dialog.exec():
            comment_data = dialog.get_comment_data()
            if comment_data:
                # Add item to tree
                comment_text = f"{comment_data['number']} - {comment_data['name']}"
                new_item = QTreeWidgetItem(self.comment_item, [comment_text])
                new_item.setData(0, Qt.ItemDataRole.UserRole, comment_data)
                new_item.setIcon(0, IconService.get_icon('common-comment'))
                self.comment_item.setExpanded(True)
                
                # Open tab in main window
                self.main_window.open_comment_table(comment_data)

    def get_existing_tag_numbers(self):
        numbers = []
        for i in range(self.tag_item.childCount()):
            child = self.tag_item.child(i)
            data = child.data(0, Qt.ItemDataRole.UserRole)
            if data and 'number' in data:
                numbers.append(data['number'])
        return numbers

    def add_new_tag(self):
        existing_numbers = self.get_existing_tag_numbers()
        dialog = TagDialog(self, existing_tag_numbers=existing_numbers)
        if dialog.exec():
            tag_data = dialog.get_tag_data()
            if tag_data:
                # Add item to tree
                tag_text = f"{tag_data['number']} - {tag_data['name']}"
                new_item = QTreeWidgetItem(self.tag_item, [tag_text])
                new_item.setData(0, Qt.ItemDataRole.UserRole, tag_data)
                new_item.setIcon(0, IconService.get_icon('common-tags'))
                self.tag_item.setExpanded(True)
                
                # Open tab in main window
                self.main_window.open_tag_table(tag_data)
            
    def open_tag(self, item):
        tag_data = item.data(0, Qt.ItemDataRole.UserRole)
        if tag_data:
            self.main_window.open_tag_table(tag_data)

    def open_comment(self, item):
        comment_data = item.data(0, Qt.ItemDataRole.UserRole)
        if comment_data:
            self.main_window.open_comment_table(comment_data)

    def cut_item(self, item):
        self.copy_item(item)
        self.delete_item(item, confirm=False)

    def copy_item(self, item):
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        parent = item.parent()
        item_type = None
        if parent == self.tag_item:
            item_type = 'tag'
        elif parent == self.comment_item:
            item_type = 'comment'

        if item_type:
            self._clipboard = copy.deepcopy(data)
            self._clipboard['type'] = item_type

    def paste_item(self, item):
        if not self._clipboard:
            return

        clipboard_type = self._clipboard.get('type')
        pasted_data = copy.deepcopy(self._clipboard)
        del pasted_data['type']

        if clipboard_type == 'tag':
            existing_numbers = self.get_existing_tag_numbers()
            new_number = pasted_data['number']
            while new_number in existing_numbers:
                new_number += 1
            pasted_data['number'] = new_number
            pasted_data['name'] += " (copy)"
            
            tag_text = f"{pasted_data['number']} - {pasted_data['name']}"
            new_item = QTreeWidgetItem(self.tag_item, [tag_text])
            new_item.setData(0, Qt.ItemDataRole.UserRole, pasted_data)
            new_item.setIcon(0, IconService.get_icon('common-tags'))
            self.tag_item.setExpanded(True)

        elif clipboard_type == 'comment':
            existing_numbers = self.get_existing_comment_numbers()
            new_number = pasted_data['number']
            while new_number in existing_numbers:
                new_number += 1
            pasted_data['number'] = new_number
            pasted_data['name'] += " (copy)"
            
            comment_text = f"{pasted_data['number']} - {pasted_data['name']}"
            new_item = QTreeWidgetItem(self.comment_item, [comment_text])
            new_item.setData(0, Qt.ItemDataRole.UserRole, pasted_data)
            new_item.setIcon(0, IconService.get_icon('common-comment'))
            self.comment_item.setExpanded(True)

    def show_tag_properties(self, item):
        tag_data = item.data(0, Qt.ItemDataRole.UserRole)
        if not tag_data:
            return

        existing_numbers = self.get_existing_tag_numbers()
        current_number = tag_data.get("number")
        editable_numbers = [num for num in existing_numbers if num != current_number]
        
        dialog = TagDialog(self, existing_tag_numbers=editable_numbers, initial_data=tag_data)

        if dialog.exec():
            updated_data = dialog.get_tag_data()
            updated_data['number'] = current_number # Keep original number
            item.setData(0, Qt.ItemDataRole.UserRole, updated_data)
            item.setText(0, f"{updated_data['number']} - {updated_data['name']}")
            
            self.main_window.close_tag_tab_by_number(current_number)
            self.main_window.open_tag_table(updated_data)

    def show_comment_properties(self, item):
        comment_data = item.data(0, Qt.ItemDataRole.UserRole)
        if not comment_data:
            return

        existing_numbers = self.get_existing_comment_numbers()
        current_number = comment_data.get("number")
        editable_numbers = [num for num in existing_numbers if num != current_number]
        
        dialog = CommentDialog(self, existing_comment_numbers=editable_numbers, initial_data=comment_data)

        if dialog.exec():
            updated_data = dialog.get_comment_data()
            updated_data['number'] = current_number # Keep original number
            item.setData(0, Qt.ItemDataRole.UserRole, updated_data)
            item.setText(0, f"{updated_data['number']} - {updated_data['name']}")
            
            self.main_window.close_comment_tab_by_number(current_number)
            self.main_window.open_comment_table(updated_data)

    def delete_item(self, item, confirm=True):
        if not item or not item.parent():
            return

        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return

        reply = QMessageBox.StandardButton.Yes
        if confirm:
            reply = QMessageBox.question(self, "Delete Item", 
                                         f"Are you sure you want to delete '{data.get('name')}'?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            item_number = data.get('number')
            parent = item.parent()

            parent.removeChild(item)
            
            if parent == self.tag_item:
                self.main_window.close_tag_tab_by_number(item_number)
            elif parent == self.comment_item:
                self.main_window.close_comment_tab_by_number(item_number)
            
    def open_dialog(self, dialog_class):
        dialog = dialog_class(self)
        dialog.exec()

    def paste_tag(self):
        # Placeholder for future implementation
        print("Paste Tag action triggered.")

    def import_tags(self):
        # Placeholder for future implementation
        print("Import Tags action triggered.")

    def export_tags(self):
        # Placeholder for future implementation
        print("Export Tags action triggered.")

    def paste_comment(self):
        # Placeholder for future implementation
        print("Paste Comment action triggered.")

    def import_comments(self):
        # Placeholder for future implementation
        print("Import Comments action triggered.")

    def export_comments(self):
        # Placeholder for future implementation
        print("Export Comments action triggered.")

