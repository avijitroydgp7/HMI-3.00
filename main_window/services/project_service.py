"main_window/services/project_service.py"
import json
import os
from PyQt6.QtWidgets import QMessageBox

class ProjectService:
    """
    A service class to manage project-related data and operations.
    """
    def __init__(self):
        self.project_data = {}
        self.file_path = None
        self.is_saved = True

    def new_project(self):
        """Resets the project to a new, unsaved state."""
        self.project_data = {}
        self.file_path = None
        self.is_saved = False

    def load_project(self, file_path):
        """Loads a project from a file."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Project file not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.file_path = file_path
            self.project_data = data.get('project_data', {})
            self.is_saved = True

            return True, "Project loaded successfully"

        except FileNotFoundError as e:
            return False, str(e)
        except json.JSONDecodeError as e:
            return False, f"Invalid project file format: {str(e)}"
        except Exception as e:
            return False, f"Error loading project: {str(e)}"

    def save_project(self, file_path=None):
        """Saves the project to a file."""
        try:
            if file_path:
                self.file_path = file_path

            if not self.file_path:
                return False, "No file path specified"

            # Ensure directory exists
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

            # Prepare data to save
            data_to_save = {
                'project_data': self.project_data,
                'file_path': self.file_path,
                'version': '1.0'
            }

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data_to_save, file, indent=2, ensure_ascii=False)

            self.is_saved = True
            return True, "Project saved successfully"

        except PermissionError:
            return False, "Permission denied. Cannot save to this location."
        except OSError as e:
            return False, f"File system error: {str(e)}"
        except Exception as e:
            return False, f"Error saving project: {str(e)}"

    def mark_as_unsaved(self):
        """Marks the current project as having unsaved changes."""
        if self.is_saved:
            self.is_saved = False
