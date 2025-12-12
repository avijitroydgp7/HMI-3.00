# main_window\toolbars\object_toolbar.py
from PySide6.QtWidgets import QToolBar, QToolButton, QMenu
from PySide6.QtCore import Qt

class ObjectToolbar(QToolBar):
    def __init__(self, main_window, object_menu):
        super().__init__("Object", main_window)
        self.main_window = main_window
        self.object_menu = object_menu
        self.setMovable(True)

        # Create and add tool buttons with popup menus
        self.add_popup_button(self.object_menu.button_actions, self.object_menu.button_object_icon, "Button")
        self.add_popup_button(self.object_menu.lamp_actions, self.object_menu.lamp_object_icon, "Lamp")
        self.add_popup_button(self.object_menu.numerical_actions, self.object_menu.numerical_object_icon, "Numerical Display/Input")
        self.addAction(self.object_menu.text_display_action)
        self.add_popup_button(self.object_menu.date_time_actions, self.object_menu.date_time_object_icon, "Date/Time")
        self.add_popup_button(self.object_menu.comment_actions, self.object_menu.comment_object_icon, "Comment")
        self.add_popup_button(self.object_menu.view_box_actions, self.object_menu.view_box_icon, "View Box")
        self.addAction(self.object_menu.image_action)
        self.addAction(self.object_menu.video_action)
        self.add_popup_button(self.object_menu.animation_actions, self.object_menu.animation_object_icon, "Animation")
        self.addAction(self.object_menu.historical_data_action)
        self.add_popup_button(self.object_menu.alarm_actions, self.object_menu.alarm_object_icon, "Alarm")
        self.addAction(self.object_menu.recipe_action)
        self.add_popup_button(self.object_menu.graph_actions, self.object_menu.graph_object_icon, "Graph")
        self.add_popup_button(self.object_menu.graphical_meter_actions, self.object_menu.graphical_meter_object_icon, "Graphical Meter")
        self.addAction(self.object_menu.slider_action)
        self.addAction(self.object_menu.document_action)
        self.addAction(self.object_menu.web_browser_action)

    def add_popup_button(self, actions, icon, tooltip):
        """Creates a QToolButton with a popup menu for the given actions."""
        if not actions:
            return
        
        tool_button = QToolButton()
        tool_button.setIcon(icon)
        tool_button.setToolTip(tooltip)
        tool_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        tool_button.setCheckable(True) # Enable checkable state for the button itself

        menu = QMenu(self)
        menu.addActions(actions)
        tool_button.setMenu(menu)

        # Function to update the main button when a sub-action is toggled
        def update_button_state():
            checked_action = None
            for action in actions:
                if action.isChecked():
                    checked_action = action
                    break
            
            if checked_action:
                # If a sub-action is checked, update icon and set button as checked
                tool_button.setIcon(checked_action.icon())
                tool_button.setToolTip(checked_action.text())
                tool_button.setChecked(True)
            else:
                # If no sub-action is checked (another tool selected elsewhere), uncheck button
                tool_button.setChecked(False)
                # We retain the last used icon here, which is standard behavior.
                # If you want to reset to the default group icon, uncomment the line below:
                # tool_button.setIcon(icon)

        # Connect the toggled signal of all child actions to the updater
        for action in actions:
            action.toggled.connect(update_button_state)

        self.addWidget(tool_button)