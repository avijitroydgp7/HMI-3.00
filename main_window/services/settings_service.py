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
            }
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self, main_window):
        """
        Loads the main window's geometry and state from the settings file.

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

        if 'main_window' in settings and 'geometry' in settings['main_window'] and 'state' in settings['main_window']:
            geometry_data = settings['main_window']['geometry']
            state_data = settings['main_window']['state']
            
            # Restore geometry and state if the data is valid
            if geometry_data:
                main_window.restoreGeometry(QByteArray.fromBase64(geometry_data.encode('utf-8')))
            if state_data:
                main_window.restoreState(QByteArray.fromBase64(state_data.encode('utf-8')))
            
            # After restoring state, update the checkboxes in the View menu to reflect the actual visibility
            self.update_view_menu_checkboxes(main_window)
        else:
            print("Invalid settings format. Using default layout.")

    def update_view_menu_checkboxes(self, main_window):
        """
        Syncs the checked state of the checkboxes in the View menu with the visibility
        of their corresponding docks and toolbars.

        Args:
            main_window (QMainWindow): The main window instance.
        """
        # Update dock visibility checkboxes
        for action in main_window.view_menu.docking_window_menu.actions():
            dock_name = action.text().lower().replace(' ', '_')
            dock = main_window.dock_factory.get_dock(dock_name)
            if dock:
                widget = action.defaultWidget()
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    # Block signals to prevent toggled signal from firing unnecessarily
                    checkbox.blockSignals(True)
                    checkbox.setChecked(dock.isVisible())
                    checkbox.blockSignals(False)
        
        # Update toolbar visibility checkboxes
        for action in main_window.view_menu.tool_bar_menu.actions():
            toolbar_name = action.text()
            if toolbar_name in main_window.toolbars:
                toolbar = main_window.toolbars[toolbar_name]
                widget = action.defaultWidget()
                checkbox = widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.blockSignals(True)
                    checkbox.setChecked(toolbar.isVisible())
                    checkbox.blockSignals(False)
