# main_window\menus\object_menu.py
from PySide6.QtGui import QAction
from ..services.icon_service import IconService

class ObjectMenu:
    """
    Creates the 'Object' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        self.main_window = main_window
        object_menu = menu_bar.addMenu("&Object")
        
        # Initialize list to hold all object actions for grouping later
        self.all_actions = []

        # --- Button Submenu ---
        self.button_object_icon = IconService.get_icon('object-button')
        button_menu = object_menu.addMenu(self.button_object_icon, "&Button")
        push_button_sq_icon = IconService.get_icon('object-push-button-sq')
        push_button_ci_icon = IconService.get_icon('object-push-button-ci')
        toggle_button_icon = IconService.get_icon('object-toggle-button')
        checkbox_icon = IconService.get_icon('object-checkbox')
        radio_button_icon = IconService.get_icon('object-radio-button')
        selector_switch_icon = IconService.get_icon('object-selector-switch')
        self.push_button_sq_action = QAction(push_button_sq_icon, "Push Button Square", self.main_window)
        self.push_button_ci_action = QAction(push_button_ci_icon, "Push Button Circle", self.main_window)
        self.toggle_button_action = QAction(toggle_button_icon, "Toggle Button", self.main_window)
        self.checkbox_action = QAction(checkbox_icon, "Check Box", self.main_window)
        self.radio_button_action = QAction(radio_button_icon, "Radio Button", self.main_window)
        self.selector_switch_action = QAction(selector_switch_icon, "Selector Switch", self.main_window)
        self.button_actions = [self.push_button_sq_action, self.push_button_ci_action, self.toggle_button_action, self.checkbox_action, self.radio_button_action, self.selector_switch_action]
        button_menu.addActions(self.button_actions)
        self.all_actions.extend(self.button_actions)
        
        # --- Lamp Submenu ---
        self.lamp_object_icon = IconService.get_icon('object-lamp')
        lamp_menu = object_menu.addMenu(self.lamp_object_icon, "Lamp")
        self.bit_lamp_action = QAction(IconService.get_icon('object-bit-lamp'), "Bit Lamp", self.main_window)
        self.word_lamp_action = QAction(IconService.get_icon('object-word-lamp'), "Word Lamp", self.main_window)
        self.border_lamp_action = QAction(IconService.get_icon('object-border-lamp'), "Border Lamp", self.main_window)
        self.lamp_actions = [self.bit_lamp_action, self.word_lamp_action, self.border_lamp_action]
        lamp_menu.addActions(self.lamp_actions)
        self.all_actions.extend(self.lamp_actions)
        
        # --- Numerical Display/Input Submenu ---
        self.numerical_object_icon = IconService.get_icon('object-numerical')
        numerical_menu = object_menu.addMenu(self.numerical_object_icon, "Numerical Display/Input")
        self.numerical_action = QAction(IconService.get_icon('object-calculator'), "Numerical", self.main_window)
        self.spin_box_action = QAction(IconService.get_icon('object-spin-box'), "Spin Box", self.main_window)
        self.numerical_actions = [self.numerical_action, self.spin_box_action]
        numerical_menu.addActions(self.numerical_actions)
        self.all_actions.extend(self.numerical_actions)

        # --- Text Display/Input ---
        text_object_icon = IconService.get_icon('object-text-display')
        self.text_display_action = QAction(text_object_icon, "Text Display/Input", self.main_window)
        object_menu.addAction(self.text_display_action)
        self.all_actions.append(self.text_display_action)

        # --- Date/Time Submenu ---
        self.date_time_object_icon = IconService.get_icon('object-datetime')
        date_time_menu = object_menu.addMenu(self.date_time_object_icon, "Date/Time")
        self.date_display_action = QAction(IconService.get_icon('object-date-display'), "Date Display", self.main_window)
        self.time_display_action = QAction(IconService.get_icon('object-time-display'), "Time Display", self.main_window)
        self.date_time_display_action = QAction(IconService.get_icon('object-datetime-display'), "Date/Time Display", self.main_window)
        self.date_time_picker_action = QAction(IconService.get_icon('object-datetime-picker'), "Date/Time Picker", self.main_window)
        self.date_time_actions = [self.date_display_action, self.time_display_action, self.date_time_display_action, self.date_time_picker_action]
        date_time_menu.addActions(self.date_time_actions)
        self.all_actions.extend(self.date_time_actions)

        # --- Comment Submenu ---
        self.comment_object_icon = IconService.get_icon('object-comment')
        comment_menu_object = object_menu.addMenu(self.comment_object_icon, "Comment")
        self.bit_comment_action = QAction(IconService.get_icon('object-bit-comment'), "Bit Comment", self.main_window)
        self.word_comment_action = QAction(IconService.get_icon('object-word-comment'), "Word Comment", self.main_window)
        self.simple_comment_action = QAction(IconService.get_icon('object-simple-comment'), "Simple Comment", self.main_window)
        self.comment_actions = [self.bit_comment_action, self.word_comment_action, self.simple_comment_action]
        comment_menu_object.addActions(self.comment_actions)
        self.all_actions.extend(self.comment_actions)

        # --- View Box Submenu ---
        self.view_box_icon = IconService.get_icon('object-view-box')
        view_box_menu = object_menu.addMenu(self.view_box_icon, "View Box")
        self.combo_box_action = QAction(IconService.get_icon('object-combo-box'), "Combo Box", self.main_window)
        self.check_list_box_action = QAction(IconService.get_icon('object-check-list-box'), "Check List Box", self.main_window)
        self.side_menu_bar_action = QAction(IconService.get_icon('object-side-menu-bar'), "Side Menu Bar", self.main_window)
        self.group_box_action = QAction(IconService.get_icon('object-group-box'), "Group Box", self.main_window)
        self.data_grid_action = QAction(IconService.get_icon('object-data-grid'), "Data Grid", self.main_window)
        self.list_box_action = QAction(IconService.get_icon('object-list-box'), "List Box", self.main_window)
        self.splitter_panel_action = QAction(IconService.get_icon('object-splitter-panel'), "Splitter Panel", self.main_window)
        self.status_bar_action = QAction(IconService.get_icon('object-status-bar'), "Status Bar", self.main_window)
        self.tab_view_action = QAction(IconService.get_icon('object-tab-view'), "Tab View", self.main_window)
        self.tree_view_action = QAction(IconService.get_icon('object-tree-view'), "Tree View", self.main_window)
        self.scroll_bar_action = QAction(IconService.get_icon('object-scroll-bar'), "Scroll Bar", self.main_window)
        self.view_box_actions = [self.combo_box_action, self.check_list_box_action, self.side_menu_bar_action, self.group_box_action, self.data_grid_action, self.list_box_action, self.splitter_panel_action, self.status_bar_action, self.tab_view_action, self.tree_view_action, self.scroll_bar_action]
        view_box_menu.addActions(self.view_box_actions)
        self.all_actions.extend(self.view_box_actions)

        # --- Other Objects (Single Actions) ---
        image_object_icon = IconService.get_icon('object-image')
        video_object_icon = IconService.get_icon('object-video')
        self.image_action = QAction(image_object_icon, "Image", self.main_window)
        self.video_action = QAction(video_object_icon, "Video", self.main_window)
        object_menu.addActions([self.image_action, self.video_action])
        self.all_actions.extend([self.image_action, self.video_action])

        # --- Animation Submenu ---
        self.animation_object_icon = IconService.get_icon('object-animation')
        animation_menu = object_menu.addMenu(self.animation_object_icon, "Animation")
        self.progress_bar_action = QAction(IconService.get_icon('object-progress-bar'), "Progress Bar", self.main_window)
        self.tower_light_action = QAction(IconService.get_icon('object-tower-light'), "Tower Light", self.main_window)
        self.gear_action = QAction(IconService.get_icon('object-gear'), "Gear", self.main_window)
        self.robot_action = QAction(IconService.get_icon('object-robot'), "Robot", self.main_window)
        self.conveyor_action = QAction(IconService.get_icon('object-conveyor'), "Conveyor", self.main_window)
        self.fan_action = QAction(IconService.get_icon('object-fan'), "Fan", self.main_window)
        self.printer_action = QAction(IconService.get_icon('object-printer'), "Printer", self.main_window)
        self.animation_actions = [self.progress_bar_action, self.tower_light_action, self.gear_action, self.robot_action, self.conveyor_action, self.fan_action, self.printer_action]
        animation_menu.addActions(self.animation_actions)
        self.all_actions.extend(self.animation_actions)

        # --- Historical Data (Single Action) ---
        historical_data_object_icon = IconService.get_icon('object-historical-data')
        self.historical_data_action = QAction(historical_data_object_icon, "Historical Data", self.main_window)
        object_menu.addAction(self.historical_data_action)
        self.all_actions.append(self.historical_data_action)

        # --- Alarm Submenu ---
        self.alarm_object_icon = IconService.get_icon('object-alarm')
        alarm_menu_object = object_menu.addMenu(self.alarm_object_icon, "Alarm")
        self.simple_alarm_action = QAction(IconService.get_icon('object-simple-alarm'), "Simple Alarm", self.main_window)
        self.user_alarm_action = QAction(IconService.get_icon('object-user-alarm'), "User Alarm", self.main_window)
        self.system_alarm_action = QAction(IconService.get_icon('object-system-alarm'), "System Alarm", self.main_window)
        self.alarm_actions = [self.simple_alarm_action, self.user_alarm_action, self.system_alarm_action]
        alarm_menu_object.addActions(self.alarm_actions)
        self.all_actions.extend(self.alarm_actions)

        # --- Recipe (Single Action) ---
        recipe_object_icon = IconService.get_icon('object-recipe')
        self.recipe_action = QAction(recipe_object_icon, "Recipe", self.main_window)
        object_menu.addAction(self.recipe_action)
        self.all_actions.append(self.recipe_action)
        
        # --- Graph Submenu ---
        self.graph_object_icon = IconService.get_icon('object-graph')
        graph_menu = object_menu.addMenu(self.graph_object_icon, "Graph")
        self.line_graph_action = QAction(IconService.get_icon('object-line-graph'), "Line", self.main_window)
        self.trend_graph_action = QAction(IconService.get_icon('object-trend-graph'), "Trend", self.main_window)
        self.bar_graph_action = QAction(IconService.get_icon('object-bar-graph'), "Bar", self.main_window)
        self.pie_graph_action = QAction(IconService.get_icon('object-pie-graph'), "Pie", self.main_window)
        self.scatter_graph_action = QAction(IconService.get_icon('object-scatter-graph'), "Scatter", self.main_window)
        self.combo_graph_action = QAction(IconService.get_icon('object-combo-graph'), "Combo", self.main_window)
        self.graph_actions = [self.line_graph_action, self.trend_graph_action, self.bar_graph_action, self.pie_graph_action, self.scatter_graph_action, self.combo_graph_action]
        graph_menu.addActions(self.graph_actions)
        self.all_actions.extend(self.graph_actions)

        # --- Graphical Meter Submenu ---
        self.graphical_meter_object_icon = IconService.get_icon('object-graphical-meter')
        graphical_meter_menu = object_menu.addMenu(self.graphical_meter_object_icon, "Graphical Meter")
        self.sector_meter_action = QAction(IconService.get_icon('object-sector-meter'), "Sector Meter", self.main_window)
        self.semi_circle_meter_action = QAction(IconService.get_icon('object-semi-circle-meter'), "Semi Circle Meter", self.main_window)
        self.bar_meter_action = QAction(IconService.get_icon('object-bar-meter'), "Bar Meter", self.main_window)
        self.graphical_meter_actions = [self.sector_meter_action, self.semi_circle_meter_action, self.bar_meter_action]
        graphical_meter_menu.addActions(self.graphical_meter_actions)
        self.all_actions.extend(self.graphical_meter_actions)

        # --- Other Objects (Single Actions) ---
        slider_object_icon = IconService.get_icon('object-slider')
        document_object_icon = IconService.get_icon('object-document')
        web_browser_object_icon = IconService.get_icon('object-web-browser')
        self.slider_action = QAction(slider_object_icon, "Slider", self.main_window)
        self.document_action = QAction(document_object_icon, "Document", self.main_window)
        self.web_browser_action = QAction(web_browser_object_icon, "Web Browser", self.main_window)
        object_menu.addActions([self.slider_action, self.document_action, self.web_browser_action])
        self.all_actions.extend([self.slider_action, self.document_action, self.web_browser_action])

        # Make all actions checkable
        for action in self.all_actions:
            action.setCheckable(True)