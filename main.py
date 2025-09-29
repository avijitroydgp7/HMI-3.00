import sys
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtGui import QIcon
from main_window.main_window import MainWindow
from services.settings_service import SettingsService
from main_window.services.icon_service import IconService

def main():
    """
    The main function to launch the application.
    """
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    
    # Set the application icon
    app.setWindowIcon(IconService.get_icon("HMI-Designer-icon"))

    # Set the application style to Fusion
    app.setStyle(QStyleFactory.create('Fusion'))

    # Load and apply the stylesheet for custom styling
    try:
        with open('stylesheet.qss', 'r') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("stylesheet.qss not found. Using default styles.") # Or handle this more gracefully
    
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
