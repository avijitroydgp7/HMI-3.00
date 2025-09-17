"main_window/menus/figure_menu.py"
from PyQt6.QtGui import QAction
from ..services.icon_service import IconService

class FigureMenu:
    """
    Creates the 'Figure' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        self.main_window = main_window
        figure_menu = menu_bar.addMenu("&Figure")

        text_figure_icon = IconService.get_icon('figure-text')
        line_figure_icon = IconService.get_icon('figure-line')
        polyline_figure_icon = IconService.get_icon('figure-polyline')
        rectangle_figure_icon = IconService.get_icon('figure-rectangle')
        polygon_figure_icon = IconService.get_icon('figure-polygon')
        circle_figure_icon = IconService.get_icon('figure-circle')
        arc_figure_icon = IconService.get_icon('figure-arc')
        sector_figure_icon = IconService.get_icon('figure-sector')
        table_figure_icon = IconService.get_icon('figure-table')
        scale_figure_icon = IconService.get_icon('figure-scale')
        image_figure_icon = IconService.get_icon('figure-image')
        dxf_figure_icon = IconService.get_icon('figure-dxf')
        
        self.text_action = QAction(text_figure_icon, "Text", self.main_window)
        self.line_action = QAction(line_figure_icon, "Line", self.main_window)
        self.polyline_action = QAction(polyline_figure_icon, "Polyline", self.main_window)
        self.rectangle_action = QAction(rectangle_figure_icon, "Rectangle", self.main_window)
        self.polygon_action = QAction(polygon_figure_icon, "Polygon", self.main_window)
        self.circle_action = QAction(circle_figure_icon, "Circle", self.main_window)
        self.arc_action = QAction(arc_figure_icon, "Arc", self.main_window)
        self.sector_action = QAction(sector_figure_icon, "Sector", self.main_window)
        self.table_action = QAction(table_figure_icon, "Table", self.main_window)
        self.scale_action = QAction(scale_figure_icon, "Scale", self.main_window)
        self.image_action = QAction(image_figure_icon, "Image", self.main_window)
        self.dxf_action = QAction(dxf_figure_icon, "DXF", self.main_window)

        figure_menu.addAction(self.text_action)
        figure_menu.addAction(self.line_action)
        figure_menu.addAction(self.polyline_action)
        figure_menu.addAction(self.rectangle_action)
        figure_menu.addAction(self.polygon_action)
        figure_menu.addAction(self.circle_action)
        figure_menu.addAction(self.arc_action)
        figure_menu.addAction(self.sector_action)
        figure_menu.addAction(self.table_action)
        figure_menu.addAction(self.scale_action)
        figure_menu.addAction(self.image_action)
        figure_menu.addAction(self.dxf_action)
