# project/tag/tag_table.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class TagTable(QWidget):
    """
    A widget to display the tag table.
    This is currently a placeholder and will be developed further.
    """
    def __init__(self, tag_data, parent=None):
        """
        Initializes the TagTable widget.

        Args:
            tag_data (dict): A dictionary containing the tag's data.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.tag_data = tag_data
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title = f"Tag Table: {self.tag_data.get('number')} - {self.tag_data.get('name')}"
        self.label = QLabel(title)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        
        layout.addWidget(self.label)
        layout.addWidget(QLabel("This is the blank tag table view. The full table will be implemented here."))
