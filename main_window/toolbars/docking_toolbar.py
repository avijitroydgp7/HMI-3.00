from PyQt6.QtWidgets import QToolBar, QCheckBox
from PyQt6.QtGui import QAction
import qtawesome as qta

class DockingToolbar(QToolBar):
    """
    A floating toolbar to control the visibility of docking windows.
    Its state is synchronized with the View > Docking Window menu.
    """
    def __init__(self, main_window, view_menu):
        super().__init__("Window Display", main_window)
        self.main_window = main_window
        self.view_menu = view_menu

        # This list should match the one in view_menu.py for consistency
        docking_items = [
            ("Project Tree", qta.icon('fa5s.project-diagram')),
            ("Screen Tree", qta.icon('fa5s.sitemap')),
            ("System Tree", qta.icon('fa5s.cogs')),
            ("Property Tree", qta.icon('fa5s.list-alt')),
            ("Library", qta.icon('fa5s.book-open')),
            ("Screen Image List", qta.icon('fa5s.images')),
            ("Tag Search", qta.icon('fa5s.search-location')),
            ("Data Browser", qta.icon('fa5s.database')),
            ("IP Address", qta.icon('fa5s.ethernet')),
            ("Controller List", qta.icon('fa5s.gamepad')),
            ("Data View", qta.icon('fa5s.table')),
        ]
        
        # Create a mapping from text to icon for easy lookup
        icon_map = {text: icon for text, icon in docking_items}

        # Find the corresponding QWidgetAction in the menu and link it
        for menu_action in self.view_menu.docking_window_menu.actions():
            action_text = menu_action.text()
            icon = icon_map.get(action_text, qta.icon('fa5s.window-maximize')) # Default icon

            # Create a new, checkable action for the toolbar
            toolbar_action = QAction(icon, action_text, self)
            toolbar_action.setCheckable(True)
            toolbar_action.setToolTip(f"Show/Hide {action_text}")

            # Find the checkbox in the menu's widget action
            widget = menu_action.defaultWidget()
            checkbox = widget.findChild(QCheckBox)

            if checkbox:
                # Sync toolbar action -> menu checkbox
                toolbar_action.toggled.connect(checkbox.setChecked)
                # Sync menu checkbox -> toolbar action
                checkbox.toggled.connect(toolbar_action.setChecked)
                # Set initial checked state from the checkbox (which is restored from settings)
                toolbar_action.setChecked(checkbox.isChecked())
            
            self.addAction(toolbar_action)
