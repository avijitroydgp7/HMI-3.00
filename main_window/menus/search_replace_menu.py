from PyQt6.QtGui import QAction
from ..services.icon_service import IconService

class SearchReplaceMenu:
    """
    Creates the 'Search/Replace' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        search_replace_menu = menu_bar.addMenu("&Search/Replace")
        
        tag_search_icon = IconService.get_icon('search-tag')
        tag_list_icon = IconService.get_icon('search-tag-list')
        text_list_icon = IconService.get_icon('search-text-list')
        data_browser_icon = IconService.get_icon('search-data-browser')
        ip_address_list_icon = IconService.get_icon('search-ip-address-list')

        search_replace_menu.addAction(QAction(tag_search_icon,"Tag Search", main_window))
        search_replace_menu.addAction(QAction(tag_list_icon, "Tag List", main_window))
        search_replace_menu.addAction(QAction(text_list_icon,"Text List", main_window))
        search_replace_menu.addSeparator()

        # Batch Edit Submenu
        batch_edit_icon = IconService.get_icon('search-batch-edit')
        batch_edit_menu = search_replace_menu.addMenu(batch_edit_icon, "Batch Edit")
        batch_edit_tags_icon = IconService.get_icon('search-batch-edit-tags')
        batch_edit_color_icon = IconService.get_icon('search-batch-edit-color')
        batch_edit_shape_icon = IconService.get_icon('search-batch-edit-shape')
        batch_edit_text_icon = IconService.get_icon('search-batch-edit-text')
        batch_edit_menu.addAction(QAction(batch_edit_tags_icon, "Tags", main_window))
        batch_edit_menu.addAction(QAction(batch_edit_color_icon, "Color", main_window))
        batch_edit_menu.addAction(QAction(batch_edit_shape_icon, "Shape", main_window))
        batch_edit_menu.addAction(QAction(batch_edit_text_icon, "Text", main_window))

        search_replace_menu.addAction(QAction(data_browser_icon,"Data Browser", main_window))
        search_replace_menu.addAction(QAction(ip_address_list_icon,"IP Address List", main_window))
