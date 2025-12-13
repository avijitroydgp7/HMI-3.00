# main_window\services\view_service.py
from PySide6.QtCore import QObject, Signal

class ViewService(QObject):
    """
    A service to manage view-related states like snapping and grid settings.
    """
    snap_changed = Signal(bool)
    grid_size_changed = Signal(int)
    snapping_mode_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._snap_enabled = True
        self._grid_size = 8
        self._snapping_mode = 'object'  # Default to object snapping

    @property
    def snap_enabled(self):
        return self._snap_enabled

    @snap_enabled.setter
    def snap_enabled(self, value: bool):
        if self._snap_enabled != value:
            self._snap_enabled = value
            self.snap_changed.emit(value)

    @property
    def grid_size(self):
        return self._grid_size

    @grid_size.setter
    def grid_size(self, value: int):
        if self._grid_size != value and value > 0:
            self._grid_size = value
            self.grid_size_changed.emit(value)

    @property
    def snapping_mode(self):
        return self._snapping_mode

    @snapping_mode.setter
    def snapping_mode(self, value: str):
        if self._snapping_mode != value:
            self._snapping_mode = value
            self.snapping_mode_changed.emit(value)
