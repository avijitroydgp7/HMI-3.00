"""
Centralized font theme for the HMI Designer Application.
All font-related constants are defined here for consistency.
"""

from PySide6.QtGui import QFont

# ============================================================================
# FONT FAMILIES
# ============================================================================

FONT_FAMILY_DEFAULT = "Arial"          # Default font family
FONT_FAMILY_MONOSPACE = "Courier New"  # Monospace font for code/formulas
FONT_FAMILY_SYSTEM = "Segoe UI"        # System font

# ============================================================================
# FONT SIZES (in points)
# ============================================================================

FONT_SIZE_SMALL = 8           # Small text (hints, status)
FONT_SIZE_NORMAL = 10         # Normal text (default)
FONT_SIZE_MEDIUM = 11         # Medium text
FONT_SIZE_LARGE = 12          # Large text (headers)
FONT_SIZE_XLARGE = 14         # Extra large text (titles)
FONT_SIZE_XXLARGE = 16        # Double extra large (dialog titles)

# ============================================================================
# FONT WEIGHTS
# ============================================================================

FONT_WEIGHT_NORMAL = QFont.Weight.Normal      # Normal weight
FONT_WEIGHT_MEDIUM = QFont.Weight.Medium      # Medium weight
FONT_WEIGHT_BOLD = QFont.Weight.Bold          # Bold weight
FONT_WEIGHT_BLACK = QFont.Weight.Black        # Black weight

# ============================================================================
# PREDEFINED FONT OBJECTS
# ============================================================================

def create_font(size: int = FONT_SIZE_NORMAL, weight: QFont.Weight = FONT_WEIGHT_NORMAL, 
                family: str = FONT_FAMILY_DEFAULT, italic: bool = False) -> QFont:
    """
    Create a font object with specified properties.
    
    Args:
        size: Font size in points
        weight: Font weight (from QFont.Weight)
        family: Font family name
        italic: Whether the font should be italic
        
    Returns:
        QFont object configured with the specified properties
    """
    font = QFont(family)
    font.setPointSize(size)
    font.setWeight(weight)
    font.setItalic(italic)
    return font


# Common font objects
FONT_DEFAULT = create_font()
FONT_SMALL = create_font(size=FONT_SIZE_SMALL)
FONT_NORMAL = create_font(size=FONT_SIZE_NORMAL)
FONT_MEDIUM = create_font(size=FONT_SIZE_MEDIUM)
FONT_LARGE = create_font(size=FONT_SIZE_LARGE)
FONT_LARGE_BOLD = create_font(size=FONT_SIZE_LARGE, weight=FONT_WEIGHT_BOLD)
FONT_XLARGE = create_font(size=FONT_SIZE_XLARGE)
FONT_XLARGE_BOLD = create_font(size=FONT_SIZE_XLARGE, weight=FONT_WEIGHT_BOLD)
FONT_XXLARGE_BOLD = create_font(size=FONT_SIZE_XXLARGE, weight=FONT_WEIGHT_BOLD)
FONT_MONOSPACE = create_font(size=FONT_SIZE_NORMAL, family=FONT_FAMILY_MONOSPACE)
FONT_MONOSPACE_SMALL = create_font(size=FONT_SIZE_SMALL, family=FONT_FAMILY_MONOSPACE)
