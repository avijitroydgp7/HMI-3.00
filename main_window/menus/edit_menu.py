from PyQt6.QtGui import QAction
import qtawesome as qta

class EditMenu:
    """
    Creates the 'Edit' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        self.main_window = main_window
        edit_menu = menu_bar.addMenu("&Edit")

        # Icons
        undo_icon = qta.icon('fa5s.undo', options=[{'color': '#4285f4'}])
        redo_icon = qta.icon('fa5s.redo', options=[{'color': '#4285f4'}])
        cut_icon = qta.icon('fa5s.cut', options=[{'color': '#5f6368'}])
        copy_icon = qta.icon('fa5.copy', options=[{'color': '#bbdefb'}])
        paste_icon = qta.icon('fa5s.clipboard', options=[{'color': '#5f6368'}])
        duplicate_icon = qta.icon('fa5.clone', options=[{'color': '#4285f4'}])
        delete_icon = qta.icon('fa5s.trash-alt', options=[{'color': '#ea4335'}])
        consecutive_copy_icon = qta.icon('fa5s.layer-group', options=[{'color': '#4285f4'}])
        select_all_icon = qta.icon('fa5s.border-all', options=[{'color': '#5f6368'}])
        
        # Actions
        self.undo_action = QAction(undo_icon,"Undo", self.main_window)
        self.redo_action = QAction(redo_icon,"Redo", self.main_window)
        self.cut_action = QAction(cut_icon,"Cut", self.main_window)
        self.copy_action = QAction(copy_icon,"Copy", self.main_window)
        self.paste_action = QAction(paste_icon,"Paste", self.main_window)
        self.duplicate_action = QAction(duplicate_icon,"Duplicate", self.main_window)
        self.consecutive_copy_action = QAction(consecutive_copy_icon, "Consecutive Copy", self.main_window)
        self.select_all_action = QAction(select_all_icon, "Select All", self.main_window)
        self.delete_action = QAction(delete_icon,"Delete", self.main_window)
        
        self.undo_action.setShortcut("Ctrl+Z")
        self.redo_action.setShortcut("Ctrl+Y")
        self.cut_action.setShortcut("Ctrl+X")
        self.copy_action.setShortcut("Ctrl+C")
        self.paste_action.setShortcut("Ctrl+V")
        self.duplicate_action.setShortcut("Ctrl+D")
        self.consecutive_copy_action.setShortcut("Ctrl+Shift+C")
        self.select_all_action.setShortcut("Ctrl+A")
        self.delete_action.setShortcut("Del")

        # Add actions to the Edit menu
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.duplicate_action)
        edit_menu.addAction(self.consecutive_copy_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)
        edit_menu.addAction(self.delete_action)
        edit_menu.addSeparator()

        # Stacking Order Submenu
        stacking_order_icon = qta.icon('fa5s.sort-amount-up', options=[{'color': '#4285f4'}])
        stacking_order_menu = edit_menu.addMenu(stacking_order_icon, "Stacking Order")
        move_front_layer_icon = qta.icon('mdi.arrange-bring-to-front', options=[{'color': '#4285f4'}])
        move_back_layer_icon = qta.icon('mdi.arrange-send-to-back', options=[{'color': '#4285f4'}])
        move_to_front_icon = qta.icon('mdi.vector-arrange-above', options=[{'color': '#34a853'}])
        move_to_back_icon = qta.icon('mdi.vector-arrange-below', options=[{'color': '#ea4335'}])
        self.move_front_layer_action = QAction(move_front_layer_icon, "Move Front Layer", self.main_window)
        stacking_order_menu.addAction(self.move_front_layer_action)
        self.move_back_layer_action = QAction(move_back_layer_icon, "Move Back Layer", self.main_window)
        stacking_order_menu.addAction(self.move_back_layer_action)
        self.move_to_front_action = QAction(move_to_front_icon, "Move to Front", self.main_window)
        stacking_order_menu.addAction(self.move_to_front_action)
        self.move_to_back_action = QAction(move_to_back_icon, "Move to Back", self.main_window)
        stacking_order_menu.addAction(self.move_to_back_action)

        # Align Submenu
        align_icon = qta.icon('fa5s.align-center', options=[{'color': '#4285f4'}])
        align_menu = edit_menu.addMenu(align_icon, "Align")
        align_left_icon = qta.icon('mdi.align-horizontal-left', options=[{'color':'#5f6368'}])
        align_center_icon = qta.icon('mdi.align-horizontal-center', options=[{'color':'#5f6368'}])
        align_right_icon = qta.icon('mdi.align-horizontal-right', options=[{'color':'#5f6368'}])
        align_top_icon = qta.icon('mdi.align-vertical-top', options=[{'color':'#5f6368'}])
        align_middle_icon = qta.icon('mdi.align-vertical-center', options=[{'color':'#5f6368'}])
        align_bottom_icon = qta.icon('mdi.align-vertical-bottom', options=[{'color':'#5f6368'}])
        dist_horz_icon = qta.icon('mdi6.align-horizontal-distribute', options=[{'color':'#4285f4'}])
        dist_vert_icon = qta.icon('mdi6.align-vertical-distribute', options=[{'color':'#4285f4'}])
        self.align_left_action = QAction(align_left_icon, "Left", self.main_window)
        align_menu.addAction(self.align_left_action)
        self.align_center_action = QAction(align_center_icon, "Center", self.main_window)
        align_menu.addAction(self.align_center_action)
        self.align_right_action = QAction(align_right_icon, "Right", self.main_window)
        align_menu.addAction(self.align_right_action)
        align_menu.addSeparator()
        self.align_top_action = QAction(align_top_icon, "Top", self.main_window)
        align_menu.addAction(self.align_top_action)
        self.align_middle_action = QAction(align_middle_icon, "Middle", self.main_window)
        align_menu.addAction(self.align_middle_action)
        self.align_bottom_action = QAction(align_bottom_icon, "Bottom", self.main_window)
        align_menu.addAction(self.align_bottom_action)
        align_menu.addSeparator()
        self.dist_horz_action = QAction(dist_horz_icon, "Distribute Horizontal", self.main_window)
        align_menu.addAction(self.dist_horz_action)
        self.dist_vert_action = QAction(dist_vert_icon, "Distribute Vertical", self.main_window)
        align_menu.addAction(self.dist_vert_action)

        # Wrap Action
        wrap_icon = qta.icon('fa5s.compress-arrows-alt', options=[{'color': '#4285f4'}])
        self.wrap_action = QAction(wrap_icon, "Wrap", self.main_window)
        edit_menu.addAction(self.wrap_action)
        
        # Flip Submenu
        flip_icon = qta.icon('fa5s.exchange-alt', options=[{'color': '#4285f4'}])
        flip_menu = edit_menu.addMenu(flip_icon, "Flip")
        flip_vert_icon = qta.icon('mdi6.flip-vertical', options=[{'color':'#5f6368'}])
        flip_horz_icon = qta.icon('mdi6.flip-horizontal', options=[{'color':'#5f6368'}])
        rotate_left_icon = qta.icon('fa5s.undo', options=[{'color':'#4285f4'}])
        rotate_right_icon = qta.icon('fa5s.redo', options=[{'color':'#4285f4'}])
        self.flip_vert_action = QAction(flip_vert_icon, "Vertical", self.main_window)
        flip_menu.addAction(self.flip_vert_action)
        self.flip_horz_action = QAction(flip_horz_icon, "Horizontal", self.main_window)
        flip_menu.addAction(self.flip_horz_action)
        self.rotate_left_action = QAction(rotate_left_icon, "Left", self.main_window)
        flip_menu.addAction(self.rotate_left_action)
        self.rotate_right_action = QAction(rotate_right_icon, "Right", self.main_window)
        flip_menu.addAction(self.rotate_right_action)
