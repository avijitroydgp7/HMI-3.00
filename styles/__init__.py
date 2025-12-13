"""
Styles package - Centralized styling for HMI Designer Application

This package contains all style-related code including:
- colors.py: Color theme constants
- fonts.py: Font theme constants
- stylesheets.py: QSS stylesheet generators

Usage:
    from styles import colors
    from styles import fonts
    from styles import stylesheets
    
    # Use colors
    widget.setStyleSheet(f"background-color: {colors.BG_DARK_PRIMARY};")
    
    # Use fonts
    widget.setFont(fonts.FONT_LARGE_BOLD)
    
    # Use stylesheets
    widget.setStyleSheet(stylesheets.get_tree_widget_stylesheet())
"""

from styles import colors
from styles import fonts
from styles import stylesheets

__all__ = ["colors", "fonts", "stylesheets"]
