# project/comment/comment_table.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QToolBar, QTableWidget
from PyQt6.QtCore import Qt

class CommentTable(QWidget):
    """
    A widget to display and edit the comment table, including a toolbar for common actions.
    """
    def __init__(self, comment_data, main_window, common_menu, parent=None):
        """
        Initializes the CommentTable widget.

        Args:
            comment_data (dict): Data for the comment table.
            main_window (QMainWindow): The main application window.
            common_menu (CommonMenu): The common menu containing shared actions.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.comment_data = comment_data
        self.main_window = main_window
        self.common_menu = common_menu
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create Toolbar
        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)

        # Create Table (Placeholder)
        self.table_widget = QTableWidget(10, 5)  # Example size
        self.table_widget.setHorizontalHeaderLabels([f"Column {i+1}" for i in range(5)])
        layout.addWidget(self.table_widget)

    def _create_toolbar(self):
        """Creates the toolbar and adds actions from the common menu."""
        toolbar = QToolBar("Comment Toolbar")
        toolbar.setIconSize(self.main_window.iconSize())

        toolbar.addAction(self.common_menu.add_column_action)
        toolbar.addAction(self.common_menu.add_row_action)
        toolbar.addAction(self.common_menu.remove_column_action)
        toolbar.addAction(self.common_menu.remove_row_action)
        toolbar.addSeparator()
        toolbar.addAction(self.common_menu.bold_action)
        toolbar.addAction(self.common_menu.italic_action)
        toolbar.addAction(self.common_menu.underline_action)
        toolbar.addAction(self.common_menu.fill_text_action)
        toolbar.addAction(self.common_menu.fill_background_action)

        # Connect actions to placeholder slots
        self.common_menu.add_column_action.triggered.connect(self.add_column)
        self.common_menu.add_row_action.triggered.connect(self.add_row)
        self.common_menu.remove_column_action.triggered.connect(self.remove_column)
        self.common_menu.remove_row_action.triggered.connect(self.remove_row)
        self.common_menu.bold_action.triggered.connect(self.set_bold)
        self.common_menu.italic_action.triggered.connect(self.set_italic)
        self.common_menu.underline_action.triggered.connect(self.set_underline)
        self.common_menu.fill_text_action.triggered.connect(self.fill_text)
        self.common_menu.fill_background_action.triggered.connect(self.fill_background)

        return toolbar

    # --- Placeholder Slots for Toolbar Actions ---
    def add_column(self):
        print(f"Action 'Add Column' triggered for comment: {self.comment_data['name']}")

    def add_row(self):
        print(f"Action 'Add Row' triggered for comment: {self.comment_data['name']}")

    def remove_column(self):
        print(f"Action 'Remove Column' triggered for comment: {self.comment_data['name']}")

    def remove_row(self):
        print(f"Action 'Remove Row' triggered for comment: {self.comment_data['name']}")

    def set_bold(self):
        print(f"Action 'Bold' triggered for comment: {self.comment_data['name']}")

    def set_italic(self):
        print(f"Action 'Italic' triggered for comment: {self.comment_data['name']}")

    def set_underline(self):
        print(f"Action 'Underline' triggered for comment: {self.comment_data['name']}")

    def fill_text(self):
        print(f"Action 'Fill Text' triggered for comment: {self.comment_data['name']}")

    def fill_background(self):
        print(f"Action 'Fill Background' triggered for comment: {self.comment_data['name']}")

