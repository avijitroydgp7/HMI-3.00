"services/edit_service.py"
from PySide6.QtWidgets import QApplication

class EditService:
    """
    A service class to manage clipboard operations (cut, copy, paste)
    and history for undo/redo functionality. This service is designed
    as a singleton to ensure a single state across the application.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EditService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initializes the EditService.
        """
        if self._initialized:
            return
        self._initialized = True
        
        self.text_clipboard = QApplication.clipboard()
        self._custom_clipboard_data = None  # For custom app data like screens
        self._undo_stack = []
        self._redo_stack = []

    def copy_custom_data(self, data):
        """Copies custom application data to the internal clipboard."""
        self._custom_clipboard_data = data

    def get_custom_data(self):
        """Gets custom data from the internal clipboard."""
        return self._custom_clipboard_data

    def has_custom_data(self):
        """Checks if there is custom data on the internal clipboard."""
        return self._custom_clipboard_data is not None

    def cut(self, widget):
        """
        Performs a cut operation on the given widget.
        For text-based widgets, this cuts the selected text.
        """
        if hasattr(widget, 'cut'):
            # This will also place the text on the system clipboard
            widget.cut()
            # In a real application, you would add a command to the undo stack here
            # For example: self.add_command(CutCommand(widget))
            print("Cut action performed.")

    def copy(self, widget):
        """
        Performs a copy operation on the given widget.
        For text-based widgets, this copies the selected text.
        """
        if hasattr(widget, 'copy'):
            # This places the text on the system clipboard
            widget.copy()
            print("Copy action performed.")

    def paste(self, widget):
        """
        Performs a paste operation on the given widget.
        For text-based widgets, this pastes text from the clipboard.
        """
        if hasattr(widget, 'paste'):
            # This pastes text from the system clipboard
            widget.paste()
            # In a real application, you would add a command to the undo stack here
            # For example: self.add_command(PasteCommand(widget))
            print("Paste action performed.")

    def undo(self, widget):
        """
        Performs an undo operation on the given widget.
        """
        if hasattr(widget, 'undo'):
            widget.undo()
            print("Undo action performed.")


    def redo(self, widget):
        """
        Performs a redo operation on the given widget.
        """
        if hasattr(widget, 'redo'):
            widget.redo()
            print("Redo action performed.")

    # In a more complex application with custom objects, you would implement
    # a command pattern and manage the undo/redo stacks like this:
    #
    # def add_command(self, command):
    #     self._undo_stack.append(command)
    #     self._redo_stack.clear() # Clear redo stack when a new action is performed
    #
    # def undo(self):
    #     if self._undo_stack:
    #         command = self._undo_stack.pop()
    #         command.undo()
    #         self._redo_stack.append(command)
    #
    # def redo(self):
    #     if self._redo_stack:
    #         command = self._redo_stack.pop()
    #         command.execute()
    #         self._undo_stack.append(command)
