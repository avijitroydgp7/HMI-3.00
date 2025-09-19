# TODO: Implement Color Selection Flow in Screen Design Template

## Tasks
- [ ] Modify `_create_fill_color_widget` in `main_window/dialogs/screen/screen_design.py` to add a "Select Colour" QPushButton instead of directly showing the ColorSwatchWidget.
- [ ] Add a new method `_open_color_swatch_dialog` in ScreenDesignDialog to open a QDialog containing the ColorSwatchWidget.
- [ ] Connect the `color_selected` signal from ColorSwatchWidget to update the color preview in the main dialog.
- [ ] Test the UI flow: Select "Fill Colour" -> Click "Select Colour" -> Opens color swatch dialog -> Click "More Colors..." -> Opens select color window.
- [ ] Verify that color selection updates the preview correctly.

## Dependent Files
- `main_window/dialogs/screen/screen_design.py`

## Notes
- Ensure the ColorSwatchWidget's "More Colors..." button opens the ColorSelector dialog as implemented.
- The dialog should be modal for better UX.
