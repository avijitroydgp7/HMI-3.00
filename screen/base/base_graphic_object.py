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
            
            # For object snapping, the logic is handled in the view during mouse move.
            # Here we just round to avoid fractional positions.
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