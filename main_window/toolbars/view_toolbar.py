from PyQt6.QtWidgets import QToolBar, QComboBox, QToolButton, QCheckBox
from PyQt6.QtCore import Qt
import qtawesome as qta

class ViewToolbar(QToolBar):
    def __init__(self, main_window, view_menu):
        super().__init__("View", main_window)
        self.main_window = main_window
        self.view_menu = view_menu
        self.setMovable(True)

        # Snap Dropdown
        self.snap_combo = QComboBox()
        self.snap_combo.setFixedWidth(100)
        self.snap_combo.addItems(["1", "2", "4", "5", "8", "10", "16", "20", "32", "40"])
        self.snap_combo.setCurrentText("10")
        self.addWidget(self.snap_combo)

        # Object Snap Checkbox
        self.object_snap_checkbox = QCheckBox("Object Snap")
        self.object_snap_checkbox.setChecked(True)
        self.object_snap_checkbox.toggled.connect(self.view_menu.object_snap_checkbox.setChecked)
        self.view_menu.object_snap_checkbox.toggled.connect(self.object_snap_checkbox.setChecked)
        self.addWidget(self.object_snap_checkbox)
        self.addSeparator()

        # Zoom Controls
        zoom_in_icon = qta.icon('fa5s.search-plus')
        zoom_out_icon = qta.icon('fa5s.search-minus')
        
        self.zoom_out_button = QToolButton()
        self.zoom_out_button.setIcon(zoom_out_icon)
        self.addWidget(self.zoom_out_button)

        self.zoom_combo = QComboBox()
        self.zoom_combo.setFixedWidth(100)
        for action in self.view_menu.zoom_actions:
            self.zoom_combo.addItem(action.text())
        self.zoom_combo.setCurrentText("100%")
        self.zoom_combo.currentTextChanged.connect(self.sync_zoom_action)
        self.addWidget(self.zoom_combo)

        self.zoom_in_button = QToolButton()
        self.zoom_in_button.setIcon(zoom_in_icon)
        self.addWidget(self.zoom_in_button)

        self.addAction(self.view_menu.fit_screen_action)
        self.addSeparator()

        # State Controls
        self.addAction(self.view_menu.prev_state_action)
        self.addAction(self.view_menu.state_on_off_action)
        self.addAction(self.view_menu.next_state_action)
        self.addSeparator()

        # Display Item Toggles
        self.addAction(self.view_menu.tag_action)
        self.addAction(self.view_menu.object_id_action)
        self.addAction(self.view_menu.transform_line_action)
        self.addAction(self.view_menu.click_area_action)

    def sync_zoom_action(self, text):
        for action in self.view_menu.zoom_actions:
            if action.text() == text:
                action.setChecked(True)
                break
