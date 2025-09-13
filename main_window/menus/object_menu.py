from PyQt6.QtGui import QAction
import qtawesome as qta

class ObjectMenu:
    """
    Creates the 'Object' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        self.main_window = main_window
        object_menu = menu_bar.addMenu("&Object")
        
        # --- Button Submenu ---
        self.button_object_icon = qta.icon('fa5s.hand-pointer', options=[{'color':'#4285f4'}])
        button_menu = object_menu.addMenu(self.button_object_icon, "&Button")
        push_button_sq_icon = qta.icon('fa5s.stop', options=[{'color':'#4285f4'}])
        push_button_ci_icon = qta.icon('fa5s.circle', options=[{'color':'#4285f4'}])
        toggle_button_icon = qta.icon('fa5s.toggle-on', options=[{'color': '#34a853'}])
        checkbox_icon = qta.icon('fa5s.check-square', options=[{'color': '#4285f4'}])
        radio_button_icon = qta.icon('fa5s.dot-circle', options=[{'color': '#4285f4'}])
        self.push_button_sq_action = QAction(push_button_sq_icon, "Push Button Square", self.main_window)
        self.push_button_ci_action = QAction(push_button_ci_icon, "Push Button Circle", self.main_window)
        self.toggle_button_action = QAction(toggle_button_icon, "Toggle Button", self.main_window)
        self.checkbox_action = QAction(checkbox_icon, "Check Box", self.main_window)
        self.radio_button_action = QAction(radio_button_icon, "Radio Button", self.main_window)
        self.button_actions = [self.push_button_sq_action, self.push_button_ci_action, self.toggle_button_action, self.checkbox_action, self.radio_button_action]
        button_menu.addActions(self.button_actions)
        
        # --- Lamp Submenu ---
        self.lamp_object_icon = qta.icon('fa5s.lightbulb', options=[{'color':'#fbbc05'}])
        lamp_menu = object_menu.addMenu(self.lamp_object_icon, "Lamp")
        self.bit_lamp_action = QAction(qta.icon('fa5s.lightbulb', options=[{'color':'#34a853'}]), "Bit Lamp", self.main_window)
        self.word_lamp_action = QAction(qta.icon('fa5s.lightbulb', options=[{'color':'#4285f4'}]), "Word Lamp", self.main_window)
        self.border_lamp_action = QAction(qta.icon('fa5s.lightbulb', 'fa5.square', options=[{'color':'#fbbc05'}, {'color':'#5f6368', 'opacity':0.2}]), "Border Lamp", self.main_window)
        self.lamp_actions = [self.bit_lamp_action, self.word_lamp_action, self.border_lamp_action]
        lamp_menu.addActions(self.lamp_actions)
        
        # --- Numerical Display/Input Submenu ---
        self.numerical_object_icon = qta.icon('fa5s.hashtag', options=[{'color':'#5f6368'}])
        numerical_menu = object_menu.addMenu(self.numerical_object_icon, "Numerical Display/Input")
        self.numerical_action = QAction(qta.icon('fa5s.calculator'), "Numerical", self.main_window)
        self.spin_box_action = QAction(qta.icon('mdi6.numeric'), "Spin Box", self.main_window)
        self.numerical_actions = [self.numerical_action, self.spin_box_action]
        numerical_menu.addActions(self.numerical_actions)

        # --- Text Display/Input ---
        text_object_icon = qta.icon('fa5s.i-cursor', options=[{'color':'#5f6368'}])
        self.text_display_action = QAction(text_object_icon, "Text Display/Input", self.main_window)
        object_menu.addAction(self.text_display_action)

        # --- Date/Time Submenu ---
        self.date_time_object_icon = qta.icon('fa5s.calendar-alt', options=[{'color':'#4285f4'}])
        date_time_menu = object_menu.addMenu(self.date_time_object_icon, "Date/Time")
        self.date_display_action = QAction(qta.icon('fa5s.calendar-day'), "Date Display", self.main_window)
        self.time_display_action = QAction(qta.icon('fa5s.clock'), "Time Display", self.main_window)
        self.date_time_display_action = QAction(qta.icon('fa5s.calendar-alt'), "Date/Time Display", self.main_window)
        self.date_time_picker_action = QAction(qta.icon('mdi6.calendar-edit'), "Date/Time Picker", self.main_window)
        self.date_time_actions = [self.date_display_action, self.time_display_action, self.date_time_display_action, self.date_time_picker_action]
        date_time_menu.addActions(self.date_time_actions)

        # --- Comment Submenu ---
        self.comment_object_icon = qta.icon('fa5s.comment-alt', options=[{'color':'#fbbc05'}])
        comment_menu_object = object_menu.addMenu(self.comment_object_icon, "Comment")
        self.bit_comment_action = QAction(qta.icon('fa5s.comment', options=[{'color':'#34a853'}]), "Bit Comment", self.main_window)
        self.word_comment_action = QAction(qta.icon('fa5s.comment-dots', options=[{'color':'#4285f4'}]), "Word Comment", self.main_window)
        self.simple_comment_action = QAction(qta.icon('fa5s.comment-alt', options=[{'color':'#fbbc05'}]), "Simple Comment", self.main_window)
        self.comment_actions = [self.bit_comment_action, self.word_comment_action, self.simple_comment_action]
        comment_menu_object.addActions(self.comment_actions)

        # --- View Box Submenu ---
        self.view_box_icon = qta.icon('fa5s.box-open', options=[{'color':'#4285f4'}])
        view_box_menu = object_menu.addMenu(self.view_box_icon, "View Box")
        self.combo_box_action = QAction(qta.icon('fa5s.caret-square-down'), "Combo Box", self.main_window)
        self.check_list_box_action = QAction(qta.icon('fa5s.check-square'), "Check List Box", self.main_window)
        self.side_menu_bar_action = QAction(qta.icon('fa5s.bars'), "Side Menu Bar", self.main_window)
        self.group_box_action = QAction(qta.icon('fa5s.object-group'), "Group Box", self.main_window)
        self.data_grid_action = QAction(qta.icon('fa5s.table'), "Data Grid", self.main_window)
        self.list_box_action = QAction(qta.icon('fa5s.list-ul'), "List Box", self.main_window)
        self.splitter_panel_action = QAction(qta.icon('msc.split-horizontal'), "Splitter Panel", self.main_window)
        self.status_bar_action = QAction(qta.icon('mdi6.application-outline'), "Status Bar", self.main_window)
        self.tab_view_action = QAction(qta.icon('fa5s.folder-plus'), "Tab View", self.main_window)
        self.tree_view_action = QAction(qta.icon('fa5s.sitemap'), "Tree View", self.main_window)
        self.scroll_bar_action = QAction(qta.icon('fa5s.sliders-h'), "Scroll Bar", self.main_window)
        self.view_box_actions = [self.combo_box_action, self.check_list_box_action, self.side_menu_bar_action, self.group_box_action, self.data_grid_action, self.list_box_action, self.splitter_panel_action, self.status_bar_action, self.tab_view_action, self.tree_view_action, self.scroll_bar_action]
        view_box_menu.addActions(self.view_box_actions)

        # --- Other Objects (Single Actions) ---
        image_object_icon = qta.icon('fa5s.file-image', options=[{'color':'#4285f4'}])
        video_object_icon = qta.icon('fa5s.video', options=[{'color':'#ea4335'}])
        self.image_action = QAction(image_object_icon, "Image", self.main_window)
        self.video_action = QAction(video_object_icon, "Video", self.main_window)
        object_menu.addActions([self.image_action, self.video_action])

        # --- Animation Submenu ---
        self.animation_object_icon = qta.icon('fa5s.film', options=[{'color':'#5f6368'}])
        animation_menu = object_menu.addMenu(self.animation_object_icon, "Animation")
        self.progress_bar_action = QAction(qta.icon('fa5s.spinner'), "Progress Bar", self.main_window)
        self.tower_light_action = QAction(qta.icon('mdi6.traffic-light'), "Tower Light", self.main_window)
        self.gear_action = QAction(qta.icon('fa5s.cog'), "Gear", self.main_window)
        self.robot_action = QAction(qta.icon('fa5s.robot'), "Robot", self.main_window)
        self.conveyor_action = QAction("Conveyor", self.main_window)
        self.fan_action = QAction(qta.icon('mdi6.fan'), "Fan", self.main_window)
        self.printer_action = QAction(qta.icon('fa5s.print'), "Printer", self.main_window)
        self.animation_actions = [self.progress_bar_action, self.tower_light_action, self.gear_action, self.robot_action, self.conveyor_action, self.fan_action, self.printer_action]
        animation_menu.addActions(self.animation_actions)

        # --- Historical Data (Single Action) ---
        historical_data_object_icon = qta.icon('fa5s.history', options=[{'color':'#5f6368'}])
        self.historical_data_action = QAction(historical_data_object_icon, "Historical Data", self.main_window)
        object_menu.addAction(self.historical_data_action)

        # --- Alarm Submenu ---
        self.alarm_object_icon = qta.icon('mdi6.bell-badge', 'fa5s.bell', options=[{'color':'#ea4335'}, {'color':'#c5221f'}])
        alarm_menu_object = object_menu.addMenu(self.alarm_object_icon, "Alarm")
        self.simple_alarm_action = QAction(qta.icon('fa5s.bell', options=[{'color':'#fbbc05'}]), "Simple Alarm", self.main_window)
        self.user_alarm_action = QAction(qta.icon('fa5s.user-clock', options=[{'color':'#ea4335'}]), "User Alarm", self.main_window)
        self.system_alarm_action = QAction(qta.icon('fa5s.cog', options=[{'color':'#ea4335'}]), "System Alarm", self.main_window)
        self.alarm_actions = [self.simple_alarm_action, self.user_alarm_action, self.system_alarm_action]
        alarm_menu_object.addActions(self.alarm_actions)

        # --- Recipe (Single Action) ---
        recipe_object_icon = qta.icon('fa5s.book', options=[{'color':'#34a853'}])
        self.recipe_action = QAction(recipe_object_icon, "Recipe", self.main_window)
        object_menu.addAction(self.recipe_action)
        
        # --- Graph Submenu ---
        self.graph_object_icon = qta.icon('fa5s.chart-bar', options=[{'color':'#4285f4'}])
        graph_menu = object_menu.addMenu(self.graph_object_icon, "Graph")
        self.line_graph_action = QAction(qta.icon('fa5s.chart-line'), "Line", self.main_window)
        self.trend_graph_action = QAction(qta.icon('mdi6.chart-timeline-variant'), "Trend", self.main_window)
        self.bar_graph_action = QAction(qta.icon('fa5s.chart-bar'), "Bar", self.main_window)
        self.pie_graph_action = QAction(qta.icon('fa5s.chart-pie'), "Pie", self.main_window)
        self.scatter_graph_action = QAction(qta.icon('mdi6.chart-scatter-plot'), "Scatter", self.main_window)
        self.combo_graph_action = QAction(qta.icon('mdi6.chart-multiple'), "Combo", self.main_window)
        self.graph_actions = [self.line_graph_action, self.trend_graph_action, self.bar_graph_action, self.pie_graph_action, self.scatter_graph_action, self.combo_graph_action]
        graph_menu.addActions(self.graph_actions)

        # --- Graphical Meter Submenu ---
        self.graphical_meter_object_icon = qta.icon('fa5s.tachometer-alt', options=[{'color':'#5f6368'}])
        graphical_meter_menu = object_menu.addMenu(self.graphical_meter_object_icon, "Graphical Meter")
        self.sector_meter_action = QAction(qta.icon('mdi6.gauge'), "Sector Meter", self.main_window)
        self.semi_circle_meter_action = QAction(qta.icon('mdi6.gauge-low'), "Semi Circle Meter", self.main_window)
        self.bar_meter_action = QAction(qta.icon('mdi6.chart-gantt'), "Bar Meter", self.main_window)
        self.graphical_meter_actions = [self.sector_meter_action, self.semi_circle_meter_action, self.bar_meter_action]
        graphical_meter_menu.addActions(self.graphical_meter_actions)

        # --- Other Objects (Single Actions) ---
        slider_object_icon = qta.icon('fa5s.sliders-h', options=[{'color':'#5f6368'}])
        document_object_icon = qta.icon('fa5s.file-word', options=[{'color':'#4285f4'}])
        web_browser_object_icon = qta.icon('fa5s.globe', options=[{'color':'#4285f4'}])
        self.slider_action = QAction(slider_object_icon, "Slider", self.main_window)
        self.document_action = QAction(document_object_icon, "Document", self.main_window)
        self.web_browser_action = QAction(web_browser_object_icon, "Web Browser", self.main_window)
        object_menu.addActions([self.slider_action, self.document_action, self.web_browser_action])

