# main_window\toolbars\alignment_toolbar.py
from PyQt6.QtWidgets import QToolBar

class AlignmentToolbar(QToolBar):
    def __init__(self, main_window, edit_menu):
        super().__init__("Alignment", main_window)
        self.main_window = main_window
        
        self.addAction(edit_menu.align_left_action)
        self.addAction(edit_menu.align_center_action)
        self.addAction(edit_menu.align_right_action)
        self.addSeparator()
        self.addAction(edit_menu.align_top_action)
        self.addAction(edit_menu.align_middle_action)
        self.addAction(edit_menu.align_bottom_action)
        self.addSeparator()
        self.addAction(edit_menu.dist_horz_action)
        self.addAction(edit_menu.dist_vert_action)
