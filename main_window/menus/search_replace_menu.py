from PyQt6.QtGui import QAction
import qtawesome as qta

class SearchReplaceMenu:
    """
    Creates the 'Search/Replace' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        search_replace_menu = menu_bar.addMenu("&Search/Replace")
        
        tag_search_icon = qta.icon('fa5s.tag', 'fa5s.search', options=[{'color': '#34a853'}, {'color': '#4285f4', 'scale_factor': 0.5, 'offset': (0.1, -0.1)}])
        tag_list_icon = qta.icon('fa5s.tags', options=[{'color': '#34a853'}])
        text_list_icon = qta.icon('fa5s.list-alt', options=[{'color': '#4285f4'}])
        data_browser_icon = qta.icon('fa5s.database', 'fa5s.search', options=[{'color': '#5f6368'}, {'color': '#4285f4', 'scale_factor': 0.4, 'offset': (0.1, -0.1)}])
        ip_address_list_icon = qta.icon('fa5s.ethernet', options=[{'color': '#4285f4'}])

        search_replace_menu.addAction(QAction(tag_search_icon,"Tag Search", main_window))
        search_replace_menu.addAction(QAction(tag_list_icon, "Tag List", main_window))
        search_replace_menu.addAction(QAction(text_list_icon,"Text List", main_window))
        search_replace_menu.addSeparator()

        # Batch Edit Submenu
        batch_edit_icon = qta.icon('fa5s.edit', options=[{'color': '#fbbc05'}])
        batch_edit_menu = search_replace_menu.addMenu(batch_edit_icon, "Batch Edit")
        batch_edit_tags_icon = qta.icon('fa5s.tags', 'fa5s.edit', options=[{'color':'#34a853'}, {'color':'#f8991d', 'scale_factor':0.6}])
        batch_edit_color_icon = qta.icon('fa5s.palette', 'fa5s.edit', options=[{'color':'#4285f4'}, {'color':'#f8991d', 'scale_factor':0.6}])
        batch_edit_shape_icon = qta.icon('fa5s.shapes', 'fa5s.edit', options=[{'color':'#ea4335'}, {'color':'#f8991d', 'scale_factor':0.6}])
        batch_edit_text_icon = qta.icon('fa5s.font', 'fa5s.edit', options=[{'color':'#5f6368'}, {'color':'#f8991d', 'scale_factor':0.6}])
        batch_edit_menu.addAction(QAction(batch_edit_tags_icon, "Tags", main_window))
        batch_edit_menu.addAction(QAction(batch_edit_color_icon, "Color", main_window))
        batch_edit_menu.addAction(QAction(batch_edit_shape_icon, "Shape", main_window))
        batch_edit_menu.addAction(QAction(batch_edit_text_icon, "Text", main_window))

        search_replace_menu.addAction(QAction(data_browser_icon,"Data Browser", main_window))
        search_replace_menu.addAction(QAction(ip_address_list_icon,"IP Address List", main_window))

