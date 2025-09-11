from PyQt6.QtGui import QAction
import qtawesome as qta

class FigureMenu:
    """
    Creates the 'Figure' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        self.main_window = main_window
        figure_menu = menu_bar.addMenu("&Figure")

        text_figure_icon = qta.icon('fa5s.font', 'fa5s.pen', options=[{'color': '#9aa0a6'}, {'color': '#4285f4', 'scale_factor': 0.6, 'offset': (0.2, 0.2)}])
        line_figure_icon = qta.icon('fa6s.slash', 'fa5s.minus', options=[{'color': '#bbdefb'}, {'color': '#5f6368'}])
        polyline_figure_icon = qta.icon('fa5s.draw-polygon', 'mdi.vector-polygon', options=[{'color': '#34a853'}, {'color': '#2e7d32', 'opacity': 0.7}])
        rectangle_figure_icon = qta.icon('fa5.square', 'fa5s.square', options=[{'color': '#bbdefb'}, {'color': '#5f6368'}])
        polygon_figure_icon = qta.icon('fa6s.shapes', 'fa5s.shapes', options=[{'color': '#fbbc05'}, {'color': '#f8991d'}])
        circle_figure_icon = qta.icon('fa5.circle', 'fa5s.circle', options=[{'color': '#bbdefb'}, {'color': '#5f6368'}])
        arc_figure_icon = qta.icon('fa6s.chart-pie', 'fa5s.chart-pie', options=[{'color': '#ea4335', 'opacity': 0.6}, {'color': '#c5221f'}])
        sector_figure_icon = qta.icon('fa5s.chart-pie', 'fa5.dot-circle', options=[{'color':'#4285f4'}, {'color':'white', 'scale_factor': 0.4}])
        table_figure_icon = qta.icon('fa6s.table', 'fa5s.table', options=[{'color': '#bbdefb'}, {'color': '#5f6368'}])
        scale_figure_icon = qta.icon('fa6s.ruler', 'fa5s.ruler-combined', options=[{'color': '#9aa0a6'}, {'color': '#5f6368'}])
        image_figure_icon = qta.icon('fa5.image', 'fa5s.image', options=[{'color': '#bbdefb'}, {'color': '#4285f4'}])
        dxf_figure_icon = qta.icon('fa5s.file-code', 'fa5.file', options=[{'color': '#5f6368'}, {'color': '#9aa0a6', 'opacity': 0.5}])
        
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
