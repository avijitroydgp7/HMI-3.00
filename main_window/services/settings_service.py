import json
import os
from PyQt6.QtCore import QSettings

class SettingsService:
    """
    Manages loading and saving of application settings from a JSON file.
    This service helps in persisting UI states like window size, position,
    and the state of dock widgets and toolbars across sessions.
    """
    def __init__(self, file_path='settings.json'):
        """
        Initializes the SettingsService.

        Args:
            file_path (str): The path to the settings file.
        """
        self.file_path = file_path
        self.settings = self.load_settings()

    def load_settings(self):
        """
        Loads the settings from the JSON file. If the file doesn't exist,
        it returns a default dictionary.
        """
        if not os.path.exists(self.file_path):
            return {
                "main_window": {
                    "geometry": None,
                    "state": None
                }
            }
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {
                "main_window": {
                    "geometry": None,
                    "state": None
                }
            }

    def save_settings(self, main_window):
        """
        Saves the current state of the main window (geometry and state of toolbars/docks)
        to the JSON file.

        Args:
            main_window (QMainWindow): The main window instance to save settings from.
        """
        self.settings['main_window']['geometry'] = main_window.saveGeometry().data().hex()
        self.settings['main_window']['state'] = main_window.saveState().data().hex()
        
        with open(self.file_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_main_window_settings(self):
        """
        Returns the settings for the main window.
        """
        return self.settings.get('main_window', {})
