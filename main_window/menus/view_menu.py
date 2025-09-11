from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QWidgetAction
import qtawesome as qta

class ViewMenu:
    """
    Creates the 'View' menu and its actions.
    """
    def __init__(self, main_window, menu_bar):
        self.main_window = main_window
        view_menu = menu_bar.addMenu("&View")
        
        preview_icon = qta.icon('fa5s.eye', 'fa5.eye', options=[{'color': '#bbdefb'}, {'color': '#4285f4'}])
        state_number_icon = qta.icon('fa5s.exchange-alt', options=[{'color': '#4285f4'}])
        object_snap_icon = qta.icon('fa5s.magnet', options=[{'color': '#ea4335'}])

        view_menu.addAction(QAction(preview_icon,"Preview", self.main_window))
        view_menu.addAction(QAction(state_number_icon,"State No.", self.main_window))

        # Tool Bar Submenu
        tool_bar_icon = qta.icon('fa5s.wrench', 'fa5s.cog', options=[{'color': '#5f6368'}, {'color': '#9aa0a6', 'scale_factor': 0.7, 'offset': (0.2, 0.2)}])
        self.tool_bar_menu = view_menu.addMenu(tool_bar_icon, "Tool Bar")
        self.create_checkable_toolbar_actions()

        # Docking Window Submenu
        docking_window_icon = qta.icon('fa5.window-restore', 'fa5s.window-restore', options=[{'color': '#bbdefb'}, {'color': '#5f6368'}])
        self.docking_window_menu = view_menu.addMenu(docking_window_icon, "Docking Window")
        self.create_checkable_docking_actions()

        # Display Item Submenu
        display_item_icon = qta.icon('fa5s.paint-brush', options=[{'color':'#4285f4'}])
        display_item_menu = view_menu.addMenu(display_item_icon, "Display Item")
        display_item_menu.addAction(QAction(qta.icon('fa5s.tag'), "Tag", self.main_window))
        display_item_menu.addAction(QAction(qta.icon('fa5s.hashtag'), "Object ID", self.main_window))
        display_item_menu.addAction(QAction(qta.icon('fa5s.ruler-combined'), "Transform Line", self.main_window))
        display_item_menu.addAction(QAction(qta.icon('fa5s.hand-pointer'), "Click Area", self.main_window))
        
        # Object Snap Action
        object_snap_widget_action = QWidgetAction(self.main_window)
        object_snap_widget = QWidget()
        object_snap_layout = QHBoxLayout(object_snap_widget)
        object_snap_layout.setContentsMargins(4, 4, 4, 4)
        object_snap_layout.setSpacing(10)

        object_snap_icon_label = QLabel()
        object_snap_icon_label.setPixmap(object_snap_icon.pixmap(16, 16))

        object_snap_text_label = QLabel("Object Snap")

        object_snap_check_box = QCheckBox()
        object_snap_check_box.setChecked(True)

        object_snap_layout.addWidget(object_snap_icon_label)
        object_snap_layout.addWidget(object_snap_text_label)
        object_snap_layout.addStretch()
        object_snap_layout.addWidget(object_snap_check_box)

        object_snap_widget_action.setDefaultWidget(object_snap_widget)
        view_menu.addAction(object_snap_widget_action)

        # Zoom Submenu
        zoom_icon = qta.icon('fa5s.search-plus', options=[{'color': '#4285f4'}])
        zoom_menu = view_menu.addMenu(zoom_icon, "Zoom")
        zoom_menu.addAction(QAction(qta.icon('fa5s.compress'), "Fit Screen", self.main_window))
        zoom_menu.addSeparator()
        zoom_levels = ["20%", "50%", "75%", "100%", "125%", "150%", "200%", "250%", "300%", "400%", "500%", "600%", "700%", "800%", "900%", "1000%"]
        for level in zoom_levels:
            zoom_menu.addAction(QAction(level, self.main_window))

    def create_checkable_toolbar_actions(self):
        """Creates and adds checkable widget actions to the Tool Bar submenu."""
        toolbar_items = [
            ("Window Display", qta.icon('fa5s.desktop')),
            ("View", qta.icon('fa5s.eye')),
            ("Screen", qta.icon('fa5s.columns')),
            ("Edit", qta.icon('fa5s.edit')),
            ("Alignment", qta.icon('fa5s.align-center')),
            ("Figure", qta.icon('fa5s.shapes')),
            ("Object", qta.icon('fa5s.cube')),
            ("Draw", qta.icon('fa5s.pencil-ruler')),
            ("Communication", qta.icon('fa5s.broadcast-tower')),
            ("Debug", qta.icon('fa5s.bug')),
        ]
        for text, icon in toolbar_items:
            widget_action = QWidgetAction(self.main_window)
            
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(4, 4, 4, 4)
            layout.setSpacing(10)

            check_box = QCheckBox()
            check_box.setChecked(True)
            
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(16, 16))
            
            text_label = QLabel(text)

            layout.addWidget(check_box)
            layout.addWidget(icon_label)
            layout.addWidget(text_label)
            layout.addStretch()
            
            # You can connect the toggled signal to a slot to show/hide the toolbar
            # check_box.toggled.connect(lambda checked, name=text: self.toggle_toolbar(checked, name))

            widget_action.setDefaultWidget(widget)
            self.tool_bar_menu.addAction(widget_action)

    def create_checkable_docking_actions(self):
        """Creates and adds checkable widget actions to the Docking Window submenu."""
        docking_items = [
            ("Project Tree", qta.icon('fa5s.project-diagram')),
            ("Screen Tree", qta.icon('fa5s.sitemap')),
            ("System Tree", qta.icon('fa5s.cogs')),
            ("Device Search", qta.icon('fa5s.search-location')),
            ("Data Browser", qta.icon('fa5s.database')),
            ("Property Tree", qta.icon('fa5s.list-alt')),
            ("IP Address", qta.icon('fa5s.ethernet')),
            ("Library", qta.icon('fa5s.book-open')),
            ("Controller List", qta.icon('fa5s.gamepad')),
            ("Data View", qta.icon('fa5s.table')),
            ("Screen Image List", qta.icon('fa5s.images')),
        ]
        for text, icon in docking_items:
            widget_action = QWidgetAction(self.main_window)

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(4, 4, 4, 4)
            layout.setSpacing(10)

            check_box = QCheckBox()
            check_box.setChecked(True)

            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(16, 16))

            text_label = QLabel(text)

            layout.addWidget(check_box)
            layout.addWidget(icon_label)
            layout.addWidget(text_label)
            layout.addStretch()

            # You can connect the toggled signal to a slot to show/hide the docking window
            # check_box.toggled.connect(lambda checked, name=text: self.toggle_docking_window(checked, name))
            
            widget_action.setDefaultWidget(widget)
            self.docking_window_menu.addAction(widget_action)

    def toggle_toolbar(self, checked, name):
        """Placeholder slot for toggling toolbars."""
        print(f"Toolbar '{name}' visibility set to: {checked}")
        # Here you would add logic to find the toolbar by name and set its visibility.
        # e.g., self.main_window.toolbars[name].setVisible(checked)

    def toggle_docking_window(self, checked, name):
        """Placeholder slot for toggling docking windows."""
        print(f"Docking window '{name}' visibility set to: {checked}")
        # Here you would add logic to find the dock widget by name and set its visibility.
        # e.g., self.main_window.docks[name].setVisible(checked)

