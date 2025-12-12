# main_window/toolbars/transform_handler.py
"""
Robust Transform Handler System
================================
Provides reliable transform handles for single and multiple graphics items.
Includes comprehensive error handling, state validation, and coordinate safety.
"""

from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QPen, QBrush, QColor
from screen.base.base_graphic_object import BaseGraphicObject
from debug_utils import get_logger

logger = get_logger(__name__)


class TransformHandle(QGraphicsRectItem):
    """A single handle (square) for resizing or rotating."""
    
    def __init__(self, cursor_shape, parent=None):
        # 6x6 pixel handle centered relative to its pos
        super().__init__(-3, -3, 6, 6, parent)
        self.setCursor(cursor_shape)
        self.setBrush(QBrush(QColor("white")))
        self.setPen(QPen(QColor("#0078D7"), 1))
        # Ensure handles stay consistent size regardless of zoom
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True)


class BaseTransformHandler(QGraphicsItem):
    """
    Base class for transform handlers with robust state management.
    Provides common functionality and error handling for all handlers.
    """
    transformed = Signal()

    def __init__(self, scene, view_service):
        super().__init__()
        self._is_resizing = False
        self.scene_ref = scene
        self.view_service = view_service
        if self.scene_ref:
            try:
                self.scene_ref.addItem(self)
            except Exception as e:
                logger.error(f"Error adding handler to scene: {e}")
                self.scene_ref = None
        
        self.setZValue(9999)  # Always on top
        
        # Pen for the border line
        self.border_pen = QPen(QColor("#0078D7"), 1, Qt.PenStyle.SolidLine)
        self.border_pen.setCosmetic(True)
        
        # State management
        self._drag_mode = None
        self._is_valid = True
        self._handles = {}
        
        self._create_handles()
    
    def get_items(self):
        """Return the item(s) being transformed."""
        raise NotImplementedError

    def _create_handles(self):
        """Create transform handles."""
        cursors = {
            'tl': Qt.CursorShape.SizeFDiagCursor,
            't':  Qt.CursorShape.SizeVerCursor,
            'tr': Qt.CursorShape.SizeBDiagCursor,
            'r':  Qt.CursorShape.SizeHorCursor,
            'br': Qt.CursorShape.SizeFDiagCursor,
            'b':  Qt.CursorShape.SizeVerCursor,
            'bl': Qt.CursorShape.SizeBDiagCursor,
            'l':  Qt.CursorShape.SizeHorCursor
        }
        
        for key, cursor in cursors.items():
            try:
                self._handles[key] = TransformHandle(cursor, self)
            except Exception as e:
                logger.warning(f"Error creating handle {key}: {e}")
    
    def is_valid(self):
        """Check if handler is still valid."""
        return self._is_valid
    
    def validate(self):
        """Override in subclasses to validate handler state."""
        return self._is_valid
    
    def boundingRect(self):
        """Return local bounding rect."""
        return QRectF()
    
    def paint(self, painter, option, widget=None):
        """Draw the transform visualization."""
        pass
    
    def get_handle_at(self, scene_pos):
        """Returns the name of the handle under the mouse, if any."""
        if not self._is_valid or not self.scene_ref:
            return None
        
        try:
            items = self.scene_ref.items(
                scene_pos, 
                Qt.ItemSelectionMode.IntersectsItemShape, 
                Qt.SortOrder.DescendingOrder
            )
            for item in items:
                for name, handle in self._handles.items():
                    if item == handle:
                        return name
        except Exception as e:
            logger.debug(f"Error getting handle at position: {e}")
        
        return None
    
    def handle_mouse_press(self, handle_name, pos, scene_pos):
        """Called when a handle is pressed."""
        self._drag_mode = handle_name
        self._is_resizing = True
    
    def handle_mouse_move(self, scene_pos, modifiers=Qt.KeyboardModifier.NoModifier):
        """Logic to resize/transform based on handle movement."""
        pass

    def handle_mouse_release(self):
        """Called when the mouse is released after a transform."""
        self._is_resizing = False
        self.transformed.emit()

    
    def cleanup(self):
        """Clean up resources."""
        try:
            if self.scene_ref:
                # Remove all handles from scene
                handles_to_remove = list(self._handles.values())
                for handle in handles_to_remove:
                    try:
                        if handle and handle.scene():
                            # Only remove if the handle belongs to this scene
                            if handle.scene() == self.scene_ref:
                                self.scene_ref.removeItem(handle)
                    except RuntimeError:
                        # Handle already removed, ignore
                        pass
                    except Exception as e:
                        logger.debug(f"Error removing handle: {e}")
                
                # Remove self from scene only if we're in it
                try:
                    if self.scene() == self.scene_ref:
                        self.scene_ref.removeItem(self)
                except RuntimeError:
                    # Already removed, ignore
                    pass
                except Exception as e:
                    logger.debug(f"Error removing self from scene: {e}")
        except Exception as e:
            logger.warning(f"Error during handler cleanup: {e}")
        finally:
            self._is_valid = False
            self._handles.clear()
            self.scene_ref = None


