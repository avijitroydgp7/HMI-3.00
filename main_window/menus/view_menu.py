from PyQt6.QtGui import QAction
import qtawesome as qta

class ViewMenu:
    """
    Creates the 'View' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        view_menu = menu_bar.addMenu("&View")
        preview_icon = qta.icon('fa5s.eye', 'fa5.eye', options=[{'color': '#bbdefb'}, {'color': '#4285f4'}])
        state_number_icon = qta.icon('fa5s.exchange-alt', options=[{'color': '#4285f4'}])
        object_snap_icon = qta.icon('fa5s.magnet', options=[{'color': '#ea4335'}])

        view_menu.addAction(QAction(preview_icon,"Preview", main_window))
        view_menu.addAction(QAction(state_number_icon,"State No.", main_window))

        # Tool Bar Submenu
        tool_bar_icon = qta.icon('fa5s.wrench', 'fa5s.cog', options=[{'color': '#5f6368'}, {'color': '#9aa0a6', 'scale_factor': 0.7, 'offset': (0.2, 0.2)}])
        tool_bar_menu = view_menu.addMenu(tool_bar_icon, "Tool Bar")
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.desktop'), "Window Display", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.eye'), "View", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.columns'), "Screen", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.edit'), "Edit", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.align-center'), "Alignment", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.shapes'), "Figure", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.cube'), "Object", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.pencil-ruler'), "Draw", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.broadcast-tower'), "Communication", main_window))
        tool_bar_menu.addAction(QAction(qta.icon('fa5s.bug'), "Debug", main_window))

        # Docking Window Submenu
        docking_window_icon = qta.icon('fa5.window-restore', 'fa5s.window-restore', options=[{'color': '#bbdefb'}, {'color': '#5f6368'}])
        docking_window_menu = view_menu.addMenu(docking_window_icon, "Docking Window")
        docking_window_menu.addAction(QAction(qta.icon('fa5s.project-diagram'), "Project Tree", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.sitemap'), "Screen Tree", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.cogs'), "System Tree", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.search-location'), "Device Search", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.database'), "Data Browser", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.list-alt'), "Property Tree", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.ethernet'), "IP Address", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.book-open'), "Library", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.gamepad'), "Controller List", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.table'), "Data View", main_window))
        docking_window_menu.addAction(QAction(qta.icon('fa5s.images'), "Screen Image List", main_window))
        
        # Display Item Submenu
        display_item_icon = qta.icon('fa5s.paint-brush', options=[{'color':'#4285f4'}])
        display_item_menu = view_menu.addMenu(display_item_icon, "Display Item")
        display_item_menu.addAction(QAction(qta.icon('fa5s.tag'), "Tag", main_window))
        display_item_menu.addAction(QAction(qta.icon('fa5s.hashtag'), "Object ID", main_window))
        display_item_menu.addAction(QAction(qta.icon('fa5s.ruler-combined'), "Transform Line", main_window))
        display_item_menu.addAction(QAction(qta.icon('fa5s.hand-pointer'), "Click Area", main_window))
        
        view_menu.addAction(QAction(object_snap_icon,"Object Snap", main_window))

        # Zoom Submenu
        zoom_icon = qta.icon('fa5s.search-plus', options=[{'color': '#4285f4'}])
        zoom_menu = view_menu.addMenu(zoom_icon, "Zoom")
        zoom_menu.addAction(QAction(qta.icon('fa5s.compress'), "Fit Screen", main_window))
        zoom_menu.addSeparator()
        zoom_levels = ["20%", "50%", "75%", "100%", "125%", "150%", "200%", "250%", "300%", "400%", "500%", "600%", "700%", "800%", "900%", "1000%"]
        for level in zoom_levels:
            zoom_menu.addAction(QAction(level, main_window))

