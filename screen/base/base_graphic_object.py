# screen\base\base_graphic_object.py
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem
from PySide6.QtCore import QRectF, QPointF
from debug_utils import get_logger

logger = get_logger(__name__)

class BaseGraphicObject(QGraphicsItem):
    """
    Abstract base class for all drawable objects on the canvas.
    It defines a common interface for geometric transformations.
    """

    def __init__(self, item, view_service=None, view=None, parent=None):
        super().__init__(parent)
        self.item = item
        self.item.setParentItem(self)
        self.view_service = view_service
        self.view = view

    def boundingRect(self):
        return self.item.boundingRect()

    def paint(self, painter, option, widget):
        # The painting is delegated to the composed item.
        # This allows us to use standard QGraphics*Item painting behavior.
        pass

    def set_geometry(self, rect: QRectF):
        """
        Sets the geometry of the object. This must be implemented by subclasses.
        This is the key method for the TransformHandler to be generic.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange and self.scene():
            new_pos = value
            
            if self.view_service and self.view_service.snap_enabled:
                if self.view_service.snapping_mode == 'grid':
                    grid_size = self.view_service.grid_size
                    new_pos.setX(round(new_pos.x() / grid_size) * grid_size)
                    new_pos.setY(round(new_pos.y() / grid_size) * grid_size)
                    return new_pos
                elif self.view_service.snapping_mode == 'object':
                    try:
                        # Magnetic snapping: attempt to align edges/centers to nearby objects
                        threshold = float(self.view_service.grid_size)

                        # Compute candidate moving rect at the new position
                        br = self.boundingRect()
                        m_left = new_pos.x() + br.left()
                        m_right = new_pos.x() + br.right()
                        m_top = new_pos.y() + br.top()
                        m_bottom = new_pos.y() + br.bottom()
                        m_v_center = new_pos.y() + br.center().y()
                        m_h_center = new_pos.x() + br.center().x()

                        best_dx = 0.0
                        best_dy = 0.0
                        best_dist_x = threshold
                        best_dist_y = threshold

                        static_items = [
                            it for it in self.scene().items()
                            if isinstance(it, BaseGraphicObject) and it is not self
                            and it.isVisible() and it.data(Qt.ItemDataRole.UserRole) is not None
                        ]

                        for static in static_items:
                            srect = static.sceneBoundingRect()
                            s_left, s_right = srect.left(), srect.right()
                            s_top, s_bottom = srect.top(), srect.bottom()
                            s_v_center = srect.center().y()
                            s_h_center = srect.center().x()

                            snap_pairs_x = [
                                (m_left, s_left), (m_left, s_right), (m_left, s_h_center),
                                (m_right, s_left), (m_right, s_right), (m_right, s_h_center),
                                (m_h_center, s_left), (m_h_center, s_right), (m_h_center, s_h_center)
                            ]
                            for m_edge, s_edge in snap_pairs_x:
                                dist = s_edge - m_edge
                                if abs(dist) < abs(best_dist_x):
                                    best_dist_x = abs(dist)
                                    best_dx = dist

                            snap_pairs_y = [
                                (m_top, s_top), (m_top, s_bottom), (m_top, s_v_center),
                                (m_bottom, s_top), (m_bottom, s_bottom), (m_bottom, s_v_center),
                                (m_v_center, s_top), (m_v_center, s_bottom), (m_v_center, s_v_center)
                            ]
                            for m_edge, s_edge in snap_pairs_y:
                                dist = s_edge - m_edge
                                if abs(dist) < abs(best_dist_y):
                                    best_dist_y = abs(dist)
                                    best_dy = dist

                        # Prefer the closest axis only
                        if abs(best_dx) > 0 and abs(best_dx) <= threshold and (abs(best_dx) < abs(best_dy) or abs(best_dy) > threshold):
                            new_pos.setX(round(new_pos.x() + best_dx))
                        if abs(best_dy) > 0 and abs(best_dy) <= threshold and (abs(best_dy) < abs(best_dx) or abs(best_dx) > threshold):
                            new_pos.setY(round(new_pos.y() + best_dy))

                        return new_pos
                    except Exception:
                        pass

            # Fallback: round to integer positions to avoid fractional coords
            new_pos.setX(round(new_pos.x()))
            new_pos.setY(round(new_pos.y()))
            return new_pos

        return super().itemChange(change, value)


class RectangleObject(BaseGraphicObject):
    """
    A concrete implementation for a rectangle object.
    """
    def __init__(self, rect: QRectF, view_service=None, view=None, parent=None):
        # We create a QGraphicsRectItem and compose it.
        super().__init__(QGraphicsRectItem(rect), view_service, view, parent)

    @property
    def rect_item(self) -> QGraphicsRectItem:
        return self.item

    def set_geometry(self, rect: QRectF):
        """
        Sets the geometry of the underlying QGraphicsRectItem.
        """
        try:
            self.prepareGeometryChange()
            self.rect_item.setRect(rect)
        except Exception as e:
            logger.error(f"CRITICAL: Error in RectangleObject.set_geometry: {e}", exc_info=True)


    def paint(self, painter, option, widget):
        # We need to explicitly call the composed item's paint method
        # if we want it to be rendered.
        self.item.paint(painter, option, widget)


class EllipseObject(BaseGraphicObject):
    """
    A concrete implementation for an ellipse object.
    """
    def __init__(self, rect: QRectF, view_service=None, view=None, parent=None):
        # We create a QGraphicsEllipseItem and compose it.
        super().__init__(QGraphicsEllipseItem(rect), view_service, view, parent)

    @property
    def ellipse_item(self) -> QGraphicsEllipseItem:
        return self.item

    def set_geometry(self, rect: QRectF):
        """
        Sets the geometry of the underlying QGraphicsEllipseItem.
        """
        try:
            self.prepareGeometryChange()
            self.ellipse_item.setRect(rect)
        except Exception as e:
            logger.error(f"CRITICAL: Error in EllipseObject.set_geometry: {e}", exc_info=True)

    
    def paint(self, painter, option, widget):
        # We need to explicitly call the composed item's paint method
        # if we want it to be rendered.
        self.item.paint(painter, option, widget)