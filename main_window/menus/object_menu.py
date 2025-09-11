from PyQt6.QtGui import QAction
import qtawesome as qta

class ObjectMenu:
    """
    Creates the 'Object' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        object_menu = menu_bar.addMenu("&Object")
        
        # Button Submenu
        button_object_icon = qta.icon('fa5s.hand-pointer', options=[{'color':'#4285f4'}])
        button_menu = object_menu.addMenu(button_object_icon, "&Button")
        push_button_sq_icon = qta.icon('fa5s.stop', 'fa5s.mouse-pointer', options=[{'color':'#4285f4'}, {'color':'white', 'scale_factor':0.5}])
        push_button_ci_icon = qta.icon('fa5s.circle', 'fa5s.mouse-pointer', options=[{'color':'#4285f4'}, {'color':'white', 'scale_factor':0.5}])
        toggle_button_icon = qta.icon('fa5s.toggle-on', options=[{'color': '#34a853'}])
        checkbox_icon = qta.icon('fa5s.check-square', options=[{'color': '#4285f4'}])
        radio_button_icon = qta.icon('fa5s.dot-circle', options=[{'color': '#4285f4'}])
        button_menu.addAction(QAction(push_button_sq_icon, "Push Button Square", main_window))
        button_menu.addAction(QAction(push_button_ci_icon, "Push Button Circle", main_window))
        button_menu.addAction(QAction(toggle_button_icon, "Toggle Button", main_window))
        button_menu.addAction(QAction(checkbox_icon, "Check Box", main_window))
        button_menu.addAction(QAction(radio_button_icon, "Radio Button", main_window))
        
        # Lamp Submenu
        lamp_object_icon = qta.icon('fa5s.lightbulb', options=[{'color':'#fbbc05'}])
        lamp_menu = object_menu.addMenu(lamp_object_icon, "Lamp")
        lamp_menu.addAction(QAction(qta.icon('fa5s.lightbulb', options=[{'color':'#34a853'}]), "Bit Lamp", main_window))
        lamp_menu.addAction(QAction(qta.icon('fa5s.lightbulb', options=[{'color':'#4285f4'}]), "Word Lamp", main_window))
        lamp_menu.addAction(QAction(qta.icon('fa5s.lightbulb', 'fa5.square', options=[{'color':'#fbbc05'}, {'color':'#5f6368', 'opacity':0.2}]), "Border Lamp", main_window))
        
        # Numerical Display/Input Submenu
        numerical_object_icon = qta.icon('fa5s.hashtag', options=[{'color':'#5f6368'}])
        numerical_menu = object_menu.addMenu(numerical_object_icon, "Numerical Display/Input")
        numerical_menu.addAction(QAction(qta.icon('fa5s.calculator'), "Numerical", main_window))
        numerical_menu.addAction(QAction(qta.icon('mdi6.numeric'), "Spin Box", main_window))

        # Text Display/Input
        text_object_icon = qta.icon('fa5s.i-cursor', options=[{'color':'#5f6368'}])
        object_menu.addAction(QAction(text_object_icon, "Text Display/Input", main_window))

        # Date/Time Submenu
        date_time_object_icon = qta.icon('fa5s.calendar-alt', options=[{'color':'#4285f4'}])
        date_time_menu = object_menu.addMenu(date_time_object_icon, "Date/Time")
        date_time_menu.addAction(QAction(qta.icon('fa5s.calendar-day'), "Date Display", main_window))
        date_time_menu.addAction(QAction(qta.icon('fa5s.clock'), "Time Display", main_window))
        date_time_menu.addAction(QAction(qta.icon('fa5s.calendar-alt'), "Date/Time Display", main_window))
        date_time_menu.addAction(QAction(qta.icon('mdi6.calendar-edit'), "Date/Time Picker", main_window))

        # Comment Submenu
        comment_object_icon = qta.icon('fa5s.comment-alt', options=[{'color':'#fbbc05'}])
        comment_menu_object = object_menu.addMenu(comment_object_icon, "Comment")
        comment_menu_object.addAction(QAction(qta.icon('fa5s.comment', options=[{'color':'#34a853'}]), "Bit Comment", main_window))
        comment_menu_object.addAction(QAction(qta.icon('fa5s.comment-dots', options=[{'color':'#4285f4'}]), "Word Comment", main_window))
        comment_menu_object.addAction(QAction(qta.icon('fa5s.comment-alt', options=[{'color':'#fbbc05'}]), "Simple Comment", main_window))

        # View Box Submenu
        view_box_icon = qta.icon('fa5s.box-open', options=[{'color':'#4285f4'}])
        view_box_menu = object_menu.addMenu(view_box_icon, "View Box")
        view_box_menu.addAction(QAction(qta.icon('fa5s.caret-square-down'), "Combo Box", main_window))
        view_box_menu.addAction(QAction(qta.icon('fa5s.check-square'), "Check List Box", main_window))
        view_box_menu.addAction(QAction(qta.icon('fa5s.bars'), "Side Menu Bar", main_window))
        view_box_menu.addAction(QAction(qta.icon('fa5s.object-group'), "Group Box", main_window))
        view_box_menu.addAction(QAction(qta.icon('fa5s.table'), "Data Grid", main_window))
        view_box_menu.addAction(QAction(qta.icon('fa5s.list-ul'), "List Box", main_window))
        view_box_menu.addAction(QAction(qta.icon('msc.split-horizontal'), "Splitter Panel", main_window))
        view_box_menu.addAction(QAction(qta.icon('mdi6.application-outline'), "Status Bar", main_window))
        view_box_menu.addAction(QAction(qta.icon('fa5s.folder-plus'), "Tab View", main_window))
        view_box_menu.addAction(QAction(qta.icon('fa5s.sitemap'), "Tree View", main_window))
        view_box_menu.addAction(QAction(qta.icon('fa5s.sliders-h'), "Scroll Bar", main_window))

        # Other Objects
        image_object_icon = qta.icon('fa5s.file-image', options=[{'color':'#4285f4'}])
        video_object_icon = qta.icon('fa5s.video', options=[{'color':'#ea4335'}])
        object_menu.addAction(QAction(image_object_icon, "Image", main_window))
        object_menu.addAction(QAction(video_object_icon, "Video", main_window))

        # Animation Submenu
        animation_object_icon = qta.icon('fa5s.film', options=[{'color':'#5f6368'}])
        animation_menu = object_menu.addMenu(animation_object_icon, "Animation")
        animation_menu.addAction(QAction(qta.icon('fa5s.spinner'), "Progress Bar", main_window))
        animation_menu.addAction(QAction(qta.icon('mdi6.traffic-light'), "Tower Light", main_window))
        animation_menu.addAction(QAction(qta.icon('fa5s.cog'), "Gear", main_window))
        animation_menu.addAction(QAction(qta.icon('fa5s.robot'), "Robot", main_window))
        animation_menu.addAction(QAction("Conveyor", main_window))
        animation_menu.addAction(QAction(qta.icon('mdi6.fan'), "Fan", main_window))
        animation_menu.addAction(QAction(qta.icon('fa5s.print'), "Printer", main_window))

        historical_data_object_icon = qta.icon('fa5s.history', options=[{'color':'#5f6368'}])
        object_menu.addAction(QAction(historical_data_object_icon, "Historical Data", main_window))

        # Alarm Submenu
        alarm_object_icon = qta.icon('mdi6.bell-badge', 'fa5s.bell', options=[{'color':'#ea4335'}, {'color':'#c5221f'}])
        alarm_menu_object = object_menu.addMenu(alarm_object_icon, "Alarm")
        alarm_menu_object.addAction(QAction(qta.icon('fa5s.bell', options=[{'color':'#fbbc05'}]), "Simple Alarm", main_window))
        alarm_menu_object.addAction(QAction(qta.icon('fa5s.user-clock', options=[{'color':'#ea4335'}]), "User Alarm", main_window))
        alarm_menu_object.addAction(QAction(qta.icon('fa5s.cog', options=[{'color':'#ea4335'}]), "System Alarm", main_window))

        recipe_object_icon = qta.icon('fa5s.book', options=[{'color':'#34a853'}])
        object_menu.addAction(QAction(recipe_object_icon, "Recipe", main_window))
        
        # Graph Submenu
        graph_object_icon = qta.icon('fa5s.chart-bar', options=[{'color':'#4285f4'}])
        graph_menu = object_menu.addMenu(graph_object_icon, "Graph")
        graph_menu.addAction(QAction(qta.icon('fa5s.chart-line'), "Line", main_window))
        graph_menu.addAction(QAction(qta.icon('mdi6.chart-timeline-variant'), "Trend", main_window))
        graph_menu.addAction(QAction(qta.icon('fa5s.chart-bar'), "Bar", main_window))
        graph_menu.addAction(QAction(qta.icon('fa5s.chart-pie'), "Pie", main_window))
        graph_menu.addAction(QAction(qta.icon('mdi6.chart-scatter-plot'), "Scatter", main_window))
        graph_menu.addAction(QAction(qta.icon('mdi6.chart-multiple'), "Combo", main_window))

        # Graphical Meter Submenu
        graphical_meter_object_icon = qta.icon('fa5s.tachometer-alt', options=[{'color':'#5f6368'}])
        graphical_meter_menu = object_menu.addMenu(graphical_meter_object_icon, "Graphical Meter")
        graphical_meter_menu.addAction(QAction(qta.icon('mdi6.gauge'), "Sector Meter", main_window))
        graphical_meter_menu.addAction(QAction(qta.icon('mdi6.gauge-low'), "Semi Circle Meter", main_window))
        graphical_meter_menu.addAction(QAction(qta.icon('mdi6.chart-gantt'), "Bar Meter", main_window))

        slider_object_icon = qta.icon('fa5s.sliders-h', options=[{'color':'#5f6368'}])
        document_object_icon = qta.icon('fa5s.file-word', options=[{'color':'#4285f4'}])
        web_browser_object_icon = qta.icon('fa5s.globe', options=[{'color':'#4285f4'}])
        object_menu.addAction(QAction(slider_object_icon, "Slider", main_window))
        object_menu.addAction(QAction(document_object_icon, "Document", main_window))
        object_menu.addAction(QAction(web_browser_object_icon, "Web Browser", main_window))

