import sys
from PyQt6.QtWidgets import QApplication, QStyleFactory
from main_window.main_window import MainWindow

def main():
    """
    The main function to launch the application.
    """
    # Create an instance of QApplication
    app = QApplication(sys.argv)
    # Set the application style to Fusion
    app.setStyle(QStyleFactory.create('Fusion'))
    # Create an instance of our MainWindow
    window = MainWindow()

    # Show the window
    window.show()

    # Start the application's event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()