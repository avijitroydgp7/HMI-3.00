# HMI Designer - Comprehensive Documentation

A powerful Human-Machine Interface (HMI) design application built with **PySide6**, providing an intuitive graphical environment for creating and managing HMI projects, screens, comments, and tags for industrial control systems.

**Version**: 3.00  
**Last Updated**: December 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Project Structure](#project-structure)
6. [Usage Guide](#usage-guide)
7. [Module Documentation](#module-documentation)
8. [Services Layer](#services-layer)
9. [UI Components](#ui-components)
10. [Advanced Features](#advanced-features)
11. [Configuration](#configuration)
12. [Troubleshooting](#troubleshooting)
13. [Contributing](#contributing)

---

## Overview

**HMI Designer** is a professional-grade desktop application designed for creating and managing Human-Machine Interfaces (HMI) for industrial control systems. It provides a comprehensive development environment with multiple editing tools, visualization options, and project management capabilities.

The application is built using **PySide6** (Qt for Python) and follows a modular, service-oriented architecture, making it maintainable, extensible, and scalable.

### Key Capabilities

- **Professional HMI Design**: Create sophisticated industrial interfaces with multiple screen types
- **Project-Based Workflow**: Organize designs into projects with persistent storage
- **Rich Comment System**: Annotate and document designs with virtual spreadsheet-based comments
- **Tag Management**: Manage data tags for binding HMI elements to data sources
- **Advanced Canvas Editing**: Full graphics scene support with drawing tools and transformations
- **Dockable UI Architecture**: Flexible, customizable interface layout
- **Dark Theme**: Modern, professional dark-themed interface

---

## Features

### Core Features

- **Project Management**
  - Create new projects from scratch
  - Open existing project files (`.hmi` format)
  - Save and save-as functionality
  - Project data structure with screens, comments, and design templates
  - Recent projects history

- **Screen Design & Types**
  - **Base Screens**: Primary design canvas with custom dimensions
  - **Window Screens**: Screen templates with windowed layouts
  - **Template Screens**: Reusable screen templates
  - **Widget Screens**: Individual widget-based screens
  - Canvas-based visual editing with drag-and-drop support
  - Background customization (color, gradients, patterns)

- **Drawing & Manipulation Tools**
  - Rectangle and ellipse drawing tools
  - Object selection and multi-selection
  - Transform operations (move, resize, rotate, scale)
  - Alignment tools (left, center, right, top, middle, bottom)
  - Distribution tools
  - Z-order management (bring to front, send to back)

- **Comment System**
  - Virtual spreadsheet-based comment tables
  - Add, edit, delete comments
  - Optimized operations for performance
  - Viewport optimization for handling large datasets
  - Performance configuration for tuning

- **Tag Management**
  - Create and manage data tags
  - Optimized tag operations
  - Tag search functionality
  - Data binding support for HMI elements

- **Dockable Windows System** (11 Docks)
  - **Project Tree Dock**: Hierarchical project structure navigation
  - **Screen Tree Dock**: All screens in project
  - **System Tree Dock**: System-wide object hierarchy
  - **Property Tree Dock**: Real-time property editing
  - **Library Dock**: Reusable components library
  - **Screen Image List Dock**: Thumbnail view of screens
  - **Tag Search Dock**: Quick tag lookup
  - **Data Browser Dock**: Data source exploration
  - **IP Address Dock**: Network configuration
  - **Controller List Dock**: Connected controllers
  - **Data View Dock**: Real-time data monitoring

- **Toolbar System** (8 customizable toolbars)
  - **Window Display Toolbar**: Application-level controls
  - **View Toolbar**: Zoom, fit, object snap, snap distance
  - **Screen Toolbar**: Screen operations
  - **Edit Toolbar**: Undo, redo, cut, copy, paste, delete
  - **Alignment Toolbar**: Object alignment and distribution
  - **Figure Toolbar**: Shape drawing tools
  - **Object Toolbar**: Object manipulation
  - **Debug Toolbar**: Debugging utilities

- **Menu System**
  - **File Menu**: Project operations (New, Open, Save, Save As, Close, Exit)
  - **Edit Menu**: Standard editing (Undo, Redo, Cut, Copy, Paste, Delete, Select All)
  - **View Menu**: Display options and docking window visibility
  - **Screen Menu**: Screen creation and management
  - **Search/Replace Menu**: Content searching
  - **Figure Menu**: Shape and drawing operations
  - **Object Menu**: Object manipulation and properties
  - **Common Menu**: Context-sensitive operations

- **UI Persistence**
  - Window geometry and state saved/restored
  - Toolbar visibility settings
  - Dock position and visibility preferences
  - View settings (zoom, snap settings)
  - All settings stored in `settings.json`

- **Zoom & View Controls**
  - Multiple zoom presets (25%, 50%, 75%, 100%, 150%, 200%, 400%)
  - Fit to window
  - Fit to page
  - Zoom in/out with mouse wheel
  - Pan capability

- **Professional UI**
  - Dark theme with custom color palette
  - Custom stylesheet support (`stylesheet.qss`)
  - Icon-based UI with qtawesome integration
  - Multi-tab interface for open screens
  - Status bar with real-time information

- **Logging & Debugging**
  - Comprehensive debug logging system
  - Structured logging with timestamps
  - File-based logging (`app_debug.log`)
  - Debug toolbar for advanced debugging

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   MainWindow (QMainWindow)              │
│  Central orchestrator for all UI and business logic     │
└─────────────────────────────────────────────────────────┘
                          ▲
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼─────────┐ ┌──────▼──────────┐
│   Menus      │  │   Toolbars       │ │  Docking Windows│
│ (8 modules)  │  │  (8 toolbars)    │ │  (11 docks)     │
└───────┬──────┘  └────────┬─────────┘ └──────┬──────────┘
        │                  │                  │
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────▼───────────────────┐
        │      Services Layer                  │
        │  (Business Logic & Data Management)  │
        └──────────────────┬───────────────────┘
                           │
      ┌────────┬───────────┼─────────┬──────────┐
      │        │           │         │          │
┌─────▼──┐ ┌───▼───┐ ┌─────▼───┐ ┌───▼───┐ ┌────▼────┐
│Project │ │Edit   │ │Comment  │ │View   │ │Settings │
│Service │ │Service│ │Service  │ │Service│ │Service  │
└────────┘ └───────┘ └─────────┘ └───────┘ └─────────┘
      │         │         │          │          │
      └─────────┴────────┬┴──────────┴──────────┘
                         │
        ┌────────────────▼──────────┐
        │     Canvas & Graphics     │
        │  (CanvasBaseScreen)       │
        │  - Screen objects         │
        │  - Drawing tools          │
        │  - Transform operations   │
        └───────────────────────────┘
                    │
        ┌───────────▼─────────────┐
        │   Data Models           │
        │  - Comments table       │
        │  - Tags table           │
        │  - Screen structures    │
        └─────────────────────────┘
```

### Design Patterns

1. **Service-Oriented Architecture (SOA)**
   - Each major functionality has a dedicated service
   - Services encapsulate business logic
   - UI components use services for data access

2. **Model-View-Controller (MVC)**
   - Canvas provides the view
   - Screen data models provide the model
   - Services orchestrate controller logic

3. **Factory Pattern**
   - `DockWidgetFactory`: Creates and manages dock widgets
   - Centralized creation of UI components

4. **Observer Pattern**
   - Signals and slots for event handling
   - Loose coupling between components

5. **Singleton Pattern**
   - Services are instantiated once and passed around
   - Ensures single source of truth for data

---

## Installation

### Prerequisites

- **Python**: 3.7 or higher (3.9+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **Disk Space**: ~500MB for dependencies
- **RAM**: Minimum 2GB (4GB recommended)

### Dependencies

```
PySide6           # Qt for Python framework
qtawesome         # Icon pack integration
```

### Setup Instructions

#### 1. Clone or Extract the Project

```bash
# If from a repository
git clone <repository-url>
cd HMI-3.00

# Or extract from zip
unzip HMI-3.00.zip
cd HMI-3.00
```

#### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Verify Installation

```bash
python -c "from PySide6.QtWidgets import QApplication; print('PySide6 installed successfully')"
```

#### 5. Run the Application

```bash
python main.py
```

The application window should open with the dark theme and all docking windows initialized.

### Troubleshooting Installation

**Issue**: `ModuleNotFoundError: No module named 'PySide6'`
```bash
pip install --upgrade PySide6
```

**Issue**: Application won't start on Windows
```bash
# Check if you have Visual C++ Runtime
# Download from: https://support.microsoft.com/en-us/help/2977003
```

**Issue**: High DPI scaling issues on Windows
- Edit `main.py` and add before `QApplication`:
```python
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = ''
```

---

## Project Structure

### Directory Organization

```
HMI-3.00/                          # Root project directory
├── main.py                        # Entry point / Application launcher
├── debug_utils.py                 # Logging utilities and debug helpers
├── requirements.txt               # Python dependencies
├── settings.json                  # Persistent UI state & settings
├── stylesheet.qss                 # Custom Qt stylesheet for dark theme
├── avijit.hmi                     # Sample/template HMI project
│
├── main_window/                   # Main application window & UI components
│   ├── __init__.py
│   ├── main_window.py             # MainWindow class (997 lines)
│   ├── services/                  # UI-specific services
│   │   ├── icon_service.py        # Icon loading and caching
│   │   └── view_service.py        # View and rendering logic
│   ├── dialogs/                   # Dialog windows for various operations
│   │   └── project_tree/          # Project tree dialogs
│   ├── docking_windows/           # Dockable UI panels (11 different docks)
│   │   ├── dock_widget_factory.py # Factory for creating dock widgets
│   │   ├── project_tree_dock.py   # Project hierarchy browser
│   │   ├── screen_tree_dock.py    # Screen list dock
│   │   ├── system_tree_dock.py    # System objects dock
│   │   ├── property_tree_dock.py  # Object properties dock
│   │   ├── library_dock.py        # Component library
│   │   ├── screen_image_list_dock.py
│   │   ├── tag_search_dock.py     # Tag search interface
│   │   ├── data_browser_dock.py   # Data source browser
│   │   ├── ip_address_dock.py     # Network configuration
│   │   ├── controller_list_dock.py
│   │   └── data_view_dock.py      # Real-time data display
│   ├── menus/                     # Menu definitions (8 menu modules)
│   │   ├── common_menu.py         # Shared menu utilities
│   │   ├── file_menu.py           # File operations menu
│   │   ├── edit_menu.py           # Editing operations
│   │   ├── search_replace_menu.py # Search and replace
│   │   ├── view_menu.py           # View options
│   │   ├── screen_menu.py         # Screen management
│   │   ├── figure_menu.py         # Shape drawing operations
│   │   └── object_menu.py         # Object manipulation
│   ├── toolbars/                  # Toolbar implementations (8 toolbars)
│   │   ├── docking_toolbar.py     # Window display controls
│   │   ├── view_toolbar.py        # Zoom and view controls
│   │   ├── screen_toolbar.py      # Screen operations
│   │   ├── edit_toolbar.py        # Edit operations
│   │   ├── alignment_toolbar.py   # Object alignment tools
│   │   ├── figure_toolbar.py      # Drawing tools
│   │   ├── object_toolbar.py      # Object tools
│   │   ├── debug_toolbar.py       # Debug utilities
│   │   ├── transform_handler.py   # Object transformation logic
│   │   └── drawing_tools/         # Specific drawing tool implementations
│   ├── resources/                 # UI resources
│   │   └── icons/                 # Application icons
│   └── widgets/                   # Custom widgets
│       ├── color_selector.py      # Color picker widget
│       ├── gradient_widget.py     # Gradient editor
│       ├── pattern_widget.py      # Pattern selector
│       └── tree.py                # Custom tree widget
│
├── screen/                        # Screen & canvas implementation
│   ├── base/                      # Base screen classes
│   │   ├── base_graphic_object.py # Base classes for screen objects
│   │   ├── canvas_base_screen.py  # Canvas implementation (700 lines)
│   ├── template/                  # Screen templates
│   ├── widgets/                   # Widget screens
│   └── window/                    # Window-based screens
│
├── services/                      # Core business logic services
│   ├── project_service.py         # Project file handling & persistence
│   ├── settings_service.py        # Application settings management
│   ├── edit_service.py            # Edit operations (undo/redo)
│   ├── comment_service.py         # Comment management
│
├── project/                       # Project data models
│   ├── comment/                   # Comment subsystem
│   │   ├── comment_table.py       # Comment table data structure
│   │   ├── comment_utils.py       # Comment utilities
│   │   ├── optimized_operations.py # Optimized comment operations
│   │   ├── performance_config.py  # Performance tuning
│   │   ├── viewport_optimizer.py  # Viewport caching
│   │   └── virtual_spreadsheet.py # Spreadsheet display
│   └── tag/                       # Tag subsystem
│       ├── tag_table.py           # Tag data structure
│       └── optimized_tag_operations.py
│
└── README.md                      # This file
```

---

## Usage Guide

### Starting the Application

```bash
python main.py
```

### Creating a New Project

1. **Method 1**: `File` → `New Project`
2. **Method 2**: Press `Ctrl+N`

### Creating & Designing Screens

#### Adding a Screen

1. Select `Screen` → `Add Screen`
2. Choose screen type:
   - **Base Screen**: Primary design canvas
   - **Window Screen**: Windowed layout
   - **Template Screen**: Reusable template
   - **Widget Screen**: Individual widget
3. Configure dimensions and background

#### Designing Screen Content

1. Select drawing tool from Figure Toolbar
2. Draw objects by clicking and dragging
3. Manipulate objects:
   - **Select**: Click object
   - **Move**: Drag selected object
   - **Resize**: Drag corner handles
   - **Multi-select**: Ctrl+click objects
4. Apply formatting via Property Tree Dock

#### Object Alignment

1. Select multiple objects
2. Use Alignment Toolbar:
   - **Horizontal**: Left, Center, Right
   - **Vertical**: Top, Middle, Bottom
3. Distribution options available

### Managing Comments

1. Access: Project Tree Dock → Double-click "Comments"
2. **Add Row**: Click "Add Comment"
3. **Edit Cell**: Double-click cell
4. **Delete Row**: Select row → Delete
5. **Search**: Use Tag Search Dock

### Working with Tags

1. **Create Tags**: Use Tag Dialog (Project Tree → New Tag)
2. **Bind to Objects**: Select object → Property Tree → Data Binding
3. **Search Tags**: Use Tag Search Dock

### Saving & Opening Projects

**Save:**
- First time: `File` → `Save As`
- Updates: `File` → `Save` (Ctrl+S)

**Open:**
- `File` → `Open` (Ctrl+O)
- Or `File` → `Recent Projects`

### View Controls

**Zoom:**
- Toolbar dropdown: Select preset (25% - 400%)
- Mouse wheel: Scroll to zoom

**Fit to View:**
- `View Toolbar` → "Fit to Window"

**Pan:**
- Middle mouse button drag

### Object Snapping

1. **Enable**: View Toolbar → Check "Object Snap"
2. **Configure Distance**: Dropdown (1, 5, 10, 15, 20 pixels)

### Undo/Redo

- **Undo**: `Edit` → `Undo` (Ctrl+Z)
- **Redo**: `Edit` → `Redo` (Ctrl+Y)

---

## Module Documentation

### Main Application (`main.py`)

Initializes QApplication, sets theme, loads stylesheets, and creates MainWindow.

### MainWindow (`main_window/main_window.py` - 997 lines)

Central orchestrator managing:
- All menus (8 modules)
- All toolbars (8 toolbars)
- All docking windows (11 docks)
- File operations
- Edit operations
- Screen management
- Object selection & transformation

### Canvas Base Screen (`screen/base/canvas_base_screen.py` - 700 lines)

Implements drawing canvas and graphics scene:
- Extends `QGraphicsView`
- Manages `QGraphicsScene`
- Handles background rendering
- Supports object manipulation
- Zoom and pan operations
- Snap line visualization

### Settings Service (`services/settings_service.py` - 109 lines)

Persistent storage of:
- Window geometry and state
- Toolbar visibility
- Dock positions
- View settings (zoom, snap)

### Project Service (`services/project_service.py` - 142 lines)

Handles:
- Project file I/O
- Data structure management
- `.hmi` file format

### Comment System (`project/comment/`)

Advanced comment management:
- Virtual spreadsheet UI
- Performance optimizations
- Viewport caching
- Search & filter

### Tag System (`project/tag/`)

Data tag management:
- Create and manage tags
- Tag search
- Data binding support

---

## Services Layer

### Project Service
```python
from services.project_service import ProjectService

service = ProjectService()
service.new_project()
service.load_project('project.hmi')
service.save_project('project.hmi')
```

### Settings Service
```python
from services.settings_service import SettingsService

settings = SettingsService('settings.json')
settings.save_settings(main_window)
toolbar_visibility = settings.get_toolbars_visibility()
```

### Comment Service
```python
from services.comment_service import CommentService

comment_service = CommentService()
comment_service.add_comment(screen_id, comment_data)
comment_service.get_comments(screen_id)
```

### Edit Service
```python
from services.edit_service import EditService

edit_service = EditService()
edit_service.undo()
edit_service.redo()
edit_service.push_action(action)
```

### View Service
```python
from main_window.services.view_service import ViewService

view_service = ViewService()
view_service.fit_to_window()
view_service.zoom_to_level(100)
```

---

## UI Components

### Menus (8 Modules)

| Menu | File | Functions |
|------|------|-----------|
| File | `file_menu.py` | New, Open, Save, Save As, Close, Exit |
| Edit | `edit_menu.py` | Undo, Redo, Cut, Copy, Paste, Delete |
| View | `view_menu.py` | Zoom, Fit, Show/Hide docks & toolbars |
| Screen | `screen_menu.py` | Add, Delete, Properties |
| Search/Replace | `search_replace_menu.py` | Find, Replace |
| Figure | `figure_menu.py` | Rectangle, Ellipse, Polygon, Line |
| Object | `object_menu.py` | Properties, Alignment, Z-order |
| Common | `common_menu.py` | Shared utilities |

### Toolbars (8 Toolbars)

| Toolbar | File | Purpose |
|---------|------|---------|
| Window Display | `docking_toolbar.py` | Application controls |
| View | `view_toolbar.py` | Zoom, fit, snap settings |
| Screen | `screen_toolbar.py` | Screen operations |
| Edit | `edit_toolbar.py` | Undo, Redo, Cut, Copy, Paste |
| Alignment | `alignment_toolbar.py` | Alignment & distribution |
| Figure | `figure_toolbar.py` | Drawing tools |
| Object | `object_toolbar.py` | Object tools |
| Debug | `debug_toolbar.py` | Debug utilities |

### Docking Windows (11 Docks)

| Dock | File | Purpose |
|------|------|---------|
| Project Tree | `project_tree_dock.py` | Project hierarchy |
| Screen Tree | `screen_tree_dock.py` | Screen list |
| System Tree | `system_tree_dock.py` | System objects |
| Property Tree | `property_tree_dock.py` | Object properties |
| Library | `library_dock.py` | Component library |
| Screen Image List | `screen_image_list_dock.py` | Screen thumbnails |
| Tag Search | `tag_search_dock.py` | Tag search |
| Data Browser | `data_browser_dock.py` | Data sources |
| IP Address | `ip_address_dock.py` | Network config |
| Controller List | `controller_list_dock.py` | Connected controllers |
| Data View | `data_view_dock.py` | Real-time data |

---

## Advanced Features

### Object Snapping

Helps align objects to grid/other objects. Configure via View Toolbar.

### Multi-Selection & Transformation

- Click: Single select
- Ctrl+Click: Add to selection
- Drag rectangle: Multi-select
- Transformations: Move, Resize, Rotate, Scale

### Z-Order Management

- Right-click → Bring to Front
- Right-click → Send to Back
- Object Menu → Arrange

### Undo/Redo System

Command pattern based, managed by EditService. Each action is reversible.

### Viewport Optimization

For large comment tables:
- Virtual viewport rendering
- Lazy loading of rows
- Caching mechanism
- Performance tuning via `performance_config.py`

---

## Configuration

### Application Settings (`settings.json`)

```json
{
  "main_window": {
    "geometry": "hex_encoded_geometry",
    "state": "hex_encoded_state"
  },
  "toolbars_visibility": {
    "Window Display": true,
    "View": true,
    "Screen": true,
    "Edit": true,
    "Alignment": true,
    "Figure": true,
    "Object": true,
    "Debug": true
  },
  "docks_visibility": {
    "project_tree": true,
    "screen_tree": true,
    "system_tree": false,
    "property_tree": true,
    "library": false,
    "screen_image_list": false,
    "tag_search": false,
    "data_browser": false,
    "ip_address": false,
    "controller_list": false,
    "data_view": false
  },
  "view_settings": {
    "object_snap": true,
    "snap_distance": "10",
    "state_number": 1
  }
}
```

### Stylesheet Customization (`stylesheet.qss`)

Modify colors, fonts, and widget styles without code changes.

### Debug Logging

**In `main.py`:**
```python
setup_logging(debug_mode=True)  # Enable debug logging
```

**Output**: `app_debug.log`

---

## Troubleshooting

### Common Issues

**Application won't start**
```bash
pip install --upgrade PySide6
pip install qtawesome
```

**Blank canvas or missing icons**
- Ensure `stylesheet.qss` exists in project directory
- Check file paths in `main.py`

**High DPI scaling issues (Windows)**
```bash
SET QT_QPA_PLATFORM_PLUGIN_PATH=""
python main.py
```

**Performance issues**
- Check `performance_config.py` settings
- Increase viewport cache size
- Monitor `app_debug.log`

**Settings not saving**
1. Check file permissions on `settings.json`
2. Ensure directory is writable
3. Check `app_debug.log` for errors
4. Delete `settings.json` and restart

### Getting Debug Information

**Check log file:**
```bash
cat app_debug.log  # or: type app_debug.log (Windows)
```

**Enable console logging:**
- Edit `debug_utils.py`
- Uncomment console handler section

---

## Contributing

### Code Style

- **Python**: PEP 8 compliant
- **Naming**:
  - Classes: PascalCase
  - Functions/Methods: snake_case
  - Constants: UPPER_SNAKE_CASE
- **Comments**: Docstrings for all classes and public methods

### Adding New Features

1. **Business Logic**: Create Service in `services/`
2. **UI Components**:
   - Dialogs: `main_window/dialogs/project_tree/`
   - Toolbars: `main_window/toolbars/`
   - Docks: `main_window/docking_windows/`
3. **Testing**: Test with existing projects, verify persistence

### Extending Canvas

1. **New Drawing Tool**: Create in `main_window/toolbars/drawing_tools/`
2. **New Object Type**: Extend `BaseGraphicObject` in `screen/base/`

---

## License & Information

- **Version**: 3.00
- **Last Updated**: December 2025
- **Author**: Avijit
- **Framework**: PySide6 (Qt for Python)
- **Python Requirement**: 3.7+

---

## Support & Resources

- **PySide6 Documentation**: https://doc.qt.io/qtforpython/
- **Qt Documentation**: https://doc.qt.io/qt-6/
- **qtawesome Icons**: https://github.com/spyder-ide/qtawesome

---

## Future Roadmap

- [ ] Export to multiple formats (SVG, PNG, PDF)
- [ ] Collaborative editing support
- [ ] Plugin architecture
- [ ] Advanced animation system
- [ ] Real-time data simulation
- [ ] Version control integration
- [ ] Batch operations
- [ ] Advanced scripting engine

---

**End of Documentation**
