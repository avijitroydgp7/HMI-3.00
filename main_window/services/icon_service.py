from PyQt6.QtGui import QIcon
import os

class IconService:
    ICON_DIR = os.path.join(os.path.dirname(__file__), "..", "resources", "icons")

    @staticmethod
    def get_icon(name: str) -> QIcon:
        """
        Loads an icon from the resources/icons directory.

        Args:
            name: The name of the icon to load (without the .svg extension).

        Returns:
            A QIcon object.
        """
        path = os.path.join(IconService.ICON_DIR, f"{name}.svg")
        if not os.path.exists(path):
            print(f"Warning: Icon '{name}' not found at '{path}'")
            return QIcon()
        return QIcon(path)
