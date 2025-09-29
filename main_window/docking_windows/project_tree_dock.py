"main_window/docking_windows/project_tree_dock.py"
from PyQt6.QtWidgets import QDockWidget, QTreeWidgetItem, QMenu, QDialog
from PyQt6.QtCore import Qt
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

        self.tree_widget = CustomTreeWidget()
        self.setWidget(self.tree_widget)
        
        self._populate_tree()

        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_widget.itemDoubleClicked.connect(self.handle_double_click)

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

    def show_context_menu(self, position):
        """
        Shows a context menu when an item is right-clicked.
        """
        item = self.tree_widget.itemAt(position)
        if not item:
            return

        menu = QMenu()
        action = None

        if item == self.tag_item:
            action = menu.addAction("Add New Tag List")
            action.triggered.connect(lambda: self.open_dialog(TagDialog))
        elif item == self.comment_item:
            action = menu.addAction("Add New Comment")
            action.triggered.connect(lambda: self.open_dialog(CommentDialog))
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

        if action:
            menu.exec(self.tree_widget.viewport().mapToGlobal(position))
            
    def open_dialog(self, dialog_class):
        dialog = dialog_class(self)
        dialog.exec()