class TransformHandler(BaseTransformHandler):
    """
    Manages selection handles for a single QGraphicsItem.
    Robust version with proper state isolation and error handling.
    """
    
    def __init__(self, target_item, scene, view_service):
        logger.debug("TransformHandler.__init__")
        self.target_item = target_item
        self._aspect_ratio = 1.0
        self._initial_rect = QRectF()
        self._initial_scene_rect = QRectF()

        super().__init__(scene, view_service)
        
        try:
            if self.validate():
                self.update_geometry()
        except Exception as e:
            logger.error(f"Error initializing TransformHandler: {e}")
            self._is_valid = False

    def get_items(self):
        return [self.target_item]

    def validate(self):
        """Validate that target item still exists and is in scene."""
        try:
            if not self.target_item:
                self._is_valid = False
                return False
            
            if not self.target_item.scene():
                self._is_valid = False
                return False
            
            self._is_valid = True
            return True
        except Exception as e:
            logger.debug(f"Error validating handler: {e}")
            self._is_valid = False
            return False

    def boundingRect(self):
        """Return the bounding rect for the handler."""
        if not self.validate():
            return QRectF()
        
        try:
            return self.target_item.boundingRect()
        except Exception as e:
            logger.debug(f"Error getting target item bounding rect: {e}")
            return QRectF()

    def paint(self, painter, option, widget=None):
        """Draws the bounding box outline."""
        if not self.validate() or not painter:
            return
        
        try:
            rect = self.target_item.boundingRect()
            painter.setPen(self.border_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(rect)
        except Exception as e:
            logger.debug(f"Error painting transform handler: {e}")

    def update_geometry(self):
        """Updates the position of the handler and its handles to match the target."""
        if not self.validate():
            self.setVisible(False)
            return

        try:
            # Sync transform with target
            self.setPos(self.target_item.pos())
            self.setRotation(self.target_item.rotation())
            self.setTransform(self.target_item.transform())
            
            # Get local bounding rect of the target
            rect = self.target_item.boundingRect()
            
            # Update handle positions
            h = self._handles
            if rect.width() > 0 and rect.height() > 0:
                h['tl'].setPos(rect.topLeft())
                h['t'].setPos(QPointF(rect.center().x(), rect.top()))
                h['tr'].setPos(rect.topRight())
                h['r'].setPos(QPointF(rect.right(), rect.center().y()))
                h['br'].setPos(rect.bottomRight())
                h['b'].setPos(QPointF(rect.center().x(), rect.bottom()))
                h['bl'].setPos(rect.bottomLeft())
                h['l'].setPos(QPointF(rect.left(), rect.center().y()))
            
            self.prepareGeometryChange()
            self.update()
        except Exception as e:
            logger.error(f"Error updating transform handler geometry: {e}")
            self._is_valid = False

    def handle_mouse_press(self, handle_name, pos, scene_pos):
        """Called when a handle is pressed."""
        if not self.validate():
            return
        
        super().handle_mouse_press(handle_name, pos, scene_pos)
        
        try:
            if isinstance(self.target_item, BaseGraphicObject):
                self._initial_rect = QRectF(self.target_item.boundingRect())
                scene_rect = self.target_item.sceneBoundingRect()
                self._initial_scene_rect = QRectF(round(scene_rect.x()),
                                                  round(scene_rect.y()),
                                                  round(scene_rect.width()),
                                                  round(scene_rect.height()))
                if self._initial_rect.height() != 0:
                    self._aspect_ratio = self._initial_rect.width() / self._initial_rect.height()
                else:
                    self._aspect_ratio = 1.0
        except Exception as e:
            logger.warning(f"Error storing initial rect: {e}")

    def handle_mouse_move(self, scene_pos, modifiers=Qt.KeyboardModifier.NoModifier):
        """Logic to resize the target item based on the active handle."""
        if not self._drag_mode or not self.validate():
            return

        if not isinstance(self.target_item, BaseGraphicObject):
            return
            
        try:
            logger.debug(f"Handling mouse move for single item. Drag mode: {self._drag_mode}, Scene pos: {scene_pos}")
            new_rect = QRectF(self._initial_scene_rect)
            
            snapped_pos = scene_pos

            # Update rect based on handle and mouse position
            if 'l' in self._drag_mode: new_rect.setLeft(snapped_pos.x())
            if 'r' in self._drag_mode: new_rect.setRight(snapped_pos.x())
            if 't' in self._drag_mode: new_rect.setTop(snapped_pos.y())
            if 'b' in self._drag_mode: new_rect.setBottom(snapped_pos.y())

            # Aspect Ratio Lock for corner drags
            maintain_aspect = (modifiers & Qt.KeyboardModifier.ShiftModifier) and \
                              (self._drag_mode in ['tl', 'tr', 'bl', 'br'])
                              
            if maintain_aspect and self._aspect_ratio > 0:
                w = new_rect.width()
                h = new_rect.height()
                
                # Use the dimension that has changed more relative to the aspect ratio
                if abs(w / h) > abs(self._aspect_ratio):
                    # Width is the leading dimension for change
                    h = w / self._aspect_ratio
                    if 't' in self._drag_mode:
                        new_rect.setTop(new_rect.bottom() - h)
                    else: # 'b' handle
                        new_rect.setBottom(new_rect.top() + h)
                else:
                    # Height is the leading dimension
                    w = h * self._aspect_ratio
                    if 'l' in self._drag_mode:
                        new_rect.setLeft(new_rect.right() - w)
                    else: # 'r' handle
                        new_rect.setRight(new_rect.left() + w)

            final_rect = new_rect.normalized()

            # Optimization: only update if geometry has changed
            current_scene_rect = self.target_item.sceneBoundingRect()
            if (round(current_scene_rect.x()) == round(final_rect.x()) and
                round(current_scene_rect.y()) == round(final_rect.y()) and
                round(current_scene_rect.width()) == round(final_rect.width()) and
                round(current_scene_rect.height()) == round(final_rect.height())):
                return

            self.target_item.setPos(round(final_rect.left()), round(final_rect.top()))
            
            # Snap width and height to the nearest integer
            snapped_width = round(final_rect.width())
            snapped_height = round(final_rect.height())

            self.target_item.set_geometry(QRectF(0, 0, snapped_width, snapped_height))
            self.update_geometry()
            logger.debug("Successfully handled mouse move for single item.")

        except Exception as e:
            logger.error(f"CRITICAL: Exception in TransformHandler.handle_mouse_move: {e}", exc_info=True)



class AverageTransformHandler(BaseTransformHandler):
    """
    Manages selection handles for multiple QGraphicsItems.
    Displays an average bounding box around all selected items.
    Robust version with safe coordinate handling and state isolation.
    """
    
    def __init__(self, target_items, scene, view_service):
        logger.debug("AverageTransformHandler.__init__")
        self.target_items = list(target_items) if target_items else []
        self._initial_rects = {}
        self._initial_positions = {}
        self._initial_avg_rect = QRectF()
        self._average_rect = QRectF()
        
        # Use different color for multi-select
        self.border_pen = QPen(QColor("#34a853"), 1, Qt.PenStyle.SolidLine)
        self.border_pen.setCosmetic(True)
        
        super().__init__(scene, view_service)
        
        try:
            if self.validate():
                self.update_geometry()
        except Exception as e:
            logger.error(f"Error initializing AverageTransformHandler: {e}")
            self._is_valid = False

    def get_items(self):
        return self.target_items

    def validate(self):
        """Validate that all target items still exist and are in scene."""
        try:
            if not self.target_items:
                self._is_valid = False
                return False
            
            # Check all items are still valid
            valid_count = 0
            for item in self.target_items:
                try:
                    if item and item.scene():
                        valid_count += 1
                except Exception as e:
                    logger.debug(f"Item validation error: {e}")
            
            if valid_count == 0:
                self._is_valid = False
                return False
            
            self._is_valid = True
            return True
        except Exception as e:
            logger.debug(f"Error validating average handler: {e}")
            self._is_valid = False
            return False

    def _calculate_average_rect(self):
        """Calculate the average bounding rectangle from all selected items."""
        if not self.validate():
            return QRectF()
        
        try:
            min_x = float('inf')
            min_y = float('inf')
            max_x = float('-inf')
            max_y = float('-inf')
            
            has_valid_item = False
            for item in self.target_items:
                try:
                    # Check if item is still valid before accessing it
                    if not item or not item.scene():
                        continue
                    
                    scene_rect = item.sceneBoundingRect()
                    
                    # Validate the rect before using it
                    if scene_rect.isNull() or scene_rect.width() < 1 or scene_rect.height() < 1:
                        continue
                    
                    min_x = min(min_x, scene_rect.left())
                    min_y = min(min_y, scene_rect.top())
                    max_x = max(max_x, scene_rect.right())
                    max_y = max(max_y, scene_rect.bottom())
                    has_valid_item = True
                except Exception as e:
                    logger.debug(f"Error getting item bounding rect: {e}")
                    continue
            
            if not has_valid_item or min_x == float('inf') or max_x == float('-inf'):
                return QRectF()
            
            width = max_x - min_x
            height = max_y - min_y
            
            # Ensure result is valid
            if width < 1 or height < 1:
                return QRectF()
            
            return QRectF(min_x, min_y, width, height)
        except Exception as e:
            logger.error(f"Error calculating average rect: {e}")
            return QRectF()

    def boundingRect(self):
        """Return the bounding rect for the handler."""
        if self._average_rect.isNull():
            return QRectF()
        # Return local coordinates
        return QRectF(0, 0, self._average_rect.width(), self._average_rect.height())

    def paint(self, painter, option, widget=None):
        """Draws the average bounding box outline."""
        if not self.validate() or self._average_rect.isNull() or not painter:
            return
        
        try:
            painter.setPen(self.border_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            local_rect = QRectF(0, 0, self._average_rect.width(), self._average_rect.height())
            painter.drawRect(local_rect)
        except Exception as e:
            logger.debug(f"Error painting average transform handler: {e}")

    def update_geometry(self):
        """Updates the handler to match the current state of selected items."""
        if not self.validate():
            self.setVisible(False)
            return

        try:
            self._average_rect = self._calculate_average_rect()
            
            if self._average_rect.isNull():
                self.setVisible(False)
                return
            
            self.setVisible(True)
            
            # Position the handler at the top-left of the average rect
            self.setPos(self._average_rect.topLeft())
            
            # Update handle positions based on the average rect
            h = self._handles
            if self._average_rect.width() > 0 and self._average_rect.height() > 0:
                local_rect = QRectF(0, 0, self._average_rect.width(), self._average_rect.height())
                
                h['tl'].setPos(local_rect.topLeft())
                h['t'].setPos(QPointF(local_rect.center().x(), local_rect.top()))
                h['tr'].setPos(local_rect.topRight())
                h['r'].setPos(QPointF(local_rect.right(), local_rect.center().y()))
                h['br'].setPos(local_rect.bottomRight())
                h['b'].setPos(QPointF(local_rect.center().x(), local_rect.bottom()))
                h['bl'].setPos(local_rect.bottomLeft())
                h['l'].setPos(QPointF(local_rect.left(), local_rect.center().y()))
            
            self.prepareGeometryChange()
            self.update()
        except Exception as e:
            logger.error(f"Error updating average transform handler geometry: {e}")
            self._is_valid = False

    def handle_mouse_press(self, handle_name, pos, scene_pos):
        """Called when a handle is pressed."""
        logger.debug("AverageTransformHandler.handle_mouse_press")
        if not self.validate():
            return
        
        super().handle_mouse_press(handle_name, pos, scene_pos)
        
        try:
            # Store initial state for all items using object references
            self._initial_rects = {}
            self._initial_positions = {}
            for item in self.target_items:
                try:
                    if isinstance(item, BaseGraphicObject) and item.scene():
                        # Use the item object itself as key instead of id(item)
                        # This avoids stale references
                        item_id = id(item)
                        self._initial_rects[item_id] = (QRectF(item.boundingRect()), item)
                        self._initial_positions[item_id] = (QPointF(round(item.pos().x()), round(item.pos().y())), item)
                except Exception as e:
                    logger.debug(f"Error storing item state: {e}")
            
            if self._initial_rects:
                avg_rect = self._calculate_average_rect()
                if not avg_rect.isNull():
                    self._initial_avg_rect = QRectF(round(avg_rect.x()),
                                                    round(avg_rect.y()),
                                                    round(avg_rect.width()),
                                                    round(avg_rect.height()))
            else:
                logger.warning("No valid items to transform")
                self._initial_avg_rect = QRectF()
        except Exception as e:
            logger.warning(f"Error in handle_mouse_press: {e}")

    def handle_mouse_move(self, scene_pos, modifiers=Qt.KeyboardModifier.NoModifier):
        """Logic to resize all selected items proportionally."""
        logger.debug("AverageTransformHandler.handle_mouse_move")
        if not self._drag_mode or not self.validate():
            return
        
        if self._initial_avg_rect.isNull():
            return
        
        try:
            logger.debug(f"Handling mouse move for multiple items. Drag mode: {self._drag_mode}, Scene pos: {scene_pos}")
            # Determine new rect based on which handle is being dragged
            new_rect = QRectF(self._initial_avg_rect)
            
            snapped_pos = scene_pos
            
            if 'r' in str(self._drag_mode):
                new_rect.setRight(snapped_pos.x())
            if 'l' in str(self._drag_mode):
                new_rect.setLeft(snapped_pos.x())
            if 'b' in str(self._drag_mode):
                new_rect.setBottom(snapped_pos.y())
            if 't' in str(self._drag_mode):
                new_rect.setTop(snapped_pos.y())
            
            new_rect = new_rect.normalized()
            
            # Optimization: only update if geometry has changed
            if (round(self._average_rect.x()) == round(new_rect.x()) and
                round(self._average_rect.y()) == round(new_rect.y()) and
                round(self._average_rect.width()) == round(new_rect.width()) and
                round(self._average_rect.height()) == round(new_rect.height())):
                return

            # Calculate scale factors with safety checks
            old_width = self._initial_avg_rect.width()
            old_height = self._initial_avg_rect.height()
            new_width = new_rect.width()
            new_height = new_rect.height()
            
            # Prevent division by zero and handle minimum size
            if old_width < 1 or old_height < 1 or new_width < 1 or new_height < 1:
                logger.debug("Skipping resize: dimensions too small")
                return
            
            scale_x = new_width / old_width
            scale_y = new_height / old_height
            logger.debug(f"Scale factors: x={scale_x}, y={scale_y}")
            
            # Apply transformations to all items
            for item_id, (initial_rect, item) in self._initial_rects.items():
                try:
                    if isinstance(item, BaseGraphicObject) and item.scene():
                        # Ensure scaled dimensions are valid
                        scaled_width = round(initial_rect.width() * scale_x)
                        scaled_height = round(initial_rect.height() * scale_y)
                        
                        if scaled_width < 1 or scaled_height < 1:
                            logger.debug(f"Skipping item transform: scaled dimensions too small")
                            continue
                        
                        # Scale the item size
                        new_item_rect = QRectF(0, 0, scaled_width, scaled_height)
                        item.set_geometry(new_item_rect)
                        
                        # Calculate new position
                        initial_pos, _ = self._initial_positions.get(item_id, (QPointF(0, 0), None))
                        offset_x = initial_pos.x() - self._initial_avg_rect.left()
                        offset_y = initial_pos.y() - self._initial_avg_rect.top()
                        
                        new_x = new_rect.left() + offset_x * scale_x
                        new_y = new_rect.top() + offset_y * scale_y
                        
                        item.setPos(round(new_x), round(new_y))
                except Exception as e:
                    logger.debug(f"Error transforming item: {e}")
            
            self.update_geometry()
            logger.debug("Successfully handled mouse move for multiple items.")
        except Exception as e:
            logger.error(f"CRITICAL: Exception in AverageTransformHandler.handle_mouse_move: {e}", exc_info=True)


    def cleanup(self):
        """Clean up and release references."""
        logger.debug("AverageTransformHandler.cleanup")
        try:
            # Clear all item references
            if self.target_items:
                self.target_items.clear()
            if self._initial_rects:
                self._initial_rects.clear()
            if self._initial_positions:
                self._initial_positions.clear()
        except Exception as e:
            logger.debug(f"Error during average handler cleanup: {e}")
        finally:
            super().cleanup()
