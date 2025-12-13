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
        # Hit area: 12x12 pixel square (larger than visual for easier clicking)
        # Centered relative to its pos (-6, -6)
        super().__init__(-6, -6, 12, 12, parent)
        self.setCursor(cursor_shape)
        self.setBrush(QBrush(QColor("white")))
        self.setPen(QPen(QColor("#00FFFF"), 2))
        # Ensure handles stay consistent size regardless of zoom
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True)

    def paint(self, painter, option, widget=None):
        """
        Draws the visual representation of the handle.
        We draw a smaller 6x6 square inside the larger 12x12 hit area.
        """
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        # Visual area: 6x6 centered
        painter.drawRect(-3, -3, 6, 6)


class BaseTransformHandler(QGraphicsItem):
    """
    Base class for transform handlers with robust state management.
    Provides common functionality and error handling for all handlers.
    """

    def __init__(self, scene, view_service):
        super().__init__()
        self._is_resizing = False
        self.scene_ref = scene
        self.view_service = view_service
        
        self.setZValue(9999)  # Always on top
        
        # Pen for the border line
        if not hasattr(self, 'border_pen'):
            self.border_pen = QPen(QColor("#00FFFF"), 2, Qt.PenStyle.SolidLine)
            self.border_pen.setCosmetic(True)
        
        # State management
        self._drag_mode = None
        self._is_valid = True
        self._handles = {}
        
        self._create_handles()
        
        # CRITICAL: Do NOT call addItem(self) here. 
        # Subclasses must call addToScene() explicitly at the end of their __init__.

    def addToScene(self):
        """Safely add the handler to the scene after full initialization."""
        if self.scene_ref:
            try:
                # Check if already in a scene to avoid errors
                if self.scene() == self.scene_ref:
                    return
                self.scene_ref.addItem(self)
            except Exception as e:
                logger.error(f"Error adding handler to scene: {e}")
                self.scene_ref = None

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
        """
        Returns the name of the handle under the mouse using scene coordinates.
        Note: Use get_handle_from_items for more robust view-based detection.
        """
        if not self._is_valid or not self.scene_ref:
            return None
        
        try:
            items = self.scene_ref.items(
                scene_pos, 
                Qt.ItemSelectionMode.IntersectsItemShape, 
                Qt.SortOrder.DescendingOrder
            )
            return self.get_handle_from_items(items)
        except Exception as e:
            logger.debug(f"Error getting handle at position: {e}")
        
        return None

    def get_handle_from_items(self, items):
        """
        Finds a handle name from a list of QGraphicsItems.
        This is preferred for use with QGraphicsView.items(pos).
        """
        if not self._is_valid:
            return None
            
        for item in items:
            for name, handle in self._handles.items():
                if item == handle:
                    return name
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

    def cleanup(self):
        """Clean up resources safely."""
        try:
            if self.scene() and self.scene_ref and self.scene() == self.scene_ref:
                self.scene_ref.removeItem(self)
        except Exception as e:
            logger.warning(f"Error during handler cleanup: {e}")
        finally:
            self._is_valid = False
            self._handles.clear()
            self.scene_ref = None


