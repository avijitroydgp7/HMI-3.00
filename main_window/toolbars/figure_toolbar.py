# main_window\toolbars\figure_toolbar.py
from PySide6.QtWidgets import QToolBar

class FigureToolbar(QToolBar):
    def __init__(self, main_window, figure_menu):
        super().__init__("Figure", main_window)
        self.main_window = main_window
        
        # Add actions from the figure menu
        self.addAction(figure_menu.text_action)
        self.addAction(figure_menu.line_action)
        self.addAction(figure_menu.polyline_action)
        self.addAction(figure_menu.rectangle_action)
        self.addAction(figure_menu.ellipse_action)
        self.addAction(figure_menu.polygon_action)
        self.addAction(figure_menu.circle_action)
        self.addAction(figure_menu.arc_action)
        self.addAction(figure_menu.sector_action)
        self.addAction(figure_menu.table_action)
        self.addAction(figure_menu.scale_action)
        self.addAction(figure_menu.image_action)
        self.addAction(figure_menu.dxf_action)
