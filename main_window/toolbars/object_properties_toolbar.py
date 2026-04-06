# main_window\toolbars\object_properties_toolbar.py
"""
Object Properties Toolbar
=========================
A floating toolbar for displaying and editing selected object's 
position, size, and rotation angle with live updates.
Supports undo/redo for all property changes.
"""

from PySide6.QtWidgets import (
    QToolBar, QWidget, QHBoxLayout, QLabel, QDoubleSpinBox, 
    QCheckBox, QFrame
)
from PySide6.QtCore import Qt, Signal, QSize, QPointF, QRectF
from ..services.icon_service import IconService
from screen.base.canvas_base_screen import CanvasBaseScreen
from screen.base.base_graphic_object import BaseGraphicObject
from services.undo_commands import TransformItemsCommand, MoveItemsCommand
from styles import stylesheets


class ObjectPropertiesToolbar(QToolBar):
    """
    Toolbar for displaying and editing selected object properties.
    Shows X, Y position, Width, Height, and Angle.
    All values are editable and provide live updates to the canvas.
    Supports undo/redo for all changes.
    """
    
    # Signals emitted when user edits values
    position_edited = Signal(float, float)  # x, y
    size_edited = Signal(float, float)  # width, height
    angle_edited = Signal(float)  # angle
    ASPECT_LOCK_KEY = "lock_aspect_ratio"
    
    def __init__(self, main_window):
        super().__init__("Object Properties", main_window)
        self.main_window = main_window
        self._syncing = False  # Prevent feedback loops during sync
        self._last_width = 100
        self._last_height = 100
        
        # Track initial state for undo
        self._editing_item = None
        self._edit_initial_state = None
        
        self._setup_ui()
        
        # Apply consistent styling
        self.setStyleSheet(stylesheets.get_object_properties_toolbar_stylesheet())
        
    def _setup_ui(self):
        """Setup the toolbar UI components."""
        # Icon size consistent with other toolbars (24x24)
        icon_size = QSize(24, 24)
        
        # Position Section
        pos_widget = QWidget()
        pos_layout = QHBoxLayout(pos_widget)
        pos_layout.setContentsMargins(4, 0, 4, 0)
        pos_layout.setSpacing(4)
        
        # X Position
        x_icon = QLabel()
        x_icon.setPixmap(IconService.get_icon('object-pos').pixmap(icon_size))
        pos_layout.addWidget(x_icon)
        
        x_label = QLabel("X:")
        x_label.setStyleSheet(stylesheets.get_bold_label_stylesheet())
        pos_layout.addWidget(x_label)
        
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-99999.0, 99999.0)
        self.x_spin.setValue(0)
        self.x_spin.setDecimals(0)
        self.x_spin.setFixedWidth(75)
        self.x_spin.setToolTip("X Position (Left)")
        self.x_spin.valueChanged.connect(self._on_position_changed)
        pos_layout.addWidget(self.x_spin)
        
        # Y Position
        y_label = QLabel("Y:")
        y_label.setStyleSheet(stylesheets.get_bold_label_stylesheet())
        pos_layout.addWidget(y_label)
        
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-99999.0, 99999.0)
        self.y_spin.setValue(0)
        self.y_spin.setDecimals(0)
        self.y_spin.setFixedWidth(75)
        self.y_spin.setToolTip("Y Position (Top)")
        self.y_spin.valueChanged.connect(self._on_position_changed)
        pos_layout.addWidget(self.y_spin)
        
        self.addWidget(pos_widget)
        self._add_separator()
        
        # Size Section
        size_widget = QWidget()
        size_layout = QHBoxLayout(size_widget)
        size_layout.setContentsMargins(4, 0, 4, 0)
        size_layout.setSpacing(4)
        
        # Width
        w_icon = QLabel()
        w_icon.setPixmap(IconService.get_icon('object-size').pixmap(icon_size))
        size_layout.addWidget(w_icon)
        
        w_label = QLabel("W:")
        w_label.setStyleSheet(stylesheets.get_bold_label_stylesheet())
        size_layout.addWidget(w_label)
        
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(1, 99999.0)
        self.width_spin.setValue(100)
        self.width_spin.setDecimals(0)
        self.width_spin.setFixedWidth(75)
        self.width_spin.setToolTip("Width")
        self.width_spin.valueChanged.connect(self._on_size_changed)
        size_layout.addWidget(self.width_spin)
        
        # Height
        h_label = QLabel("H:")
        h_label.setStyleSheet(stylesheets.get_bold_label_stylesheet())
        size_layout.addWidget(h_label)
        
        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(1, 99999.0)
        self.height_spin.setValue(100)
        self.height_spin.setDecimals(0)
        self.height_spin.setFixedWidth(75)
        self.height_spin.setToolTip("Height")
        self.height_spin.valueChanged.connect(self._on_size_changed)
        size_layout.addWidget(self.height_spin)
        
        # Lock Aspect Ratio
        self.lock_aspect = QCheckBox()
        self.lock_aspect.setToolTip("Lock Aspect Ratio")
        self.lock_aspect.setIcon(IconService.get_icon('lock'))
        self.lock_aspect.setIconSize(icon_size)
        self.lock_aspect.toggled.connect(self._on_lock_aspect_toggled)
        size_layout.addWidget(self.lock_aspect)
        
        self.addWidget(size_widget)
        self._add_separator()
        
        # Angle Section
        angle_widget = QWidget()
        angle_layout = QHBoxLayout(angle_widget)
        angle_layout.setContentsMargins(4, 0, 4, 0)
        angle_layout.setSpacing(4)
        
        angle_icon = QLabel()
        angle_icon.setPixmap(IconService.get_icon('rotate-right').pixmap(icon_size))
        angle_layout.addWidget(angle_icon)
        
        angle_label = QLabel("∠:")
        angle_label.setStyleSheet(stylesheets.get_bold_label_stylesheet())
        angle_layout.addWidget(angle_label)
        
        self.angle_spin = QDoubleSpinBox()
        self.angle_spin.setRange(-360.0, 360.0)
        self.angle_spin.setValue(0)
        self.angle_spin.setSuffix("°")
        self.angle_spin.setDecimals(1)
        self.angle_spin.setFixedWidth(75)
        self.angle_spin.setToolTip("Rotation Angle")
        self.angle_spin.valueChanged.connect(self._on_angle_changed)
        angle_layout.addWidget(self.angle_spin)
        
        self.addWidget(angle_widget)
        
        # Initially disable all inputs (no selection)
        self._set_enabled(False)
        
    def _add_separator(self):
        """Add a visual separator."""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.addWidget(separator)
        
    def _set_enabled(self, enabled):
        """Enable or disable all input widgets."""
        self.x_spin.setEnabled(enabled)
        self.y_spin.setEnabled(enabled)
        self.width_spin.setEnabled(enabled)
        self.height_spin.setEnabled(enabled)
        self.angle_spin.setEnabled(enabled)
        self.lock_aspect.setEnabled(enabled)
        
    def _on_position_changed(self, value):
        """Handle position spinbox changes."""
        if self._syncing:
            return
        
        x = self.x_spin.value()
        y = self.y_spin.value()
        
        # Apply to active canvas selection
        self._apply_position_to_selection(x, y)
        self.position_edited.emit(x, y)
        
    def _on_size_changed(self, value):
        """Handle size spinbox changes with aspect ratio lock support."""
        if self._syncing:
            return

        active_screen = self.main_window.get_active_screen_widget()
        valid_items = []
        if isinstance(active_screen, CanvasBaseScreen):
            valid_items = [
                item for item in active_screen.scene.selectedItems()
                if isinstance(item, BaseGraphicObject)
            ]
        
        width = self.width_spin.value()
        height = self.height_spin.value()
        maintain_aspect = self.lock_aspect.isChecked() or any(
            self._is_item_aspect_locked(item) for item in valid_items
        )
        
        # Handle aspect ratio lock
        if maintain_aspect:
            sender = self.sender()
            if sender == self.width_spin and self._last_width > 0:
                ratio = self._last_height / self._last_width
                self._syncing = True
                self.height_spin.setValue(width * ratio)
                self._syncing = False
                height = self.height_spin.value()
            elif sender == self.height_spin and self._last_height > 0:
                ratio = self._last_width / self._last_height
                self._syncing = True
                self.width_spin.setValue(height * ratio)
                self._syncing = False
                width = self.width_spin.value()
        
        self._last_width = width
        self._last_height = height
        
        # Apply to active canvas selection
        self._apply_size_to_selection(width, height, maintain_aspect, self.sender())
        self.size_edited.emit(width, height)

    def _on_lock_aspect_toggled(self, checked):
        """Persist lock-aspect state on selected object(s)."""
        if self._syncing:
            return

        active_screen = self.main_window.get_active_screen_widget()
        if not isinstance(active_screen, CanvasBaseScreen):
            return

        valid_items = [
            item for item in active_screen.scene.selectedItems()
            if isinstance(item, BaseGraphicObject)
        ]
        if not valid_items:
            return

        for item in valid_items:
            self._set_item_aspect_locked(item, checked)
        active_screen.save_items()
        
    def _on_angle_changed(self, value):
        """Handle angle spinbox changes."""
        if self._syncing:
            return
        
        # Apply to active canvas selection
        self._apply_angle_to_selection(value)
        self.angle_edited.emit(value)
    
    def _capture_item_state(self, item):
        """Capture current state of an item for undo."""
        rect = self._get_item_rect(item)
        state = {
            'pos': QPointF(item.pos()),
            'rect': QRectF(rect),
            'rotation': item.rotation(),
            'transform_origin': QPointF(item.transformOriginPoint())
        }
        if hasattr(item, 'corner_radii'):
            state['corner_radii'] = item.corner_radii.copy()
        return state

    def _get_item_rect(self, item):
        """Return the geometric rect used for editing (without pen-inflated bounds)."""
        if hasattr(item, 'item') and hasattr(item.item, 'rect'):
            try:
                return QRectF(item.item.rect())
            except Exception:
                pass
        return QRectF(item.boundingRect())

    def _get_item_scene_rect(self, item):
        """Return item rect in scene coordinates (axis-aligned, ignoring rotation)."""
        rect = self._get_item_rect(item)
        return QRectF(
            item.pos().x() + rect.x(),
            item.pos().y() + rect.y(),
            rect.width(),
            rect.height()
        )

    def _calculate_selection_bounds(self, items):
        """Calculate combined bounds from selected item scene rects."""
        if not items:
            return QRectF()
        scene_rects = [self._get_item_scene_rect(item) for item in items]
        min_x = min(rect.left() for rect in scene_rects)
        min_y = min(rect.top() for rect in scene_rects)
        max_x = max(rect.right() for rect in scene_rects)
        max_y = max(rect.bottom() for rect in scene_rects)
        return QRectF(min_x, min_y, max(1.0, max_x - min_x), max(1.0, max_y - min_y))

    def _is_item_aspect_locked(self, item):
        """Read persisted lock-aspect flag from item data."""
        data = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(data, dict):
            return bool(data.get(self.ASPECT_LOCK_KEY, False))
        return False

    def _set_item_aspect_locked(self, item, locked):
        """Persist lock-aspect flag on item data."""
        data = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(data, dict):
            data[self.ASPECT_LOCK_KEY] = bool(locked)
            item.setData(Qt.ItemDataRole.UserRole, data)
        
    def _apply_position_to_selection(self, x, y):
        """Apply position changes to the selected object(s) with undo support."""
        active_screen = self.main_window.get_active_screen_widget()
        if not isinstance(active_screen, CanvasBaseScreen):
            return
        
        selected_items = active_screen.scene.selectedItems()
        valid_items = [item for item in selected_items if isinstance(item, BaseGraphicObject)]
        
        if not valid_items:
            return

        if len(valid_items) == 1:
            old_positions = [QPointF(valid_items[0].pos())]
            new_positions = [QPointF(x, y)]
            description = "Move Item"
        else:
            selection_bounds = self._calculate_selection_bounds(valid_items)
            dx = x - selection_bounds.x()
            dy = y - selection_bounds.y()
            if dx == 0 and dy == 0:
                return
            old_positions = [QPointF(item.pos()) for item in valid_items]
            new_positions = [QPointF(item.pos().x() + dx, item.pos().y() + dy) for item in valid_items]
            description = "Move Items"

        if old_positions != new_positions:
            command = MoveItemsCommand(valid_items, old_positions, new_positions, description, active_screen)
            active_screen.undo_stack.push(command)

        active_screen.scene.update()
        active_screen.save_items()
        # Update transform handler if exists
        if active_screen.transform_handler:
            active_screen.transform_handler.update_geometry()
                
    def _apply_size_to_selection(self, width, height, maintain_aspect=False, sender=None):
        """Apply size changes to the selected object(s) with undo support."""
        active_screen = self.main_window.get_active_screen_widget()
        if not isinstance(active_screen, CanvasBaseScreen):
            return
        
        selected_items = active_screen.scene.selectedItems()
        valid_items = [item for item in selected_items if isinstance(item, BaseGraphicObject)]
        if not valid_items:
            return

        width = max(1.0, float(width))
        height = max(1.0, float(height))
        old_states = [self._capture_item_state(item) for item in valid_items]

        if len(valid_items) == 1:
            item = valid_items[0]
            snapped_width = max(1.0, round(width))
            snapped_height = max(1.0, round(height))
            item.set_geometry(QRectF(0, 0, snapped_width, snapped_height))
            item.setTransformOriginPoint(QPointF(snapped_width / 2, snapped_height / 2))
        else:
            selection_bounds = self._calculate_selection_bounds(valid_items)
            old_width = selection_bounds.width()
            old_height = selection_bounds.height()
            if old_width < 1 or old_height < 1:
                return

            scale_x = width / old_width
            scale_y = height / old_height

            if maintain_aspect:
                if sender == self.width_spin:
                    scale_y = scale_x
                elif sender == self.height_spin:
                    scale_x = scale_y
                else:
                    uniform = scale_x if abs(scale_x - 1.0) >= abs(scale_y - 1.0) else scale_y
                    scale_x = uniform
                    scale_y = uniform

                locked_width = max(1.0, round(old_width * scale_x))
                locked_height = max(1.0, round(old_height * scale_y))
                if abs(locked_width - self.width_spin.value()) > 0.01 or abs(locked_height - self.height_spin.value()) > 0.01:
                    self._syncing = True
                    self.width_spin.setValue(locked_width)
                    self.height_spin.setValue(locked_height)
                    self._syncing = False
                    self._last_width = self.width_spin.value()
                    self._last_height = self.height_spin.value()

            for item in valid_items:
                initial_rect = self._get_item_rect(item)
                initial_scene_rect = self._get_item_scene_rect(item)
                scaled_width = max(1.0, round(initial_rect.width() * scale_x))
                scaled_height = max(1.0, round(initial_rect.height() * scale_y))

                rel_x = initial_scene_rect.x() - selection_bounds.x()
                rel_y = initial_scene_rect.y() - selection_bounds.y()
                new_x = selection_bounds.x() + rel_x * scale_x
                new_y = selection_bounds.y() + rel_y * scale_y

                item.set_geometry(QRectF(0, 0, scaled_width, scaled_height))
                item.setTransformOriginPoint(QPointF(scaled_width / 2, scaled_height / 2))
                item.setPos(round(new_x), round(new_y))

        new_states = [self._capture_item_state(item) for item in valid_items]
        if old_states != new_states:
            description = "Resize Items" if len(valid_items) > 1 else "Resize Item"
            command = TransformItemsCommand(valid_items, old_states, new_states, description, active_screen)
            active_screen.undo_stack.push(command)

        active_screen.scene.update()
        active_screen.save_items()
        # Update transform handler if exists
        if active_screen.transform_handler:
            active_screen.transform_handler.update_geometry()
                
    def _apply_angle_to_selection(self, angle):
        """Apply rotation angle to the selected object(s) with undo support."""
        active_screen = self.main_window.get_active_screen_widget()
        if not isinstance(active_screen, CanvasBaseScreen):
            return
        
        selected_items = active_screen.scene.selectedItems()
        valid_items = [item for item in selected_items if isinstance(item, BaseGraphicObject)]
        
        if len(valid_items) == 1:
            item = valid_items[0]
            
            # Capture old state
            old_state = self._capture_item_state(item)
            
            # Apply the rotation
            rect = item.boundingRect()
            center = rect.center()
            item.setTransformOriginPoint(center)
            item.setRotation(angle)
            
            # Capture new state
            new_state = self._capture_item_state(item)
            
            # Only push command if state actually changed
            if old_state != new_state:
                command = TransformItemsCommand([item], [old_state], [new_state], "Rotate Item", active_screen)
                active_screen.undo_stack.push(command)
            
            active_screen.scene.update()
            active_screen.save_items()
            # Update transform handler if exists
            if active_screen.transform_handler:
                active_screen.transform_handler.update_geometry()
    
    def sync_from_selection(self, selected_items, deselected_items=None):
        """
        Sync toolbar values from selected canvas items.
        Called when canvas selection changes.
        """
        valid_items = [item for item in selected_items if isinstance(item, BaseGraphicObject)]
        
        if len(valid_items) == 0:
            # No selection - disable and reset
            self._syncing = True
            self.x_spin.setValue(0)
            self.y_spin.setValue(0)
            self.width_spin.setValue(100)
            self.height_spin.setValue(100)
            self.angle_spin.setValue(0)
            self.lock_aspect.setChecked(False)
            self._syncing = False
            self._set_enabled(False)
            return
        
        if len(valid_items) == 1:
            # Single selection - show and enable all properties
            item = valid_items[0]
            self._syncing = True
            
            # Position
            pos = item.pos()
            self.x_spin.setValue(pos.x())
            self.y_spin.setValue(pos.y())
            
            # Size
            rect = self._get_item_rect(item)
            width = rect.width()
            height = rect.height()
            self.width_spin.setValue(width)
            self.height_spin.setValue(height)
            self._last_width = width
            self._last_height = height
            self.lock_aspect.setChecked(self._is_item_aspect_locked(item))
            
            # Angle
            self.angle_spin.setValue(item.rotation())
            
            self._syncing = False
            self._set_enabled(True)
        else:
            # Multiple selection - show bounding box info and group editing
            self._syncing = True
            
            # Calculate combined bounding rect
            selection_bounds = self._calculate_selection_bounds(valid_items)
            
            self.x_spin.setValue(selection_bounds.x())
            self.y_spin.setValue(selection_bounds.y())
            self.width_spin.setValue(selection_bounds.width())
            self.height_spin.setValue(selection_bounds.height())
            self.angle_spin.setValue(0)  # Mixed angles - show 0
            self._last_width = selection_bounds.width()
            self._last_height = selection_bounds.height()
            self.lock_aspect.setChecked(any(self._is_item_aspect_locked(item) for item in valid_items))
            
            self._syncing = False
            
            # Enable position and size for group edit, disable mixed-angle edit
            self.x_spin.setEnabled(True)
            self.y_spin.setEnabled(True)
            self.width_spin.setEnabled(True)
            self.height_spin.setEnabled(True)
            self.angle_spin.setEnabled(False)
            self.lock_aspect.setEnabled(True)
    
    def update_from_canvas(self):
        """
        Update toolbar values from current canvas selection.
        Called during object manipulation (drag, resize, etc.)
        """
        active_screen = self.main_window.get_active_screen_widget()
        if not isinstance(active_screen, CanvasBaseScreen):
            return
        
        selected_items = active_screen.scene.selectedItems()
        self.sync_from_selection(selected_items)
    
    def on_object_data_changed(self, data):
        """
        Handle live updates during object manipulation (resize, move, rotate).
        Called when object_data_changed signal is emitted.
        
        Args:
            data: Dict with 'position' (x, y), 'size' (w, h), and 'rotation' (angle) or None values
        """
        if self._syncing:
            return
        
        self._syncing = True
        
        position = data.get('position')
        size = data.get('size')
        rotation = data.get('rotation')
        
        if position is not None:
            x, y = position
            self.x_spin.setValue(x)
            self.y_spin.setValue(y)
        
        if size is not None:
            active_screen = self.main_window.get_active_screen_widget()
            w, h = size
            if isinstance(active_screen, CanvasBaseScreen):
                valid_items = [
                    item for item in active_screen.scene.selectedItems()
                    if isinstance(item, BaseGraphicObject)
                ]
                if len(valid_items) == 1:
                    rect = self._get_item_rect(valid_items[0])
                    w, h = rect.width(), rect.height()
            self.width_spin.setValue(w)
            self.height_spin.setValue(h)
            self._last_width = w
            self._last_height = h
        
        if rotation is not None:
            self.angle_spin.setValue(rotation)
        
        self._syncing = False
