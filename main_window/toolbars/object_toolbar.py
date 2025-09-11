from PyQt6.QtWidgets import QToolBar, QToolButton, QMenu
from PyQt6.QtCore import Qt

class ObjectToolbar(QToolBar):
    def __init__(self, main_window, object_menu):
        super().__init__("Object", main_window)
        self.main_window = main_window
        self.object_menu = object_menu
        self.setMovable(True)

        # Create and add tool buttons with popup menus
        self.add_popup_button(self.object_menu.button_actions, self.object_menu.button_object_icon)
        self.add_popup_button(self.object_menu.lamp_actions, self.object_menu.lamp_object_icon)
        self.add_popup_button(self.object_menu.numerical_actions, self.object_menu.numerical_object_icon)
        self.addAction(self.object_menu.text_display_action)
        self.add_popup_button(self.object_menu.date_time_actions, self.object_menu.date_time_object_icon)
        self.add_popup_button(self.object_menu.comment_actions, self.object_menu.comment_object_icon)
        self.add_popup_button(self.object_menu.view_box_actions, self.object_menu.view_box_icon)
        self.addAction(self.object_menu.image_action)
        self.addAction(self.object_menu.video_action)
        self.add_popup_button(self.object_menu.animation_actions, self.object_menu.animation_object_icon)
        self.addAction(self.object_menu.historical_data_action)
        self.add_popup_button(self.object_menu.alarm_actions, self.object_menu.alarm_object_icon)
        self.addAction(self.object_menu.recipe_action)
        self.add_popup_button(self.object_menu.graph_actions, self.object_menu.graph_object_icon)
        self.add_popup_button(self.object_menu.graphical_meter_actions, self.object_menu.graphical_meter_object_icon)
        self.addAction(self.object_menu.slider_action)
        self.addAction(self.object_menu.document_action)
        self.addAction(self.object_menu.web_browser_action)

    def add_popup_button(self, actions, icon):
        """Creates a QToolButton with a popup menu for the given actions."""
        if not actions:
            return

        # Use the first action to set the button's properties
        first_action = actions[0]
        
        tool_button = QToolButton()
        tool_button.setIcon(icon)
        tool_button.setToolTip(first_action.toolTip() or first_action.text().split(' ')[0])
        tool_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        menu = QMenu(self)
        menu.addActions(actions)
        tool_button.setMenu(menu)

        self.addWidget(tool_button)

