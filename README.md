# HMI Designer

A powerful Human-Machine Interface (HMI) design application built with PyQt6, providing an intuitive graphical environment for creating and managing HMI projects, screens, comments, and tags.

## Description

HMI Designer is a desktop application that allows users to design and develop Human-Machine Interfaces for industrial control systems. The application features a modular architecture with dockable windows, multiple toolbars, and support for various screen types including base screens, window screens, template screens, and widget screens.

## Features

- **Project Management**: Create, open, save, and manage HMI project files (.hmi)
- **Screen Design**: Design different types of screens with canvas-based editing
- **Comment System**: Manage comments and annotations within projects
- **Tag Management**: Handle data tags for HMI elements
- **Dockable Interface**: Multiple dockable windows for project tree, screen tree, property tree, and more
- **Toolbar System**: Comprehensive toolbars for editing, viewing, alignment, figures, objects, and debugging
- **Menu System**: Full menu bar with file operations, editing, viewing, screen management, and more
- **Settings Management**: Persistent application settings and UI state
- **Zoom and View Controls**: Flexible zoom levels and screen fitting capabilities
- **Multi-tab Interface**: Support for multiple open screens, comments, and tags in tabs
- **Icon-based UI**: Rich icon set for intuitive user interaction

## Installation

### Prerequisites

- Python 3.7 or higher
- PyQt6
- qtawesome

### Setup

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Starting the Application**: Run `python main.py` to launch the HMI Designer
2. **Creating a New Project**: Use File > New Project to start a fresh HMI project
3. **Adding Screens**: Use the Screen menu to add different types of screens (Base, Window, Template, Widgets)
4. **Designing Screens**: Use the canvas to add and manipulate UI elements
5. **Managing Comments**: Access comment tables through the project tree
6. **Managing Tags**: Work with tag tables for data binding
7. **Saving Projects**: Use File > Save or File > Save As to save your work

### Key Shortcuts

- Ctrl+N: New Project
- Ctrl+O: Open Project
- Ctrl+S: Save Project
- Ctrl+Z: Undo
- Ctrl+Y: Redo
- Ctrl+C: Copy
- Ctrl+V: Paste
- Ctrl+A: Select All
- Delete: Delete selected items

## Requirements

- PyQt6: For the GUI framework
- qtawesome: For icon support
- Python 3.7+: Minimum Python version required

## Project Structure

```
HMI-3.00/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── settings.json          # Application settings
├── stylesheet.qss         # Custom styling
├── avijit.hmi             # Sample project file
├── main_window/           # Main application window components
│   ├── main_window.py     # Main window class
│   ├── menus/             # Menu classes
│   ├── toolbars/          # Toolbar classes
│   ├── widgets/           # Custom widgets
│   ├── dialogs/           # Dialog windows
│   ├── docking_windows/   # Dockable window classes
│   └── services/          # Application services
├── project/               # Project-related classes
│   ├── comment/           # Comment management
│   └── tag/               # Tag management
├── screen/                # Screen-related classes
│   ├── base/              # Base screen implementation
│   ├── template/          # Template screen
│   ├── widgets/           # Widget screens
│   └── window/            # Window screens
├── services/              # Core services
│   ├── project_service.py # Project file handling
│   ├── settings_service.py# Settings management
│   ├── comment_service.py # Comment data management
│   └── edit_service.py    # Edit operations
└── main_window/resources/icons/  # Application icons
```

## Contributing

Contributions to HMI Designer are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

1. Follow the installation steps above
2. Ensure you have a compatible Python environment
3. Test changes across different screen resolutions
4. Verify compatibility with different PyQt6 versions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions about HMI Designer, please check the project documentation or create an issue in the repository.

## Version

Current Version: 1.0

---

*HMI Designer - Empowering Industrial Interface Design*
