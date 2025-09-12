import json
import os
from PyQt6.QtCore import QByteArray
from PyQt6.QtWidgets import QCheckBox

class SettingsService:
    """
    Manages loading and saving the application's UI settings to a JSON file.
    This includes the main window's geometry and the state of all docks and toolbars.
    """
    def __init__(self, settings_file='settings.json'):
        """
        Initializes the SettingsService.

        Args:
            settings_file (str): The name of the file to store settings in.
                                 It's expected to be in the root directory of the project.
        """
        self.settings_file = settings_file

    def save_settings(self, main_window):
        """
        Saves the main window's geometry and state to the settings file.
        The state includes the positions and visibility of all dock widgets and toolbars.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        settings = {
            'main_window': {
                'geometry': main_window.saveGeometry().toBase64().data().decode('utf-8'),
                'state': main_window.saveState().toBase64().data().decode('utf-8')
            },
            'dock_visibility': {name: dock.isVisible() for name, dock in main_window.dock_factory.docks.items()},
            'toolbar_visibility': {name: toolbar.isVisible() for name, toolbar in main_window.toolbars.items()}
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self, main_window):
        """
        Loads the main window's geometry, state, and visibility settings from the settings file.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        if not os.path.exists(self.settings_file):
            print("Settings file not found. Using default layout.")
            return

        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, TypeError) as e:
            print(f"Could not load settings: {e}. Using default layout.")
            return

        # Restore main window geometry and state first.
        # The visibility of docks/toolbars might be part of this state, but we will
        # explicitly set it from our saved settings for better reliability.
        if 'main_window' in settings:
            geometry_data = settings['main_window'].get('geometry')
            state_data = settings['main_window'].get('state')
            
            if geometry_data:
                main_window.restoreGeometry(QByteArray.fromBase64(geometry_data.encode('utf-8')))
            if state_data:
                main_window.restoreState(QByteArray.fromBase64(state_data.encode('utf-8')))

        # Restore dock visibility by setting the state of the checkboxes in the menu.
        # This is the source of truth and will override any visibility loaded by restoreState.
        if 'dock_visibility' in settings:
            for action in main_window.view_menu.docking_window_menu.actions():
                dock_name = action.text().lower().replace(' ', '_')
                # Default to True if the key is somehow missing for a new dock
                is_visible = settings['dock_visibility'].get(dock_name, True)
                
                widget = action.defaultWidget()
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    # This will trigger the toggled signal, which shows/hides the dock
                    checkbox.setChecked(is_visible)
        
        # Restore toolbar visibility similarly.
        if 'toolbar_visibility' in settings:
            for action in main_window.view_menu.tool_bar_menu.actions():
                toolbar_name = action.text()
                 # Default to True if the key is somehow missing for a new toolbar
                is_visible = settings['toolbar_visibility'].get(toolbar_name, True)

                widget = action.defaultWidget()
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    # This will trigger the toggled signal, which shows/hides the toolbar
                    checkbox.setChecked(is_visible)