class TransformHandler(BaseTransformHandler):
    """
    Manages selection handles for a single QGraphicsItem.
    """
    
    def __init__(self, target_item, scene, view_service):
        logger.debug("TransformHandler.__init__")
        self.target_item = target_item
        self._aspect_ratio = 1.0
        self._initial_rect = QRectF()
        self._initial_scene_rect = QRectF()

        # Initialize base class WITHOUT adding to scene yet
        super().__init__(scene, view_service)
        
        try:
            if self.validate():
                self.update_geometry()
                # NOW it is safe to add to scene because we are fully initialized
                self.addToScene() 
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
                
                if abs(w / h) > abs(self._aspect_ratio):
                    h = w / self._aspect_ratio
                    if 't' in self._drag_mode: new_rect.setTop(new_rect.bottom() - h)
                    else: new_rect.setBottom(new_rect.top() + h)
                else:
                    w = h * self._aspect_ratio
                    if 'l' in self._drag_mode: new_rect.setLeft(new_rect.right() - w)
                    else: new_rect.setRight(new_rect.left() + w)

            final_rect = new_rect.normalized()

            # Enforce Minimum Size
            if final_rect.width() < 1: final_rect.setWidth(1)
            if final_rect.height() < 1: final_rect.setHeight(1)

            # Optimization: only update if geometry has changed
            current_scene_rect = self.target_item.sceneBoundingRect()
            if (round(current_scene_rect.x()) == round(final_rect.x()) and
                round(current_scene_rect.y()) == round(final_rect.y()) and
                round(current_scene_rect.width()) == round(final_rect.width()) and
                round(current_scene_rect.height()) == round(final_rect.height())):
                return

            self.target_item.setPos(round(final_rect.left()), round(final_rect.top()))
            
            snapped_width = round(final_rect.width())
            snapped_height = round(final_rect.height())

            self.prepareGeometryChange()

            self.target_item.set_geometry(QRectF(0, 0, snapped_width, snapped_height))
            self.update_geometry()
            logger.debug("Successfully handled mouse move for single item.")

        except Exception as e:
            logger.error(f"CRITICAL: Exception in TransformHandler.handle_mouse_move: {e}", exc_info=True)


