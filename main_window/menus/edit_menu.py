from PyQt6.QtGui import QAction
import qtawesome as qta

class EditMenu:
    """
    Creates the 'Edit' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        edit_menu = menu_bar.addMenu("&Edit")

        # Icons
        undo_icon = qta.icon('fa5s.undo', options=[{'color': '#4285f4'}])
        redo_icon = qta.icon('fa5s.redo', options=[{'color': '#4285f4'}])
        cut_icon = qta.icon('fa5s.cut', options=[{'color': '#5f6368'}])
        copy_icon = qta.icon('fa5.copy', 'fa5s.copy', options=[{'color': '#bbdefb', 'offset': (0.1, -0.1)}, {'color': '#4285f4'}])
        paste_icon = qta.icon('fa5s.clipboard', 'fa5s.file-alt', options=[{'color': '#5f6368'}, {'color': 'white', 'scale_factor': 0.7}])
        duplicate_icon = qta.icon('fa5.clone', options=[{'color': '#4285f4'}])
        delete_icon = qta.icon('fa5s.trash-alt', options=[{'color': '#ea4335'}])
        consecutive_copy_icon = qta.icon('fa5s.layer-group', options=[{'color': '#4285f4'}])
        select_all_icon = qta.icon('fa5s.border-all', options=[{'color': '#5f6368'}])
        
        # Actions
        undo_action = QAction(undo_icon,"Undo", main_window)
        redo_action = QAction(redo_icon,"Redo", main_window)
        cut_action = QAction(cut_icon,"Cut", main_window)
        copy_action = QAction(copy_icon,"Copy", main_window)
        paste_action = QAction(paste_icon,"Paste", main_window)
        duplicate_action = QAction(duplicate_icon,"Duplicate", main_window)
        consecutive_copy_action = QAction(consecutive_copy_icon, "Consecutive Copy", main_window)
        select_all_action = QAction(select_all_icon, "Select All", main_window)
        delete_action = QAction(delete_icon,"Delete", main_window)
        
        undo_action.setShortcut("Ctrl+Z")
        redo_action.setShortcut("Ctrl+Y")
        cut_action.setShortcut("Ctrl+X")
        copy_action.setShortcut("Ctrl+C")
        paste_action.setShortcut("Ctrl+V")
        duplicate_action.setShortcut("Ctrl+D")
        consecutive_copy_action.setShortcut("Ctrl+Shift+C")
        select_all_action.setShortcut("Ctrl+A")
        delete_action.setShortcut("Del")

        # Add actions to the Edit menu
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(duplicate_action)
        edit_menu.addAction(consecutive_copy_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)
        edit_menu.addAction(delete_action)
        edit_menu.addSeparator()

        # Stacking Order Submenu
        stacking_order_icon = qta.icon('fa5s.sort-amount-up', options=[{'color': '#4285f4'}])
        stacking_order_menu = edit_menu.addMenu(stacking_order_icon, "Stacking Order")
        move_front_layer_icon = qta.icon('mdi.arrange-bring-to-front', 'mdi6.arrange-bring-to-front', options=[{'color': '#4285f4'}, {'color': '#9aa0a6'}])
        move_back_layer_icon = qta.icon('mdi.arrange-send-to-back', 'mdi6.arrange-send-to-back', options=[{'color': '#4285f4'}, {'color': '#9aa0a6'}])
        move_to_front_icon = qta.icon('mdi.vector-arrange-above', 'mdi6.vector-arrange-above', options=[{'color': '#34a853'}, {'color': '#9aa0a6'}])
        move_to_back_icon = qta.icon('mdi.vector-arrange-below', 'mdi6.vector-arrange-below', options=[{'color': '#ea4335'}, {'color': '#9aa0a6'}])
        stacking_order_menu.addAction(QAction(move_front_layer_icon, "Move Front Layer", main_window))
        stacking_order_menu.addAction(QAction(move_back_layer_icon, "Move Back Layer", main_window))
        stacking_order_menu.addAction(QAction(move_to_front_icon, "Move to Front", main_window))
        stacking_order_menu.addAction(QAction(move_to_back_icon, "Move to Back", main_window))

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
        align_menu.addAction(QAction(align_left_icon, "Left", main_window))
        align_menu.addAction(QAction(align_center_icon, "Center", main_window))
        align_menu.addAction(QAction(align_right_icon, "Right", main_window))
        align_menu.addSeparator()
        align_menu.addAction(QAction(align_top_icon, "Top", main_window))
        align_menu.addAction(QAction(align_middle_icon, "Middle", main_window))
        align_menu.addAction(QAction(align_bottom_icon, "Bottom", main_window))
        align_menu.addSeparator()
        align_menu.addAction(QAction(dist_horz_icon, "Distribute Horizontal", main_window))
        align_menu.addAction(QAction(dist_vert_icon, "Distribute Vertical", main_window))

        # Wrap Action
        wrap_icon = qta.icon('fa5s.compress-arrows-alt', options=[{'color': '#4285f4'}])
        edit_menu.addAction(QAction(wrap_icon, "Wrap", main_window))
        
        # Flip Submenu
        flip_icon = qta.icon('fa5s.exchange-alt', options=[{'color': '#4285f4'}])
        flip_menu = edit_menu.addMenu(flip_icon, "Flip")
        flip_vert_icon = qta.icon('mdi6.flip-vertical', options=[{'color':'#5f6368'}])
        flip_horz_icon = qta.icon('mdi6.flip-horizontal', options=[{'color':'#5f6368'}])
        rotate_left_icon = qta.icon('fa5s.undo', options=[{'color':'#4285f4'}])
        rotate_right_icon = qta.icon('fa5s.redo', options=[{'color':'#4285f4'}])
        flip_menu.addAction(QAction(flip_vert_icon, "Vertical", main_window))
        flip_menu.addAction(QAction(flip_horz_icon, "Horizontal", main_window))
        flip_menu.addAction(QAction(rotate_left_icon, "Left", main_window))
        flip_menu.addAction(QAction(rotate_right_icon, "Right", main_window))

