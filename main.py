# main.py
import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from main_window.main_window import MainWindow
from services.settings_service import SettingsService
from main_window.services.icon_service import IconService
from debug_utils import setup_logging
from styles import stylesheets

def main():
    """
    The main function to launch the application.
    """
    # Set up logging
    setup_logging(debug_mode=True)

    # Create an instance of QApplication
    app = QApplication(sys.argv)
    
    # Set the application icon
    app.setWindowIcon(IconService.get_icon("HMI-Designer-icon"))

    # Set the application style to Fusion
    app.setStyle(QStyleFactory.create('Fusion'))

    # Create and set a dark palette using centralized theme
    dark_palette = stylesheets.create_dark_palette()
    app.setPalette(dark_palette)

    # Load and apply centralized stylesheets
    global_stylesheet = (
        stylesheets.get_tool_button_stylesheet() + 
        stylesheets.get_menu_stylesheet() + 
        stylesheets.get_toolbar_stylesheet()
    )
    app.setStyleSheet(global_stylesheet)
    
    # Initialize the settings service
    settings_service = SettingsService('settings.json')
    
    # Create an instance of our MainWindow
    window = MainWindow(settings_service)

    # Show the window
    window.show()

    # Start the application's event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
