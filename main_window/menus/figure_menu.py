from PyQt6.QtGui import QAction
import qtawesome as qta

class FigureMenu:
    """
    Creates the 'Figure' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
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
        
        figure_menu.addAction(QAction(text_figure_icon, "Text", main_window))
        figure_menu.addAction(QAction(line_figure_icon, "Line", main_window))
        figure_menu.addAction(QAction(polyline_figure_icon, "Polyline", main_window))
        figure_menu.addAction(QAction(rectangle_figure_icon, "Rectangle", main_window))
        figure_menu.addAction(QAction(polygon_figure_icon, "Polygon", main_window))
        figure_menu.addAction(QAction(circle_figure_icon, "Circle", main_window))
        figure_menu.addAction(QAction(arc_figure_icon, "Arc", main_window))
        figure_menu.addAction(QAction(sector_figure_icon, "Sector", main_window))
        figure_menu.addAction(QAction(table_figure_icon, "Table", main_window))
        figure_menu.addAction(QAction(scale_figure_icon, "Scale", main_window))
        figure_menu.addAction(QAction(image_figure_icon, "Image", main_window))
        figure_menu.addAction(QAction(dxf_figure_icon, "DXF", main_window))