class AverageTransformHandler(BaseTransformHandler):
    """
    Manages selection handles for multiple QGraphicsItems.
    """
    
    def __init__(self, target_items, scene, view_service):
        logger.debug("AverageTransformHandler.__init__")
        self.target_items = list(target_items) if target_items else []
        self._initial_rects = {}
        self._initial_positions = {}
        self._initial_avg_rect = QRectF()
        self._average_rect = QRectF()
        
        self.border_pen = QPen(QColor("#00FFFF"), 2, Qt.PenStyle.SolidLine)
        self.border_pen.setCosmetic(True)
        
        super().__init__(scene, view_service)
        
        try:
            if self.validate():
                self.update_geometry()
                # NOW it is safe to add to scene
                self.addToScene()
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
                    if not item or not item.scene(): continue
                    
                    scene_rect = item.sceneBoundingRect()
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
        return QRectF(0, 0, self._average_rect.width(), self._average_rect.height())

    def paint(self, painter, option, widget=None):
        if not self.validate() or self._average_rect.isNull() or not painter:
            return
        try:
            # Draw individual highlights for selected items
            # Use a dashed blue line for individual items to distinguish them
            painter.save()
            individual_pen = QPen(QColor("#FF4FF0"), 2, Qt.PenStyle.DashLine)
            individual_pen.setCosmetic(True)
            painter.setPen(individual_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            handler_pos = self.pos()

            for item in self.target_items:
                try:
                    if item and item.scene():
                        # Get item's rect in scene coordinates
                        scene_rect = item.sceneBoundingRect()
                        
                        # Calculate position relative to this handler
                        local_x = scene_rect.x() - handler_pos.x()
                        local_y = scene_rect.y() - handler_pos.y()
                        
                        painter.drawRect(QRectF(local_x, local_y, scene_rect.width(), scene_rect.height()))
                except Exception as e:
                    logger.debug(f"Error drawing individual selection: {e}")
            
            painter.restore()

            # Draw the main group bounding box (Green)
            painter.setPen(self.border_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            local_rect = QRectF(0, 0, self._average_rect.width(), self._average_rect.height())
            painter.drawRect(local_rect)
        except Exception as e:
            logger.debug(f"Error painting average transform handler: {e}")

    def update_geometry(self):
        if not self.validate():
            self.setVisible(False)
            return

        try:
            new_rect = self._calculate_average_rect()
            if new_rect.isNull():
                self.setVisible(False)
                return
            
            self.prepareGeometryChange()
            self._average_rect = new_rect
            
            self.setVisible(True)
            self.setPos(self._average_rect.topLeft())
            
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
            
            self.update()
        except Exception as e:
            logger.error(f"Error updating average transform handler geometry: {e}")
            self._is_valid = False

    def handle_mouse_press(self, handle_name, pos, scene_pos):
        if not self.validate(): return
        super().handle_mouse_press(handle_name, pos, scene_pos)
        
        try:
            self._initial_rects = {}
            self._initial_positions = {}
            for item in self.target_items:
                try:
                    if isinstance(item, BaseGraphicObject) and item.scene():
                        item_id = id(item)
                        self._initial_rects[item_id] = (QRectF(item.boundingRect()), item)
                        self._initial_positions[item_id] = (QPointF(round(item.pos().x()), round(item.pos().y())), item)
                except Exception as e:
                    logger.debug(f"Error storing item state: {e}")
            
            if self._initial_rects:
                avg_rect = self._calculate_average_rect()
                if not avg_rect.isNull():
                    self._initial_avg_rect = QRectF(round(avg_rect.x()), round(avg_rect.y()), round(avg_rect.width()), round(avg_rect.height()))
        except Exception as e:
            logger.warning(f"Error in handle_mouse_press: {e}")

    def handle_mouse_move(self, scene_pos, modifiers=Qt.KeyboardModifier.NoModifier):
        if not self._drag_mode or not self.validate(): return
        if self._initial_avg_rect.isNull(): return
        
        try:
            new_rect = QRectF(self._initial_avg_rect)
            snapped_pos = scene_pos
            
            if 'r' in str(self._drag_mode): new_rect.setRight(snapped_pos.x())
            if 'l' in str(self._drag_mode): new_rect.setLeft(snapped_pos.x())
            if 'b' in str(self._drag_mode): new_rect.setBottom(snapped_pos.y())
            if 't' in str(self._drag_mode): new_rect.setTop(snapped_pos.y())
            
            new_rect = new_rect.normalized()
            
            old_width = self._initial_avg_rect.width()
            old_height = self._initial_avg_rect.height()
            new_width = new_rect.width()
            new_height = new_rect.height()
            
            if old_width < 1 or old_height < 1 or new_width < 1 or new_height < 1:
                return
            
            scale_x = new_width / old_width
            scale_y = new_height / old_height
            
            for item_id, (initial_rect, item) in self._initial_rects.items():
                try:
                    if isinstance(item, BaseGraphicObject) and item.scene():
                        scaled_width = round(initial_rect.width() * scale_x)
                        scaled_height = round(initial_rect.height() * scale_y)
                        
                        if scaled_width < 1 or scaled_height < 1: continue
                        
                        new_item_rect = QRectF(0, 0, scaled_width, scaled_height)
                        item.set_geometry(new_item_rect)
                        
                        initial_pos, _ = self._initial_positions.get(item_id, (QPointF(0, 0), None))
                        offset_x = initial_pos.x() - self._initial_avg_rect.left()
                        offset_y = initial_pos.y() - self._initial_avg_rect.top()
                        
                        new_x = new_rect.left() + offset_x * scale_x
                        new_y = new_rect.top() + offset_y * scale_y
                        
                        item.setPos(round(new_x), round(new_y))
                except Exception as e:
                    logger.debug(f"Error transforming item: {e}")
            
            self.update_geometry()
        except Exception as e:
            logger.error(f"CRITICAL: Exception in AverageTransformHandler.handle_mouse_move: {e}", exc_info=True)

    def cleanup(self):
        try:
            if self.target_items: self.target_items.clear()
            if self._initial_rects: self._initial_rects.clear()
            if self._initial_positions: self._initial_positions.clear()
        except Exception as e:
            logger.debug(f"Error during average handler cleanup: {e}")
        finally:
            super().cleanup()