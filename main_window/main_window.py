import sys
from PyQt6.QtWidgets import QMainWindow, QCheckBox, QTextEdit
from PyQt6.QtCore import Qt, QSize, QByteArray

# Import the menu classes from the new modules
from .menus.file_menu import FileMenu
from .menus.edit_menu import EditMenu
from .menus.search_replace_menu import SearchReplaceMenu
from .menus.view_menu import ViewMenu
from .menus.screen_menu import ScreenMenu
from .menus.common_menu import CommonMenu
from .menus.figure_menu import FigureMenu
from .menus.object_menu import ObjectMenu

# Import the toolbar classes
from .toolbars.docking_toolbar import DockingToolbar
from .toolbars.view_toolbar import ViewToolbar
from .toolbars.screen_toolbar import ScreenToolbar
from .toolbars.edit_toolbar import EditToolbar
from .toolbars.alignment_toolbar import AlignmentToolbar
from .toolbars.figure_toolbar import FigureToolbar
from .toolbars.object_toolbar import ObjectToolbar
from .toolbars.debug_toolbar import DebugToolbar

# Import the dock widget factory
from .docking_windows.dock_widget_factory import DockWidgetFactory

class MainWindow(QMainWindow):
    """
    This is the main window of the application.
    It inherits from QMainWindow.
    """
    def __init__(self, settings_service):
        """
        Constructor for the MainWindow class.
        """
        super().__init__()
        self.settings_service = settings_service

        # Set the window title
        self.setWindowTitle("HMI Designer")

        # Set the initial size of the window (width, height)
        self.setGeometry(0, 0, 1200, 720)
        
        self.setIconSize(QSize(24, 24))
        
        # Set the central widget
        self.setCentralWidget(QTextEdit("Central Workspace"))

        # Allow nested docks and tabbed docks
        self.setDockNestingEnabled(True)

        # Create the menu bar by instantiating the menu classes
        self._create_menu_bar()
        # Create the toolbars
        self._create_toolbars()
        # Create the dock widgets
        self._create_dock_widgets()
        
        # Restore window state from settings
        self._restore_window_state()
        
        # Sync UI elements like checkboxes to the restored state
        self._sync_checkboxes_to_widget_visibility()

    def _create_menu_bar(self):
        """
        Creates the menu bar for the main window by instantiating
        the dedicated class for each menu.
        """
        menu_bar = self.menuBar()
        
        # Instantiate each menu class to build the menu bar
        self.file_menu = FileMenu(self, menu_bar)
        self.edit_menu = EditMenu(self, menu_bar)
        self.search_replace_menu = SearchReplaceMenu(self, menu_bar)
        self.view_menu = ViewMenu(self, menu_bar)
        self.screen_menu = ScreenMenu(self, menu_bar)
        self.common_menu = CommonMenu(self, menu_bar)
        self.figure_menu = FigureMenu(self, menu_bar)
        self.object_menu = ObjectMenu(self, menu_bar)

    def _create_toolbars(self):
        """Creates the toolbars for the main window."""
        self.toolbars = {}
        self.toolbars["Window Display"] = DockingToolbar(self, self.view_menu)
        self.toolbars["View"] = ViewToolbar(self, self.view_menu)
        self.toolbars["Screen"] = ScreenToolbar(self, self.screen_menu)
        self.toolbars["Edit"] = EditToolbar(self, self.edit_menu)
        self.toolbars["Alignment"] = AlignmentToolbar(self, self.edit_menu)
        self.toolbars["Figure"] = FigureToolbar(self, self.figure_menu)
        self.toolbars["Object"] = ObjectToolbar(self, self.object_menu)
        self.toolbars["Debug"] = DebugToolbar(self)
        
        for name, toolbar in self.toolbars.items():
            # Set a unique object name for each toolbar so its state can be saved.
            toolbar.setObjectName(f"{name.lower().replace(' ', '_')}_toolbar")
            self.addToolBar(toolbar)
            toolbar.setIconSize(self.iconSize())
            
        # Connect the toggle actions from the view menu
        for action in self.view_menu.tool_bar_menu.actions():
            widget = action.defaultWidget()
            checkbox = widget.findChild(QCheckBox)
            if checkbox:
                toolbar_name = action.text()
                if toolbar_name in self.toolbars:
                    # Use a lambda to capture the toolbar name correctly
                    checkbox.toggled.connect(
                        lambda checked, name=toolbar_name: self.toggle_toolbar(checked, name)
                    )

    def _create_dock_widgets(self):
        """Creates and arranges all dock widgets."""
        self.dock_factory = DockWidgetFactory(self)
        self.dock_factory.create_all_docks()

        # DOCKING SETUP
        # All dock widgets are movable and closable by default.
        # We allow them to be tabbed.
        
        # --- Left Area ---
        project_tree = self.dock_factory.get_dock("project_tree")
        screen_tree = self.dock_factory.get_dock("screen_tree")
        system_tree = self.dock_factory.get_dock("system_tree")
        
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, project_tree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, screen_tree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, system_tree)
        
        # Tabify the left docks
        self.tabifyDockWidget(project_tree, screen_tree)
        self.tabifyDockWidget(screen_tree, system_tree)

        # --- Right Area ---
        property_tree = self.dock_factory.get_dock("property_tree")
        library = self.dock_factory.get_dock("library")
        screen_image_list = self.dock_factory.get_dock("screen_image_list")
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, property_tree)
        self.splitDockWidget(property_tree, library, Qt.Orientation.Vertical)
        self.tabifyDockWidget(library, screen_image_list)

        # --- Bottom Area ---
        tag_search = self.dock_factory.get_dock("tag_search")
        data_browser = self.dock_factory.get_dock("data_browser")
        ip_address = self.dock_factory.get_dock("ip_address")
        controller_list = self.dock_factory.get_dock("controller_list")
        data_view = self.dock_factory.get_dock("data_view")

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, tag_search)
        self.tabifyDockWidget(tag_search, data_browser)
        self.tabifyDockWidget(data_browser, ip_address)
        self.tabifyDockWidget(ip_address, controller_list)
        self.tabifyDockWidget(controller_list, data_view)

        # Connect the toggle actions from the view menu
        for action in self.view_menu.docking_window_menu.actions():
            widget = action.defaultWidget()
            checkbox = widget.findChild(QCheckBox)
            if checkbox:
                # The object name must match the key in the factory's dock dict
                dock_name = action.text().lower().replace(' ', '_')
                if self.dock_factory.get_dock(dock_name):
                    checkbox.toggled.connect(
                        lambda checked, name=dock_name: self.toggle_dock_widget(checked, name)
                    )

    def toggle_toolbar(self, checked, name):
        """Shows or hides the toolbar with the given name."""
        if name in self.toolbars:
            self.toolbars[name].setVisible(checked)

    def toggle_dock_widget(self, checked, name):
        """Shows or hides the dock widget with the given name."""
        dock = self.dock_factory.get_dock(name)
        if dock:
            dock.setVisible(checked)

    def _restore_window_state(self):
        """Restores the window geometry and state from settings."""
        main_window_settings = self.settings_service.get_main_window_settings()
        geometry = main_window_settings.get('geometry')
        state = main_window_settings.get('state')

        if geometry:
            self.restoreGeometry(QByteArray.fromHex(bytes(geometry, 'utf-8')))
        if state:
            self.restoreState(QByteArray.fromHex(bytes(state, 'utf-8')))
        else:
            # If no state, maximize the window
            self.setWindowState(Qt.WindowState.WindowMaximized)

    def _sync_checkboxes_to_widget_visibility(self):
        """
        After restoring state, syncs the visibility checkboxes in the View menu
        to match the last saved visibility state from the settings file, as
        querying widget visibility right after restoring state can be unreliable.
        """
        toolbars_visibility = self.settings_service.get_toolbars_visibility()
        docks_visibility = self.settings_service.get_docks_visibility()

        # Sync toolbar checkboxes
        for action in self.view_menu.tool_bar_menu.actions():
            widget = action.defaultWidget()
            checkbox = widget.findChild(QCheckBox)
            if checkbox:
                toolbar_name = action.text()
                # Default to True if the toolbar is new and not in settings
                is_visible = toolbars_visibility.get(toolbar_name, True)
                checkbox.blockSignals(True)
                checkbox.setChecked(is_visible)
                checkbox.blockSignals(False)

        # Sync dock widget checkboxes
        for action in self.view_menu.docking_window_menu.actions():
            widget = action.defaultWidget()
            checkbox = widget.findChild(QCheckBox)
            if checkbox:
                dock_name = action.text().lower().replace(' ', '_')
                dock = self.dock_factory.get_dock(dock_name)
                if dock:
                    # Default to True if the dock is new and not in settings
                    is_visible = docks_visibility.get(dock_name, True)
                    checkbox.blockSignals(True)
                    checkbox.setChecked(is_visible)
                    checkbox.blockSignals(False)

    def closeEvent(self, event):
        """
        Handles the window's close event. Overridden to save settings.
        
        Args:
            event (QCloseEvent): The close event.
        """
        self.settings_service.save_settings(self)
        super().closeEvent(event)
