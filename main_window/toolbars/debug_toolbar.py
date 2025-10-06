# main_window\toolbars\debug_toolbar.py
from PyQt6.QtWidgets import QToolBar

class DebugToolbar(QToolBar):
    """
    A blank toolbar that can be used for debugging purposes.
    """
    def __init__(self, main_window):
        super().__init__("Debug", main_window)
        self.main_window = main_window
        # This toolbar is intentionally left blank for development and debugging.
