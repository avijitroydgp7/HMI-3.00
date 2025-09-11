import sys
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import qtawesome as qta

class MainWindow(QMainWindow):
    """
    This is the main window of the application.
    It inherits from QMainWindow.
    """
    def __init__(self):
        """
        Constructor for the MainWindow class.
        """
        super().__init__()

        # Set the window title
        self.setWindowTitle("HMI Designer")

        # Set the initial size of the window (width, height)
        self.setGeometry(0,0, 1920, 1080)
        self.setWindowState(Qt.WindowState.WindowMaximized)

        # Create the menu bar
        self._create_menu_bar()

        # You can add widgets and layouts here in the future

    def _create_menu_bar(self):
        """
        Creates the menu bar for the main window.
        """
        menu_bar = self.menuBar()

        # --- File Menu ---
        file_menu = menu_bar.addMenu("&File")

        # Create multicolor icons
        new_icon = qta.icon('fa5s.file-alt', 'fa5s.plus-circle', options=[{'color': '#4285f4'}, {'color': '#34a853', 'scale_factor': 0.6}])
        open_icon = qta.icon('fa5s.folder', 'fa5.folder-open', options=[{'color': '#fbbc05'}, {'color': '#f8991d', 'opacity': 0.8}])
        save_icon = qta.icon('fa5.save', 'fa5s.save', options=[{'color': '#bbdefb'}, {'color': '#4285f4'}])
        save_as_icon = qta.icon('fa5s.save', 'fa5s.copy', options=[{'color': '#4285f4', 'offset': (0.15, 0.15), 'opacity': 0.7}, {'color': '#4285f4'}])
        run_icon = qta.icon('fa5s.play-circle', options=[{'color': '#34a853'}])
        close_tab_icon = qta.icon('fa5s.window-maximize', 'fa5s.times', options=[{'color': '#5f6368'}, {'color': '#ea4335', 'scale_factor': 0.5}])
        close_all_tabs_icon = qta.icon('fa5s.window-close', 'fa5.window-close', options=[{'color':'#ea4335', 'offset':(0.1, -0.1)}, {'color':'#c5221f'}])
        exit_icon = qta.icon('fa5s.sign-out-alt', options=[{'color': '#ea4335'}])

        # New, Open, Save actions
        new_action = QAction(new_icon,"New", self)
        open_action = QAction(open_icon,"Open", self)
        save_action = QAction(save_icon,"Save", self)
        save_as_action = QAction(save_as_icon,"Save As", self)
        run_action = QAction(run_icon,"Run", self)
        close_tab_action = QAction(close_tab_icon,"Close Tab", self)
        close_all_tabs_action = QAction(close_all_tabs_icon,"Close All Tabs", self)
        exit_action = QAction(exit_icon,"Exit", self)

        new_action.setShortcut("Ctrl+N")
        open_action.setShortcut("Ctrl+O")
        save_action.setShortcut("Ctrl+S")
        save_as_action.setShortcut("Ctrl+Shift+S")
        run_action.setShortcut("F4")
        close_tab_action.setShortcut("Ctrl+W")
        close_all_tabs_action.setShortcut("Ctrl+Shift+W")
        exit_action.setShortcut("Ctrl+Q")

        # Exit action
        exit_action.triggered.connect(self.close) # Connects the action to closing the window

        # Add actions to the File menu
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(run_action)
        file_menu.addSeparator() # Adds a separator line
        file_menu.addAction(close_tab_action)
        file_menu.addAction(close_all_tabs_action)
        file_menu.addSeparator() # Adds a separator line
        file_menu.addAction(exit_action)



        # --- Edit Menu ---
        edit_menu = menu_bar.addMenu("&Edit")

        # Create multicolor icons
        undo_icon = qta.icon('fa5s.undo', options=[{'color': '#4285f4'}])
        redo_icon = qta.icon('fa5s.redo', options=[{'color': '#4285f4'}])
        cut_icon = qta.icon('fa5s.cut', options=[{'color': '#5f6368'}])
        copy_icon = qta.icon('fa5.copy', 'fa5s.copy', options=[{'color': '#bbdefb', 'offset': (0.1, -0.1)}, {'color': '#4285f4'}])
        paste_icon = qta.icon('fa5s.clipboard', 'fa5s.file-alt', options=[{'color': '#5f6368'}, {'color': 'white', 'scale_factor': 0.7}])
        duplicate_icon = qta.icon('fa5.clone', options=[{'color': '#4285f4'}])
        delete_icon = qta.icon('fa5s.trash-alt', options=[{'color': '#ea4335'}])
        align_icon = qta.icon('fa5s.align-center', options=[{'color': '#4285f4'}])
        consecutive_copy_icon = qta.icon('fa5s.layer-group', options=[{'color': '#4285f4'}])
        select_all_icon = qta.icon('fa5s.border-all', options=[{'color': '#5f6368'}])
        stacking_order_icon = qta.icon('fa5s.sort-amount-up', options=[{'color': '#4285f4'}])
        wrap_icon = qta.icon('fa5s.compress-arrows-alt', options=[{'color': '#4285f4'}])
        flip_icon = qta.icon('fa5s.exchange-alt', options=[{'color': '#4285f4'}])


        # Actions
        undo_action = QAction(undo_icon,"Undo", self)
        redo_action = QAction(redo_icon,"Redo", self)
        cut_action = QAction(cut_icon,"Cut", self)
        copy_action = QAction(copy_icon,"Copy", self)
        paste_action = QAction(paste_icon,"Paste", self)
        duplicate_action = QAction(duplicate_icon,"Duplicate", self)
        consecutive_copy_action = QAction(consecutive_copy_icon, "Consecutive Copy", self)
        select_all_action = QAction(select_all_icon, "Select All", self)
        delete_action = QAction(delete_icon,"Delete", self)
        stacking_order_action = QAction(stacking_order_icon, "Stacking Order", self)
        align_action = QAction(align_icon,"Align", self)
        wrap_action = QAction(wrap_icon, "Wrap", self)
        flip_action = QAction(flip_icon, "Flip", self)
        
        undo_action.setShortcut("Ctrl+Z")
        redo_action.setShortcut("Ctrl+Y")
        cut_action.setShortcut("Ctrl+X")
        copy_action.setShortcut("Ctrl+C")
        paste_action.setShortcut("Ctrl+V")
        duplicate_action.setShortcut("Ctrl+D")
        consecutive_copy_action.setShortcut("Ctrl+Shift+C")
        select_all_action.setShortcut("Ctrl+A")
        delete_action.setShortcut("Del")

        # Add actions to the Edit menu
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(duplicate_action)
        edit_menu.addAction(consecutive_copy_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)
        edit_menu.addAction(delete_action)
        edit_menu.addSeparator()
        edit_menu.addAction(stacking_order_action)
        edit_menu.addAction(align_action)
        edit_menu.addAction(wrap_action)
        edit_menu.addAction(flip_action)


        # --- Search / replace ---
        search_replace_menu = menu_bar.addMenu("&Search/Replace")
        
        tag_search_icon = qta.icon('fa5s.tag', 'fa5s.search', options=[{'color': '#34a853'}, {'color': '#4285f4', 'scale_factor': 0.5, 'offset': (0.1, -0.1)}])
        tag_list_icon = qta.icon('fa5s.tags', options=[{'color': '#34a853'}])
        text_list_icon = qta.icon('fa5s.list-alt', options=[{'color': '#4285f4'}])
        batch_edit_icon = qta.icon('fa5s.edit', options=[{'color': '#fbbc05'}])
        data_browser_icon = qta.icon('fa5s.database', 'fa5s.search', options=[{'color': '#5f6368'}, {'color': '#4285f4', 'scale_factor': 0.4, 'offset': (0.1, -0.1)}])
        ip_address_list_icon = qta.icon('fa5s.ethernet', options=[{'color': '#4285f4'}])

        tag_search_action = QAction(tag_search_icon,"Tag Search", self)
        tag_list_action = QAction(tag_list_icon, "Tag List", self)
        text_list_action = QAction(text_list_icon,"Text List", self)
        batch_edit_action = QAction(batch_edit_icon, "Batch Edit",self)
        data_browser_action = QAction(data_browser_icon,"Data Browser",self)
        ip_address_list_action = QAction(ip_address_list_icon,"IP Address List",self)

        search_replace_menu.addAction(tag_search_action)
        search_replace_menu.addAction(tag_list_action)
        search_replace_menu.addAction(text_list_action)
        search_replace_menu.addSeparator()
        search_replace_menu.addAction(batch_edit_action)
        search_replace_menu.addAction(data_browser_action)
        search_replace_menu.addAction(ip_address_list_action)


        # --- View ---
        view_menu = menu_bar.addMenu("&View")
        
        preview_icon = qta.icon('fa5s.eye', 'fa5.eye', options=[{'color': '#bbdefb'}, {'color': '#4285f4'}])
        state_number_icon = qta.icon('fa5s.exchange-alt', options=[{'color': '#4285f4'}])
        tool_bar_icon = qta.icon('fa5s.wrench', 'fa5s.cog', options=[{'color': '#5f6368'}, {'color': '#9aa0a6', 'scale_factor': 0.7, 'offset': (0.2, 0.2)}])
        docking_window_icon = qta.icon('fa5.window-restore', 'fa5s.window-restore', options=[{'color': '#bbdefb'}, {'color': '#5f6368'}])
        display_item_icon = qta.icon('fa5s.paint-brush', options=[{'color':'#4285f4'}])
        object_snap_icon = qta.icon('fa5s.magnet', options=[{'color': '#ea4335'}])
        zoom_icon = qta.icon('fa5s.search-plus', options=[{'color': '#4285f4'}])

        preview_action = QAction(preview_icon,"Preview", self)
        state_number_action = QAction(state_number_icon,"State No.", self)
        tool_bar_action = QAction(tool_bar_icon,"Tool Bar", self)
        docking_window_action = QAction(docking_window_icon,"Docking Window", self)
        display_item_action = QAction(display_item_icon, "Display Item", self)
        object_snap_action = QAction(object_snap_icon,"Object Snap", self)
        zoom_action = QAction(zoom_icon,"Zoom", self)

        view_menu.addAction(preview_action)
        view_menu.addAction(state_number_action)
        view_menu.addAction(tool_bar_action)
        view_menu.addAction(docking_window_action)
        view_menu.addAction(display_item_action)
        view_menu.addAction(object_snap_action)
        view_menu.addAction(zoom_action)



        # --- Screen ---
        screen_menu = menu_bar.addMenu("&Screen")
        
        new_screen_icon = qta.icon('fa5s.desktop', 'fa5s.plus', options=[{'color': '#5f6368'}, {'color': '#34a853', 'scale_factor': 0.5}])
        open_screen_icon = qta.icon('fa5s.desktop', 'fa5s.folder-open', options=[{'color': '#5f6368'}, {'color': '#fbbc05', 'scale_factor': 0.5, 'offset': (0.1, 0.1)}])
        close_screen_icon = qta.icon('fa5s.desktop', 'fa5s.times-circle', options=[{'color': '#5f6368'}, {'color': '#ea4335', 'scale_factor': 0.5}])
        close_all_screens_icon = qta.icon('fa5.window-close', 'fa5s.window-close', options=[{'color':'#ea4335'}, {'color':'#c5221f'}])
        screen_design_icon = qta.icon('fa5s.palette', options=[{'color': '#4285f4'}])
        screen_property_icon = qta.icon('fa5s.cog', options=[{'color': '#5f6368'}])

        new_screen_action = QAction(new_screen_icon,"New Screen", self)
        open_screen_action = QAction(open_screen_icon, "Open Screen", self)
        close_screen_action = QAction(close_screen_icon, "Close Screen", self)
        close_all_screens_action = QAction(close_all_screens_icon, "Close All Screens", self)
        screen_design_action = QAction(screen_design_icon, "Screen Design...", self)
        screen_property_action = QAction(screen_property_icon, "Screen Property...", self)

        screen_menu.addAction(new_screen_action)
        screen_menu.addAction(open_screen_action)
        screen_menu.addAction(close_screen_action)
        screen_menu.addAction(close_all_screens_action)
        screen_menu.addSeparator()
        screen_menu.addAction(screen_design_action)
        screen_menu.addAction(screen_property_action)


        # --- Common ---
        common_menu = menu_bar.addMenu("&Common")
        
        environment_icon = qta.icon('fa5s.cogs', options=[{'color':'#5f6368'}])
        ethernet_icon = qta.icon('fa5s.network-wired', options=[{'color':'#4285f4'}])
        controller_icon = qta.icon('fa5s.gamepad', options=[{'color':'#5f6368'}])
        peripheral_device_icon = qta.icon('fa5s.plug', options=[{'color':'#34a853'}])
        tags_icon = qta.icon('fa5s.tags', options=[{'color':'#34a853'}])
        comment_icon = qta.icon('fa5s.comment-dots', options=[{'color':'#fbbc05'}])
        alarm_icon = qta.icon('fa5s.bell', options=[{'color':'#ea4335'}])
        logging_icon = qta.icon('fa5s.file-medical-alt', options=[{'color':'#4285f4'}])
        script_icon = qta.icon('fa5s.code', options=[{'color':'#5f6368'}])
        tags_data_transfer_icon = qta.icon('fa5s.exchange-alt', options=[{'color':'#4285f4'}])
        trigger_action_icon = qta.icon('fa5s.bolt', options=[{'color':'#fbbc05'}])
        time_action_icon = qta.icon('fa5s.clock', options=[{'color':'#4285f4'}])

        environment_action = QAction(environment_icon, "Environment", self)
        ethernet_action = QAction(ethernet_icon, "Ethernet", self)
        controller_action = QAction(controller_icon, "Controller Setting", self)
        peripheral_device_action = QAction(peripheral_device_icon, "Peripheral Device", self)
        tags_action = QAction(tags_icon, "Tags", self)
        comment_action = QAction(comment_icon, "Comment", self)
        alarm_action = QAction(alarm_icon, "Alarm", self)
        logging_action = QAction(logging_icon, "Logging..", self)
        script_action = QAction(script_icon, "Script", self)
        tags_data_transfer_action = QAction(tags_data_transfer_icon, "Tags Data Transfer", self)
        trigger_action_action = QAction(trigger_action_icon, "Trigger Action..", self)
        time_action = QAction(time_action_icon, "Time Action..", self)

        common_menu.addAction(environment_action)
        common_menu.addAction(ethernet_action)
        common_menu.addAction(controller_action)
        common_menu.addAction(peripheral_device_action)
        common_menu.addSeparator()
        common_menu.addAction(tags_action)
        common_menu.addAction(comment_action)
        common_menu.addAction(alarm_action)
        common_menu.addAction(logging_action)
        common_menu.addSeparator()
        common_menu.addAction(script_action)
        common_menu.addAction(tags_data_transfer_action)
        common_menu.addAction(trigger_action_action)
        common_menu.addAction(time_action)



        # --- Figure ---
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

        text_figure_action = QAction(text_figure_icon, "Text", self)
        line_figure_action = QAction(line_figure_icon, "Line", self)
        polyline_figure_action = QAction(polyline_figure_icon, "Polyline", self)
        rectangle_figure_action = QAction(rectangle_figure_icon, "Rectangle", self)
        polygon_figure_action = QAction(polygon_figure_icon, "Polygon", self)
        circle_figure_action = QAction(circle_figure_icon, "Circle", self)
        arc_figure_action = QAction(arc_figure_icon, "Arc", self)
        sector_figure_action = QAction(sector_figure_icon, "Sector", self)
        table_figure_action = QAction(table_figure_icon, "Table", self)
        scale_figure_action = QAction(scale_figure_icon, "Scale", self)
        image_figure_action = QAction(image_figure_icon, "Image", self)
        dxf_figure_action = QAction(dxf_figure_icon, "DXF", self)
        
        figure_menu.addAction(text_figure_action)
        figure_menu.addAction(line_figure_action)
        figure_menu.addAction(polyline_figure_action)
        figure_menu.addAction(rectangle_figure_action)
        figure_menu.addAction(polygon_figure_action)
        figure_menu.addAction(circle_figure_action)
        figure_menu.addAction(arc_figure_action)
        figure_menu.addAction(sector_figure_action)
        figure_menu.addAction(table_figure_action)
        figure_menu.addAction(scale_figure_action)
        figure_menu.addAction(image_figure_action)
        figure_menu.addAction(dxf_figure_action)



        # --- Object ---
        object_menu = menu_bar.addMenu("&Object")
        
        button_object_icon = qta.icon('fa5s.hand-pointer', options=[{'color':'#4285f4'}])
        lamp_object_icon = qta.icon('fa5s.lightbulb', options=[{'color':'#fbbc05'}])
        numerical_object_icon = qta.icon('fa5s.hashtag', options=[{'color':'#5f6368'}])
        text_object_icon = qta.icon('fa5s.i-cursor', options=[{'color':'#5f6368'}])
        date_time_object_icon = qta.icon('fa5s.calendar-alt', options=[{'color':'#4285f4'}])
        comment_object_icon = qta.icon('fa5s.comment-alt', options=[{'color':'#fbbc05'}])
        image_object_icon = qta.icon('fa5s.file-image', options=[{'color':'#4285f4'}])
        video_object_icon = qta.icon('fa5s.video', options=[{'color':'#ea4335'}])
        animation_object_icon = qta.icon('fa5s.film', options=[{'color':'#5f6368'}])
        historical_data_object_icon = qta.icon('fa5s.history', options=[{'color':'#5f6368'}])
        alarm_object_icon = qta.icon('mdi6.bell-badge', 'fa5s.bell', options=[{'color':'#ea4335'}, {'color':'#c5221f'}])
        recipe_object_icon = qta.icon('fa5s.book', options=[{'color':'#34a853'}])
        graph_object_icon = qta.icon('fa5s.chart-bar', options=[{'color':'#4285f4'}])
        graphical_meter_object_icon = qta.icon('fa5s.tachometer-alt', options=[{'color':'#5f6368'}])
        slider_object_icon = qta.icon('fa5s.sliders-h', options=[{'color':'#5f6368'}])
        document_object_icon = qta.icon('fa5s.file-word', options=[{'color':'#4285f4'}])
        web_browser_object_icon = qta.icon('fa5s.globe', options=[{'color':'#4285f4'}])
        
        button_object_action = QAction(button_object_icon, "Button", self)
        lamp_object_action = QAction(lamp_object_icon, "Lamp", self)
        numerical_object_action = QAction(numerical_object_icon, "Numerical Display/Input", self)
        text_object_action = QAction(text_object_icon, "Text Display/Input", self)
        date_time_object_action = QAction(date_time_object_icon, "Date/Time", self)
        comment_object_action = QAction(comment_object_icon, "Comment", self)
        image_object_action = QAction(image_object_icon, "Image", self)
        video_object_action = QAction(video_object_icon, "Video", self)
        animation_object_action = QAction(animation_object_icon, "Animation", self)
        historical_data_object_action = QAction(historical_data_object_icon, "Historical Data", self)
        alarm_object_action = QAction(alarm_object_icon, "Alarm", self)
        recipe_object_action = QAction(recipe_object_icon, "Recipe", self)
        graph_object_action = QAction(graph_object_icon, "Graph", self)
        graphical_meter_object_action = QAction(graphical_meter_object_icon, "Graphical Meter", self)
        slider_object_action = QAction(slider_object_icon, "Slider", self)
        document_object_action = QAction(document_object_icon, "Document", self)
        web_browser_object_action = QAction(web_browser_object_icon, "Web Browser", self)
        
        object_menu.addAction(button_object_action)
        object_menu.addAction(lamp_object_action)
        object_menu.addAction(numerical_object_action)
        object_menu.addAction(text_object_action)
        object_menu.addAction(date_time_object_action)
        object_menu.addAction(comment_object_action)
        object_menu.addAction(image_object_action)
        object_menu.addAction(video_object_action)
        object_menu.addAction(animation_object_action)
        object_menu.addAction(historical_data_object_action)
        object_menu.addAction(alarm_object_action)
        object_menu.addAction(recipe_object_action)
        object_menu.addAction(graph_object_action)
        object_menu.addAction(graphical_meter_object_action)
        object_menu.addAction(slider_object_action)
        object_menu.addAction(document_object_action)
        object_menu.addAction(web_browser_object_action)