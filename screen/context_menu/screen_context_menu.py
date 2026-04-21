from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Qt

from main_window.services.icon_service import IconService
from screen.base.base_graphic_object import BaseGraphicObject
from services.edit_service import ClipboardDataType


class ScreenContextMenu:
    """Build and show the canvas context menu."""

    def __init__(self, canvas, target_item=None, global_pos=None):
        self.canvas = canvas
        self.target_item = target_item if isinstance(target_item, BaseGraphicObject) else None
        self.global_pos = global_pos
        self.menu = QMenu(canvas)

    def _selected_graphic_objects(self):
        selected_items = [
            item for item in self.canvas.scene.selectedItems() if isinstance(item, BaseGraphicObject)
        ]
        if self.target_item and self.target_item not in selected_items:
            selected_items.append(self.target_item)
        return selected_items

    def _populate(self):
        selected_graphic_objects = self._selected_graphic_objects()
        selected_count = len(selected_graphic_objects)
        has_selection = selected_count > 0
        can_group = selected_count >= 2
        can_ungroup = any(
            (item.data(Qt.ItemDataRole.UserRole) or {}).get('group_id')
            for item in selected_graphic_objects
        )
        can_align = selected_count >= 2
        can_distribute = selected_count >= 3

        clipboard_type = self.canvas.edit_service.get_clipboard_type()
        can_paste_canvas_items = clipboard_type == ClipboardDataType.CANVAS_ITEMS

        cut_action = QAction(IconService.get_icon('edit-cut'), "Cut", self.menu)
        cut_action.triggered.connect(self.canvas.cut)
        cut_action.setEnabled(has_selection)
        self.menu.addAction(cut_action)

        copy_action = QAction(IconService.get_icon('edit-copy'), "Copy", self.menu)
        copy_action.triggered.connect(self.canvas.copy)
        copy_action.setEnabled(has_selection)
        self.menu.addAction(copy_action)

        paste_action = QAction(IconService.get_icon('edit-paste'), "Paste", self.menu)
        paste_action.triggered.connect(self.canvas.paste)
        paste_action.setEnabled(can_paste_canvas_items)
        self.menu.addAction(paste_action)

        duplicate_action = QAction(IconService.get_icon('edit-duplicate'), "Duplicate", self.menu)
        duplicate_action.triggered.connect(self.canvas.duplicate)
        duplicate_action.setEnabled(has_selection)
        self.menu.addAction(duplicate_action)

        delete_action = QAction(IconService.get_icon('edit-delete'), "Delete", self.menu)
        delete_action.triggered.connect(self.canvas.delete)
        delete_action.setEnabled(has_selection)
        self.menu.addAction(delete_action)

        self.menu.addSeparator()

        stacking_order_menu = self.menu.addMenu(IconService.get_icon('stacking-order'), "Stacking Order")

        move_front_layer_action = QAction(IconService.get_icon('move-front-layer'), "Move Front Layer", self.menu)
        move_front_layer_action.triggered.connect(self.canvas.move_front_layer)
        move_front_layer_action.setEnabled(has_selection)
        stacking_order_menu.addAction(move_front_layer_action)

        move_back_layer_action = QAction(IconService.get_icon('move-back-layer'), "Move Back Layer", self.menu)
        move_back_layer_action.triggered.connect(self.canvas.move_back_layer)
        move_back_layer_action.setEnabled(has_selection)
        stacking_order_menu.addAction(move_back_layer_action)

        move_to_front_action = QAction(IconService.get_icon('move-to-front'), "Move to Front", self.menu)
        move_to_front_action.triggered.connect(self.canvas.move_to_front)
        move_to_front_action.setEnabled(has_selection)
        stacking_order_menu.addAction(move_to_front_action)

        move_to_back_action = QAction(IconService.get_icon('move-to-back'), "Move to Back", self.menu)
        move_to_back_action.triggered.connect(self.canvas.move_to_back)
        move_to_back_action.setEnabled(has_selection)
        stacking_order_menu.addAction(move_to_back_action)

        flip_menu = self.menu.addMenu(IconService.get_icon('flip'), "Flip")

        flip_vertical_action = QAction(IconService.get_icon('flip-vertical'), "Vertical", self.menu)
        flip_vertical_action.triggered.connect(lambda: self.canvas.flip_items('vertical'))
        flip_vertical_action.setEnabled(has_selection)
        flip_menu.addAction(flip_vertical_action)

        flip_horizontal_action = QAction(IconService.get_icon('flip-horizontal'), "Horizontal", self.menu)
        flip_horizontal_action.triggered.connect(lambda: self.canvas.flip_items('horizontal'))
        flip_horizontal_action.setEnabled(has_selection)
        flip_menu.addAction(flip_horizontal_action)

        rotate_left_action = QAction(IconService.get_icon('rotate-left'), "Left", self.menu)
        rotate_left_action.triggered.connect(lambda: self.canvas.rotate_items(-90))
        rotate_left_action.setEnabled(has_selection)
        flip_menu.addAction(rotate_left_action)

        rotate_right_action = QAction(IconService.get_icon('rotate-right'), "Right", self.menu)
        rotate_right_action.triggered.connect(lambda: self.canvas.rotate_items(90))
        rotate_right_action.setEnabled(has_selection)
        flip_menu.addAction(rotate_right_action)

        align_menu = self.menu.addMenu(IconService.get_icon('align-center'), "Align")

        align_left_action = QAction(IconService.get_icon('align-left'), "Left", self.menu)
        align_left_action.triggered.connect(lambda: self.canvas.align_items('left'))
        align_left_action.setEnabled(can_align)
        align_menu.addAction(align_left_action)

        align_center_action = QAction(IconService.get_icon('align-horizontal-center'), "Center", self.menu)
        align_center_action.triggered.connect(lambda: self.canvas.align_items('center'))
        align_center_action.setEnabled(can_align)
        align_menu.addAction(align_center_action)

        align_right_action = QAction(IconService.get_icon('align-right'), "Right", self.menu)
        align_right_action.triggered.connect(lambda: self.canvas.align_items('right'))
        align_right_action.setEnabled(can_align)
        align_menu.addAction(align_right_action)

        align_menu.addSeparator()

        align_top_action = QAction(IconService.get_icon('align-top'), "Top", self.menu)
        align_top_action.triggered.connect(lambda: self.canvas.align_items('top'))
        align_top_action.setEnabled(can_align)
        align_menu.addAction(align_top_action)

        align_middle_action = QAction(IconService.get_icon('align-middle'), "Middle", self.menu)
        align_middle_action.triggered.connect(lambda: self.canvas.align_items('middle'))
        align_middle_action.setEnabled(can_align)
        align_menu.addAction(align_middle_action)

        align_bottom_action = QAction(IconService.get_icon('align-bottom'), "Bottom", self.menu)
        align_bottom_action.triggered.connect(lambda: self.canvas.align_items('bottom'))
        align_bottom_action.setEnabled(can_align)
        align_menu.addAction(align_bottom_action)

        align_menu.addSeparator()

        dist_horz_action = QAction(IconService.get_icon('distribute-horizontal'), "Distribute Horizontal", self.menu)
        dist_horz_action.triggered.connect(lambda: self.canvas.distribute_items('horizontal'))
        dist_horz_action.setEnabled(can_distribute)
        align_menu.addAction(dist_horz_action)

        dist_vert_action = QAction(IconService.get_icon('distribute-vertical'), "Distribute Vertical", self.menu)
        dist_vert_action.triggered.connect(lambda: self.canvas.distribute_items('vertical'))
        dist_vert_action.setEnabled(can_distribute)
        align_menu.addAction(dist_vert_action)

        self.menu.addSeparator()

        group_action = QAction(IconService.get_icon('edit-group'), "Group", self.menu)
        if hasattr(self.canvas, 'group_selected_items'):
            group_action.triggered.connect(self.canvas.group_selected_items)
        group_action.setEnabled(can_group and hasattr(self.canvas, 'group_selected_items'))
        self.menu.addAction(group_action)

        ungroup_action = QAction(IconService.get_icon('edit-ungroup'), "Ungroup", self.menu)
        if hasattr(self.canvas, 'ungroup_selected_items'):
            ungroup_action.triggered.connect(self.canvas.ungroup_selected_items)
        ungroup_action.setEnabled(can_ungroup and hasattr(self.canvas, 'ungroup_selected_items'))
        self.menu.addAction(ungroup_action)

        self.menu.addSeparator()
        self.menu.addAction("Select All", self.canvas.selectAll)

    def show(self):
        """Show menu and return True when menu was executed."""
        if self.global_pos is None:
            return False

        self._populate()
        self.menu.exec(self.global_pos)
        return True
