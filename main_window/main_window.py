# main_window\main_window.py
import sys
from PyQt6.QtWidgets import QMainWindow, QCheckBox, QTextEdit, QMessageBox, QFileDialog, QTabWidget
from PyQt6.QtCore import Qt, QSize, QByteArray
from PyQt6.QtGui import QAction

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
from .services.icon_service import IconService
from services.project_service import ProjectService
from services.edit_service import EditService
from screen.base.canvas_base_screen import CanvasBaseScreen

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
        self.project_service = ProjectService()
        self.edit_service = EditService()
        self.open_screens = {} # Dictionary to track open screens {(type, number): widget}

        # Set the window title
        self.update_window_title()

        # Set the window icon
        self.setWindowIcon(IconService.get_icon("HMI-Designer-icon"))

        # Set the initial size of the window (width, height)
        self.setGeometry(0, 0, 1200, 720)
        
        self.setIconSize(QSize(24, 24))
        
        # Set the central widget to a tab widget for multiple screens
        self.central_widget = QTabWidget()
        self.central_widget.setTabsClosable(True)
        self.central_widget.setMovable(True)
        self.central_widget.currentChanged.connect(self.on_tab_changed)
        self.central_widget.tabCloseRequested.connect(self.close_screen_tab)
        self.setCentralWidget(self.central_widget)

        # Allow nested docks and tabbed docks
        self.setDockNestingEnabled(True)

        # Create the menu bar by instantiating the menu classes
        self._create_menu_bar()
        # Create the toolbars
        self._create_toolbars()
        # Create the dock widgets
        self._create_dock_widgets()
        
        # Connect UI signals to slots
        self._connect_signals()
        
        # Restore window state from settings
        self._restore_window_state()
        
        # Sync UI elements like checkboxes to the restored state
        self._sync_checkboxes_to_widget_visibility()

        # Restore other UI settings from the settings file
        self._restore_ui_settings()
        
        self.new_project()

    def update_window_title(self):
        """Updates the window title based on the project state."""
        title = "HMI Designer"
        project_name = "untitled.hmi"
        if self.project_service.file_path:
            project_name = self.project_service.file_path.split('/')[-1]
        
        if not self.project_service.is_saved:
            project_name += "*"
            
        self.setWindowTitle(f"{title} - {project_name}")

    def project_modified(self):
        """Slot to handle modifications to the project."""
        self.project_service.mark_as_unsaved()
        self.update_window_title()

    def get_project_content(self):
        """Gets the current project content. (Placeholder for multi-screen)"""
        return ""

    def set_project_content(self, content):
        """Sets the project content. (Placeholder for multi-screen)"""
        pass

    def new_project(self):
        if not self.prompt_to_save():
            return
        self.project_service.new_project()
        self.central_widget.clear()
        self.open_screens.clear()
        self.update_window_title()

    def prepare_project_data(self):
        """Prepares project data for saving."""
        # This will need to be updated to serialize all open screens
        return {
            'content': self.get_project_content(),
        }

    def open_project(self):
        """Opens a project from a file."""
        if not self.prompt_to_save():
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "HMI Project Files (*.hmi)")
        if file_path:
            success, message = self.project_service.load_project(file_path)
            if success:
                # Restore project content to central widget
                project_data = self.project_service.project_data
                if project_data and 'content' in project_data:
                    self.set_project_content(project_data['content'])
                self.update_window_title()
            else:
                QMessageBox.warning(self, "Load Error", message)

    def save_project(self):
        """Saves the current project."""
        if not self.project_service.file_path:
            return self.save_project_as()
        else:
            # Prepare project data before saving
            self.project_service.project_data = self.prepare_project_data()

            success, message = self.project_service.save_project()
            if success:
                self.update_window_title()
                return True
            else:
                QMessageBox.warning(self, "Save Error", message)
                return False

    def save_project_as(self):
        """Saves the project with a new file name."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Project As", "", "HMI Project Files (*.hmi)")
        if file_path:
            # Prepare project data before saving
            self.project_service.project_data = self.prepare_project_data()

            success, message = self.project_service.save_project(file_path)
            if success:
                self.update_window_title()
                return True
            else:
                QMessageBox.warning(self, "Save Error", message)
                return False
        return False

    def open_screen(self, screen_data):
        """Creates and opens a new screen in a tab, or activates an existing one."""
        if not screen_data:
            return

        screen_type = screen_data.get('type')
        screen_number = screen_data.get('number')
        
        if not screen_type or screen_number is None:
            return

        screen_id = (screen_type, screen_number)

        if screen_id in self.open_screens:
            widget_to_activate = self.open_screens.get(screen_id)
            if widget_to_activate:
                self.central_widget.setCurrentWidget(widget_to_activate)
            return

        screen_widget = CanvasBaseScreen(screen_data, self.project_service, parent=self)
        screen_widget.zoom_changed.connect(lambda zf, sw=screen_widget: self.sync_zoom_controls(sw))
        
        if screen_type == 'base':
            tab_title = f"[B] - {screen_number} - {screen_data.get('name')}"
            icon = IconService.get_icon("screen-base")
        elif screen_type == 'window':
            tab_title = f"[W] - {screen_number} - {screen_data.get('name')}"
            icon = IconService.get_icon("screen-window")
        else:
            return # Don't open unsupported types for now

        index = self.central_widget.addTab(screen_widget, tab_title)
        self.central_widget.setTabIcon(index, icon)

        self.open_screens[screen_id] = screen_widget
        self.central_widget.setCurrentWidget(screen_widget)

    def is_screen_open(self, screen_id):
        return screen_id in self.open_screens

    def close_screen_by_id(self, screen_id):
        if screen_id in self.open_screens:
            widget_to_close = self.open_screens[screen_id]
            index = self.central_widget.indexOf(widget_to_close)
            if index != -1:
                self.central_widget.removeTab(index)
            del self.open_screens[screen_id]

    def get_screen_id_for_widget(self, widget):
        for screen_id, screen_widget in self.open_screens.items():
            if screen_widget is widget:
                return screen_id
        return None

    def close_screen_tab(self, index):
        """Closes a screen tab."""
        widget = self.central_widget.widget(index)
        if not widget:
            return

        screen_id_to_remove = self.get_screen_id_for_widget(widget)
        
        if screen_id_to_remove is not None:
            del self.open_screens[screen_id_to_remove]

        self.central_widget.removeTab(index)
            
    def prompt_to_save(self):
        if self.project_service.is_saved:
            return True
        
        reply = QMessageBox.question(self, 'Save Project',
                                     "You have unsaved changes. Would you like to save them?",
                                     QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Save:
            return self.save_project()
        elif reply == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def update_open_screens_from_template(self):
        """
        Reloads the configuration for any open screens that use the default template.
        """
        screens_to_reopen = []
        for screen_id, widget in self.open_screens.items():
            screen_data = widget.screen_data
            # If the screen is a base screen and has no individual design, it needs updating.
            if screen_data.get("type") == "base" and not screen_data.get("design"):
                 screens_to_reopen.append(screen_data)
        
        for screen_data in screens_to_reopen:
            screen_id = (screen_data.get('type'), screen_data.get('number'))
            self.close_screen_by_id(screen_id)
            self.open_screen(screen_data)
        
        if screens_to_reopen:
             self.project_modified()

    def _connect_signals(self):
        """Connect all signals for the main window."""
        # --- File Menu ---
        self.file_menu.new_action.triggered.connect(self.new_project)
        self.file_menu.open_action.triggered.connect(self.open_project)
        self.file_menu.save_action.triggered.connect(self.save_project)
        self.file_menu.save_as_action.triggered.connect(self.save_project_as)

        # --- Edit Menu ---
        self.edit_menu.undo_action.triggered.connect(self.undo_active_widget)
        self.edit_menu.redo_action.triggered.connect(self.redo_active_widget)
        self.edit_menu.cut_action.triggered.connect(self.cut_active_widget)
        self.edit_menu.copy_action.triggered.connect(self.copy_active_widget)
        self.edit_menu.paste_action.triggered.connect(self.paste_active_widget)
        self.edit_menu.select_all_action.triggered.connect(self.select_all_in_active_widget)
        self.edit_menu.delete_action.triggered.connect(self.delete_in_active_widget)

        # --- View Menu & Toolbar (Zoom) ---
        self.view_menu.zoom_action_group.triggered.connect(self.on_zoom_action_triggered)
        self.view_menu.fit_screen_action.triggered.connect(self.on_fit_screen_triggered)

        view_toolbar = self.toolbars.get("View")
        if view_toolbar:
            view_toolbar.zoom_in_button.clicked.connect(self.on_zoom_in_triggered)
            view_toolbar.zoom_out_button.clicked.connect(self.on_zoom_out_triggered)
            view_toolbar.zoom_combo.currentTextChanged.connect(self.on_zoom_combo_changed)

        # --- Screen Menu ---
        screen_tree = self.dock_factory.get_dock("screen_tree")
        if screen_tree:
            self.screen_menu.base_screen_action.triggered.connect(screen_tree.add_main_screen)
            self.screen_menu.window_screen_action.triggered.connect(screen_tree.add_window_screen)
            self.screen_menu.template_screen_action.triggered.connect(screen_tree.add_template_screen)
            self.screen_menu.widgets_action.triggered.connect(screen_tree.add_widgets_screen)
            self.screen_menu.screen_design_action.triggered.connect(screen_tree.open_screen_design)
            
        # --- Toolbar Visibility ---
        for action in self.view_menu.tool_bar_menu.actions():
            widget = action.defaultWidget()
            checkbox = widget.findChild(QCheckBox)
            if checkbox:
                toolbar_name = action.text()
                if toolbar_name in self.toolbars:
                    checkbox.toggled.connect(
                        lambda checked, name=toolbar_name: self.toggle_toolbar(checked, name)
                    )

        # --- Dock Widget Visibility ---
        for action in self.view_menu.docking_window_menu.actions():
            dock_name = action.text().lower().replace(' ', '_')
            if self.dock_factory.get_dock(dock_name):
                # Connect menu checkbox
                menu_checkbox = action.defaultWidget().findChild(QCheckBox)
                if menu_checkbox:
                    menu_checkbox.toggled.connect(
                        lambda checked, name=dock_name: self.set_dock_widget_visibility(name, checked)
                    )
                
                # Connect toolbar action
                toolbar = self.toolbars.get("Window Display")
                if toolbar:
                    toolbar_action = toolbar.findChild(QAction, f"toggle_{dock_name}")
                    if toolbar_action:
                        toolbar_action.toggled.connect(
                             lambda checked, name=dock_name: self.set_dock_widget_visibility(name, checked)
                        )

    def get_active_screen_widget(self):
        """Returns the widget from the currently active tab."""
        return self.central_widget.currentWidget()

    def on_tab_changed(self, index):
        """Handles syncing UI when the current tab is changed."""
        widget = self.central_widget.widget(index)
        if isinstance(widget, CanvasBaseScreen):
            self.sync_zoom_controls(widget)
        else:
            # No screen active, maybe disable some controls. For now, pass.
            pass
            
    # --- Zoom Handlers ---
    def on_zoom_action_triggered(self, action):
        """Handles when a zoom percentage is selected from the menu."""
        active_screen = self.get_active_screen_widget()
        if isinstance(active_screen, CanvasBaseScreen):
            view_toolbar = self.toolbars.get("View")
            if view_toolbar:
                # This will trigger on_zoom_combo_changed, which does the actual work
                view_toolbar.zoom_combo.setCurrentText(action.text())

    def on_zoom_combo_changed(self, text):
        """Handles when the zoom combo box text changes."""
        active_screen = self.get_active_screen_widget()
        if isinstance(active_screen, CanvasBaseScreen):
            # Block the screen's signal to prevent a feedback loop
            active_screen.blockSignals(True)
            active_screen.set_zoom_level(text)
            active_screen.blockSignals(False)
            self.sync_zoom_controls(active_screen)

    def on_fit_screen_triggered(self):
        """Fits the active screen to the view."""
        active_screen = self.get_active_screen_widget()
        if isinstance(active_screen, CanvasBaseScreen):
            active_screen.fit_screen()
            # The sync will be triggered by the zoom_changed signal

    def on_zoom_in_triggered(self):
        """Zooms in on the active screen."""
        active_screen = self.get_active_screen_widget()
        if isinstance(active_screen, CanvasBaseScreen):
            active_screen.zoom_in()
            # The sync will be triggered by the zoom_changed signal

    def on_zoom_out_triggered(self):
        """Zooms out on the active screen."""
        active_screen = self.get_active_screen_widget()
        if isinstance(active_screen, CanvasBaseScreen):
            active_screen.zoom_out()
            # The sync will be triggered by the zoom_changed signal
    
    def sync_zoom_controls(self, active_screen):
        """Updates the zoom combobox and menu from the screen's zoom factor."""
        if not (self.toolbars.get("View") and isinstance(active_screen, CanvasBaseScreen)):
            return

        view_toolbar = self.toolbars.get("View")
        zoom_factor = active_screen.zoom_factor
        new_zoom_percentage_str = f"{zoom_factor * 100:.0f}%"

        # --- Update Toolbar ComboBox ---
        view_toolbar.zoom_combo.blockSignals(True)
        if view_toolbar.zoom_combo.findText(new_zoom_percentage_str) == -1:
            zoom_levels = [float(view_toolbar.zoom_combo.itemText(i).strip('%')) for i in range(view_toolbar.zoom_combo.count())]
            new_zoom_level = float(new_zoom_percentage_str.strip('%'))
            
            insert_index = 0
            for i, level in enumerate(zoom_levels):
                if new_zoom_level > level:
                    insert_index = i + 1
                else:
                    break
            view_toolbar.zoom_combo.insertItem(insert_index, new_zoom_percentage_str)

        view_toolbar.zoom_combo.setCurrentText(new_zoom_percentage_str)
        view_toolbar.zoom_combo.blockSignals(False)

        # --- Update Menu ---
        self.view_menu.zoom_action_group.blockSignals(True)
        found_in_menu = False
        for action in self.view_menu.zoom_actions:
            if action.text() == new_zoom_percentage_str:
                action.setChecked(True)
                found_in_menu = True
                break
        
        if not found_in_menu:
            self.view_menu.zoom_action_group.setExclusive(False)
            for action in self.view_menu.zoom_actions:
                action.setChecked(False)
            self.view_menu.zoom_action_group.setExclusive(True)
        self.view_menu.zoom_action_group.blockSignals(False)

    def undo_active_widget(self):
        widget = self.get_active_screen_widget()
        if widget:
            self.edit_service.undo(widget)

    def redo_active_widget(self):
        widget = self.get_active_screen_widget()
        if widget:
            self.edit_service.redo(widget)

    def cut_active_widget(self):
        widget = self.get_active_screen_widget()
        if widget:
            self.edit_service.cut(widget)

    def copy_active_widget(self):
        widget = self.get_active_screen_widget()
        if widget:
            self.edit_service.copy(widget)

    def paste_active_widget(self):
        widget = self.get_active_screen_widget()
        if widget:
            self.edit_service.paste(widget)
            
    def delete_in_active_widget(self):
        widget = self.get_active_screen_widget()
        if hasattr(widget, 'delete_selection'):
             widget.delete_selection()
        elif hasattr(widget, 'textCursor'):
            widget.textCursor().removeSelectedText()

    def select_all_in_active_widget(self):
        widget = self.get_active_screen_widget()
        if hasattr(widget, 'selectAll'):
            widget.selectAll()

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

    def set_dock_widget_visibility(self, dock_name, visible):
        """
        Acts as the central controller for dock widget visibility.
        Updates the dock, menu checkbox, and toolbar action.
        """
        dock = self.dock_factory.get_dock(dock_name)
        if not dock:
            return

        # 1. Update the dock widget's visibility
        if visible:
            dock.show()
            dock.raise_()
        else:
            dock.hide()

        # 2. Update the menu checkbox state
        for action in self.view_menu.docking_window_menu.actions():
            if action.text().lower().replace(' ', '_') == dock_name:
                checkbox = action.defaultWidget().findChild(QCheckBox)
                if checkbox and checkbox.isChecked() != visible:
                    checkbox.blockSignals(True)
                    checkbox.setChecked(visible)
                    checkbox.blockSignals(False)
                break
        
        # 3. Update the toolbar action state
        toolbar = self.toolbars.get("Window Display")
        if toolbar:
            toolbar_action = toolbar.findChild(QAction, f"toggle_{dock_name}")
            if toolbar_action and toolbar_action.isChecked() != visible:
                toolbar_action.blockSignals(True)
                toolbar_action.setChecked(visible)
                toolbar_action.blockSignals(False)

    def toggle_toolbar(self, checked, name):
        """Shows or hides the toolbar with the given name."""
        if name in self.toolbars:
            self.toolbars[name].setVisible(checked)

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

    def _restore_ui_settings(self):
        """Restores various UI settings from the settings service."""
        view_settings = self.settings_service.get_view_settings()
        view_toolbar = self.toolbars.get("View")

        if view_toolbar:
            # Restore object snap state from settings
            object_snap_checked = view_settings.get("object_snap", True)
            self.view_menu.object_snap_checkbox.setChecked(object_snap_checked)

            # Restore snap distance from settings
            snap_distance = view_settings.get("snap_distance", "10")
            view_toolbar.snap_combo.setCurrentText(snap_distance)

            # Restore state number from settings
            state_number = view_settings.get("state_number", 0)
            if 0 <= state_number < view_toolbar.max_states:
                view_toolbar.current_state = state_number
                view_toolbar.update_state_ui()

    def _sync_checkboxes_to_widget_visibility(self):
        """
        After restoring state, syncs the visibility checkboxes in the View menu
        to match the actual visibility of toolbars and dock widgets.
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

        # Sync dock widget checkboxes and toolbar buttons
        for action in self.view_menu.docking_window_menu.actions():
            dock_name = action.text().lower().replace(' ', '_')
            is_visible = docks_visibility.get(dock_name, True)
            # This will update the dock, the menu checkbox, and the toolbar button
            self.set_dock_widget_visibility(dock_name, is_visible)


    def closeEvent(self, event):
        """
        Handles the window's close event. Overridden to save settings.
        
        Args:
            event (QCloseEvent): The close event.
        """
        if self.prompt_to_save():
            self.settings_service.save_settings(self)
            event.accept()
        else:
            event.ignore()
