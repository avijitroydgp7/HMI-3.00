# project/comment/comment_table.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class CommentTable(QWidget):
    """
    A widget to display the comment table.
    This is currently a placeholder and will be developed further.
    """
    def __init__(self, comment_data, parent=None):
        """
        Initializes the CommentTable widget.

        Args:
            comment_data (dict): A dictionary containing the comment's data.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.comment_data = comment_data
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title = f"Comment Table: {self.comment_data.get('number')} - {self.comment_data.get('name')}"
        self.label = QLabel(title)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        
        layout.addWidget(self.label)
        layout.addWidget(QLabel("This is the blank comment table view. The full table will be implemented here."))
