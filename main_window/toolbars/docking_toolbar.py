from PyQt6.QtWidgets import QToolBar, QCheckBox
from PyQt6.QtGui import QAction
import qtawesome as qta

class DockingToolbar(QToolBar):
    """
    A floating toolbar to control the visibility of docking windows.
    Its state is synchronized with the View > Docking Window menu via a
    central controller in the MainWindow.
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
        
        for text, icon in docking_items:
            dock_name = text.lower().replace(' ', '_')
            
            # Create a new, checkable action for the toolbar
            toolbar_action = QAction(icon, text, self)
            toolbar_action.setCheckable(True)
            toolbar_action.setToolTip(f"Show/Hide {text}")
            # Set a unique object name to find it later
            toolbar_action.setObjectName(f"toggle_{dock_name}")

            self.addAction(toolbar_action)
