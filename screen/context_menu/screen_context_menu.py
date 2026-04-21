from PySide6.QtWidgets import QMenu

from screen.base.base_graphic_object import BaseGraphicObject


class ScreenContextMenu:
    """Build and show the canvas context menu."""

    def __init__(self, canvas, target_item=None, global_pos=None):
        self.canvas = canvas
        self.target_item = target_item if isinstance(target_item, BaseGraphicObject) else None
        self.global_pos = global_pos
        self.menu = QMenu(canvas)

    def _populate(self):
        can_edit_selection = bool(self.target_item) or any(
            isinstance(item, BaseGraphicObject) for item in self.canvas.scene.selectedItems()
        )

        if can_edit_selection:
            self.menu.addAction("Cut", self.canvas.cut)
            self.menu.addAction("Copy", self.canvas.copy)
            self.menu.addAction("Duplicate", self.canvas.duplicate)
            self.menu.addSeparator()
            self.menu.addAction("Delete", self.canvas.delete)
            self.menu.addSeparator()

        self.menu.addAction("Paste", self.canvas.paste)
        self.menu.addAction("Select All", self.canvas.selectAll)

    def show(self):
        """Show menu and return True when menu was executed."""
        if self.global_pos is None:
            return False

        self._populate()
        self.menu.exec(self.global_pos)
        return True
