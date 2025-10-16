# project/comment/comment_table.py
import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QToolBar, QTableWidget, QTableWidgetItem, 
    QLineEdit, QMessageBox, QAbstractItemView, QHeaderView, QApplication, QLabel,
    QStyledItemDelegate, QMenu, QListWidget
)
from PyQt6.QtGui import QColor, QBrush, QFont, QPainter, QPen, QKeySequence
from PyQt6.QtCore import Qt, QRegularExpression, QRectF, QPointF, pyqtSignal

class CommentTable(QWidget):
    """
    A widget that provides a spreadsheet-like interface for comments, 
    supporting formulas, cell referencing, and basic Excel features.
    """
    def __init__(self, comment_data, main_window, common_menu, parent=None):
        super().__init__(parent)
        self.comment_data = comment_data
        self.main_window = main_window
        self.common_menu = common_menu
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        toolbar = self._create_toolbar()
        self.formula_bar = QLineEdit()
        self.formula_bar.setPlaceholderText("Enter formula here")
        self.table_widget = Spreadsheet(self)

        layout.addWidget(toolbar)
        layout.addWidget(self.formula_bar)
        layout.addWidget(self.table_widget)

        self._connect_signals()

    def _create_toolbar(self):
        toolbar = QToolBar("Comment Toolbar")
        toolbar.setIconSize(self.main_window.iconSize())

        toolbar.addAction(self.common_menu.add_column_action)
        toolbar.addAction(self.common_menu.add_row_action)
        toolbar.addAction(self.common_menu.remove_column_action)
        toolbar.addAction(self.common_menu.remove_row_action)
        toolbar.addSeparator()
        toolbar.addAction(self.common_menu.bold_action)
        toolbar.addAction(self.common_menu.italic_action)
        toolbar.addAction(self.common_menu.underline_action)
        toolbar.addAction(self.common_menu.fill_text_action)
        toolbar.addAction(self.common_menu.fill_background_action)
        return toolbar

    def _connect_signals(self):
        # Link toolbar actions to table methods
        self.common_menu.add_column_action.triggered.connect(self.table_widget.add_column)
        self.common_menu.add_row_action.triggered.connect(self.table_widget.add_row)
        self.common_menu.remove_column_action.triggered.connect(self.table_widget.remove_column)
        self.common_menu.remove_row_action.triggered.connect(self.table_widget.remove_row)
        self.common_menu.bold_action.triggered.connect(self.table_widget.set_bold)
        self.common_menu.italic_action.triggered.connect(self.table_widget.set_italic)
        self.common_menu.underline_action.triggered.connect(self.table_widget.set_underline)
        
        # Link formula bar and table selection
        self.table_widget.currentCellChanged.connect(self.update_formula_bar)
        self.formula_bar.returnPressed.connect(self.update_cell_from_formula_bar)
        self.table_widget.cellClicked.connect(self.handle_cell_click_for_formula)


    def handle_cell_click_for_formula(self, row, column):
        """Appends a cell reference to the formula bar if it's in formula-entry mode."""
        if self.formula_bar.hasFocus() and self.formula_bar.text().startswith('='):
            cell_ref = self.table_widget.get_cell_ref_str(row, column)
            self.formula_bar.insert(cell_ref)


    def update_formula_bar(self, currentRow, currentColumn, previousRow, previousColumn):
        """Update the formula bar with the raw formula/text of the selected cell."""
        item = self.table_widget.item(currentRow, currentColumn)
        if item:
            # Read from UserRole, which holds the raw formula/text
            raw_data = item.data(Qt.ItemDataRole.UserRole)
            self.formula_bar.setText(str(raw_data) if raw_data is not None else "")

    def update_cell_from_formula_bar(self):
        """Update the selected cell with the content from the formula bar."""
        if self.table_widget.currentItem():
            row = self.table_widget.currentRow()
            col = self.table_widget.currentColumn()
            self.table_widget.setItem(row, col, SpreadsheetItem(self.formula_bar.text()))


    # Placeholder slots for actions that need more implementation
    def fill_text(self):
        print(f"Action 'Fill Text' triggered for comment: {self.comment_data['name']}")
    
    def fill_background(self):
        print(f"Action 'Fill Background' triggered for comment: {self.comment_data['name']}")


class SpreadsheetItem(QTableWidgetItem):
    """Custom item that uses UserRole as the single source of truth for raw text/formulas."""
    def __init__(self, text=''):
        # Set initial display text
        super().__init__(text)
        # Store the raw text/formula in UserRole.
        self.setData(Qt.ItemDataRole.UserRole, text)


class ExcelHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setHighlightSections(False) 

    def paintSection(self, painter, rect, logicalIndex):
        is_selected = False
        table = self.parentWidget()
        if isinstance(table, QTableWidget):
            selected_ranges = table.selectedRanges()
            for r in selected_ranges:
                if self.orientation() == Qt.Orientation.Horizontal:
                    if r.leftColumn() <= logicalIndex <= r.rightColumn():
                        is_selected = True
                        break
                else: # Vertical
                    if r.topRow() <= logicalIndex <= r.bottomRow():
                        is_selected = True
                        break
        
        painter.save()
        
        if is_selected:
            bg_color = QColor("#9FFF9F")
            text_color = QColor("#0F5113")
            pen_color = QColor("#A0A0A0")
        else:
            bg_color = QColor("#f0f0f0")
            text_color = QColor("#212121")
            pen_color = QColor("#d0d0d0")

        painter.fillRect(rect, bg_color)

        painter.setPen(pen_color)
        if self.orientation() == Qt.Orientation.Horizontal:
            painter.drawLine(rect.topRight(), rect.bottomRight())
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        else:
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())
            painter.drawLine(rect.topRight(), rect.bottomRight())
            
        painter.setPen(text_color)
        text = self.model().headerData(logicalIndex, self.orientation())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(text))

        painter.restore()

class SpreadsheetDelegate(QStyledItemDelegate):
    editingTextChanged = pyqtSignal(str)

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.textChanged.connect(self.editingTextChanged)
        return editor

    def setEditorData(self, editor, index):
        """Populate the editor with the raw formula from UserRole."""
        value = index.model().data(index, Qt.ItemDataRole.UserRole)
        if isinstance(editor, QLineEdit):
            editor.setText(str(value) if value is not None else "")
            
    def setModelData(self, editor, model, index):
        """When editing is finished, save the text back to UserRole."""
        if isinstance(editor, QLineEdit):
            value = editor.text()
            model.setData(index, value, Qt.ItemDataRole.UserRole)

class Spreadsheet(QTableWidget):
    """A QTableWidget with spreadsheet-like formula and fill capabilities."""
    def __init__(self, parent=None):
        super().__init__(20, 10, parent) # Default size 20 rows, 10 columns
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._is_dragging_fill_handle = False
        self._drag_start_pos = None
        self._drag_fill_rect = None
        self._currently_evaluating = set() # For circular reference detection
        self.precedents = {} # For formula auditing
        self.highlighted_cells = set()
        self.referenced_cells = []
        self.ref_colors = [QColor("#54B8FF"), QColor("#FF3C3C"), QColor("#39FF92"), QColor("#BE6AFF")]
        
        # --- Formula Hinting Widgets ---
        self.formula_hint = QLabel(self)
        self.formula_hint.setStyleSheet("background-color: white; border: 1px solid #c0c0c0; padding: 4px; font-size: 9pt; color: #333;")
        self.formula_hint.setWindowFlags(Qt.WindowType.ToolTip)
        self.formula_hint.hide()

        self.completer_popup = QListWidget(self)
        self.completer_popup.setWindowFlags(Qt.WindowType.ToolTip)
        self.completer_popup.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #c0c0c0;
                font-size: 9pt;
                color: black;
            }
            QListWidget::item:hover { background-color: #f0f0f0; }
            QListWidget::item:selected { background-color: #0078d7; color: white; }
        """)
        self.completer_popup.hide()
        self.completer_popup.itemClicked.connect(self.complete_formula)


        self.FUNCTION_HINTS = {
            "SUM": "SUM(value1, [value2], ...)",
            "AVERAGE": "AVERAGE(value1, [value2], ...)",
            "MAX": "MAX(value1, [value2], ...)",
            "MIN": "MIN(value1, [value2], ...)",
            "COUNT": "COUNT(value1, [value2], ...)",
            "IF": "IF(logical_test, value_if_true, [value_if_false])",
            "IFERROR": "IFERROR(value, value_if_error)",
            "IFNA": "IFNA(value, value_if_na)",
            "AND": "AND(logical1, [logical2], ...)",
            "OR": "OR(logical1, [logical2], ...)",
            "NOT": "NOT(logical)",
            "TRUE": "TRUE()",
            "FALSE": "FALSE()",
            "UPPER": "UPPER(text)",
            "LOWER": "LOWER(text)",
            "LEN": "LEN(text)",
            "LEFT": "LEFT(text, [num_chars])",
            "RIGHT": "RIGHT(text, [num_chars])",
            "MID": "MID(text, start_num, num_chars)",
            "CONCAT": "CONCAT(text1, [text2], ...)",
            "INT": "INT(number)",
            "TRIM": "TRIM(text)",
            "REPLACE": "REPLACE(old_text, start_num, num_chars, new_text)",
            "SUBSTITUTE": "SUBSTITUTE(text, old_text, new_text, [instance_num])",
            "DEC2HEX": "DEC2HEX(number)",
            "DEC2BIN": "DEC2BIN(number)",
            "DEC2OCT": "DEC2OCT(number)",
            "HEX2DEC": "HEX2DEC(hex_number)",
            "HEX2BIN": "HEX2BIN(hex_number)",
            "HEX2OCT": "HEX2OCT(hex_number)",
            "BIN2DEC": "BIN2DEC(binary_number)",
            "BIN2HEX": "BIN2HEX(binary_number)",
            "BIN2OCT": "BIN2OCT(binary_number)",
            "OCT2DEC": "OCT2DEC(octal_number)",
            "OCT2BIN": "OCT2BIN(octal_number)",
            "OCT2HEX": "OCT2HEX(octal_number)",
            "CHAR": "CHAR(number)",
            "VLOOKUP": "VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])",
            "HLOOKUP": "HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])",
        }
        # --- End Hinting Widgets ---

        self.setHorizontalHeader(ExcelHeaderView(Qt.Orientation.Horizontal, self))
        self.setVerticalHeader(ExcelHeaderView(Qt.Orientation.Vertical, self))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.delegate = SpreadsheetDelegate(self)
        self.setItemDelegate(self.delegate)
        self.delegate.editingTextChanged.connect(parent.formula_bar.setText)


        self.blockSignals(True)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.setItem(row, col, SpreadsheetItem())
        self.blockSignals(False)
        
        self.update_headers()
        
        self.itemSelectionChanged.connect(self.on_selection_changed)
        # Use itemChanged signal for re-evaluation
        self.itemChanged.connect(self.on_item_changed)
        parent.formula_bar.textChanged.connect(self.on_formula_bar_text_changed)

        # Hide hints when application loses focus
        QApplication.instance().focusChanged.connect(self.on_focus_changed)


        self.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                outline: none;
                selection-background-color: transparent;
            }
            QTableWidget::item:selected {
                color: white; 
                background-color: transparent;
            }
        """)

    def contextMenuEvent(self, event):
        """Shows a context menu on right-click."""
        menu = QMenu(self)
        
        cut_action = menu.addAction("Cut")
        copy_action = menu.addAction("Copy")
        paste_action = menu.addAction("Paste")
        delete_action = menu.addAction("Delete")
        
        cut_action.triggered.connect(self.cut)
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)
        delete_action.triggered.connect(self.delete)
        
        # Check if there is anything to paste
        paste_action.setEnabled(bool(QApplication.clipboard().text()))
        
        item = self.itemAt(event.pos())
        if item and str(item.data(Qt.ItemDataRole.UserRole) or '').startswith('='):
            menu.addSeparator()
            trace_precedents_action = menu.addAction("Trace Precedents")
            trace_precedents_action.triggered.connect(self.trace_precedents)
            if self.highlighted_cells:
                clear_highlights_action = menu.addAction("Clear Highlights")
                clear_highlights_action.triggered.connect(self.clear_highlights)

        menu.exec(event.globalPos())

    def keyPressEvent(self, event):
        """Handle key press events for clipboard operations."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy()
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste()
        elif event.matches(QKeySequence.StandardKey.Cut):
            self.cut()
        elif event.matches(QKeySequence.StandardKey.SelectAll):
            self.selectAll()
        elif event.key() == Qt.Key.Key_Delete:
            self.delete()
        elif event.matches(QKeySequence.StandardKey.Undo):
            self.undo()
        elif event.matches(QKeySequence.StandardKey.Redo):
            self.redo()
        else:
            super().keyPressEvent(event)

    def copy(self):
        """Copies the selected cells' raw data to the clipboard."""
        selection = self.selectedRanges()
        if not selection:
            return

        first_range = selection[0]
        min_row, max_row = first_range.topRow(), first_range.bottomRow()
        min_col, max_col = first_range.leftColumn(), first_range.rightColumn()
        for r in selection:
            min_row = min(min_row, r.topRow())
            max_row = max(max_row, r.bottomRow())
            min_col = min(min_col, r.leftColumn())
            max_col = max(max_col, r.rightColumn())
        
        clipboard_text = ""
        for r in range(min_row, max_row + 1):
            row_data = []
            for c in range(min_col, max_col + 1):
                item = self.item(r, c)
                if item:
                    raw_data = item.data(Qt.ItemDataRole.UserRole)
                    row_data.append(str(raw_data) if raw_data is not None else "")
                else:
                    row_data.append("")
            clipboard_text += "\t".join(row_data) + "\n"

        QApplication.clipboard().setText(clipboard_text)

    def cut(self):
        """Cuts the selected cells' data."""
        self.copy()
        self.delete()

    def delete(self):
        """Deletes the content of the selected cells."""
        selection = self.selectedRanges()
        if not selection:
            return

        for r in selection:
            for row in range(r.topRow(), r.bottomRow() + 1):
                for col in range(r.leftColumn(), r.rightColumn() + 1):
                    item = self.item(row, col)
                    if item:
                        # Clear UserRole which holds the raw data.
                        # This will trigger on_item_changed to update the display.
                        item.setData(Qt.ItemDataRole.UserRole, "")
        self.evaluate_all_cells()

    def paste(self):
        """Pastes clipboard content into the table."""
        selection = self.selectedRanges()
        if not selection:
            return

        start_row = selection[0].topRow()
        start_col = selection[0].leftColumn()

        clipboard_text = QApplication.clipboard().text()
        rows = clipboard_text.strip('\n').split('\n')

        for r, row_data in enumerate(rows):
            columns = row_data.split('\t')
            for c, cell_text in enumerate(columns):
                target_row = start_row + r
                target_col = start_col + c

                if target_row < self.rowCount() and target_col < self.columnCount():
                    self.setItem(target_row, target_col, SpreadsheetItem(cell_text))
        
        self.evaluate_all_cells()
        
    def undo(self):
        # Full undo/redo is not implemented in this version.
        pass

    def redo(self):
        # Full undo/redo is not implemented in this version.
        pass


    def on_selection_changed(self):
        """Handles changes in cell selection."""
        self.horizontalHeader().update()
        self.verticalHeader().update()
        self.viewport().update()
        self.formula_hint.hide()
        self.completer_popup.hide()

    def on_formula_bar_text_changed(self, text):
        """Highlights cells referenced in the formula bar and shows function hints."""
        self.referenced_cells.clear()
        self.formula_hint.hide()
        self.completer_popup.hide()

        if text.startswith('='):
            text_upper = text.upper()
            
            # Find all cell references like A1, B2, etc.
            refs = re.findall(r"([A-Z]+)(\d+)", text_upper)
            for i, (col_str, row_str) in enumerate(refs):
                row = int(row_str) - 1
                col = self.col_str_to_int(col_str)
                color = self.ref_colors[i % len(self.ref_colors)]
                self.referenced_cells.append(((row, col), color))

            # Regex to find the function currently being typed or whose args are being edited
            syntax_match = re.search(r"([A-Z_]+)\(([^)]*)$", text_upper)
            if syntax_match:
                func_name = syntax_match.group(1)
                if func_name in self.FUNCTION_HINTS:
                    self.show_syntax_hint(func_name)
            else:
                # Regex to find a function name being typed
                completer_match = re.search(r"=([A-Z_]+)$", text_upper)
                if completer_match:
                    self.show_completer_popup(completer_match.group(1))

        self.viewport().update()

    def show_syntax_hint(self, func_name):
        """Displays the syntax hint for a given function."""
        hint_text = self.FUNCTION_HINTS[func_name]
        self.formula_hint.setText(hint_text)
        self.formula_hint.adjustSize()
        current_rect = self.visualRect(self.currentIndex())
        if current_rect.isValid():
            global_pos = self.viewport().mapToGlobal(current_rect.bottomLeft())
            self.formula_hint.move(global_pos)
            self.formula_hint.show()
    
    def show_completer_popup(self, partial_func):
        """Displays a popup with function suggestions."""
        matches = [f for f in self.FUNCTION_HINTS if f.startswith(partial_func)]
        if matches:
            self.completer_popup.clear()
            self.completer_popup.addItems(matches)
            current_rect = self.visualRect(self.currentIndex())
            if current_rect.isValid():
                # Map the local viewport coordinate to a global coordinate for the top-level popup
                global_pos = self.viewport().mapToGlobal(current_rect.bottomLeft())
                self.completer_popup.move(global_pos)
                self.completer_popup.adjustSize()
                self.completer_popup.setMinimumWidth(150)
                self.completer_popup.show()

    def complete_formula(self, item):
        """Completes the formula with the selected function."""
        full_func = item.text()
        editor = self.focusWidget()
        if not isinstance(editor, QLineEdit):
             editor = self.parent().formula_bar
        
        current_text = editor.text()
        # Use a case-insensitive match for completing
        match = re.search(r"=([a-zA-Z_]*)$", current_text)
        if match:
             start_pos = match.start(1)
             new_text = current_text[:start_pos] + full_func + "("
             editor.setText(new_text)
             editor.setFocus()
             # Move cursor to the end
             editor.setCursorPosition(len(new_text))
        self.completer_popup.hide()


    def get_cell_ref_str(self, row, col):
        col_str = ""
        temp = col
        while temp >= 0:
            col_str = chr(ord('A') + temp % 26) + col_str
            temp = temp // 26 - 1
        return f"{col_str}{row + 1}"

    def update_headers(self):
        col_count = self.columnCount()
        col_headers = []
        for i in range(col_count):
            header = ""
            temp = i
            while temp >= 0:
                header = chr(ord('A') + temp % 26) + header
                temp = temp // 26 - 1
            col_headers.append(header)
        self.setHorizontalHeaderLabels(col_headers)

        row_headers = [str(i+1) for i in range(self.rowCount())]
        self.setVerticalHeaderLabels(row_headers)

    def on_item_changed(self, item):
        """
        Triggered when an item's data changes. We use this to re-evaluate all cells,
        as a change in one cell (e.g., via the editor) can affect others.
        """
        if not isinstance(item, QTableWidgetItem):
            return

        self.blockSignals(True)
        self.evaluate_all_cells()
        self.blockSignals(False)
        self.viewport().update()

    def evaluate_all_cells(self):
        self._currently_evaluating.clear() # Reset for a new evaluation cycle
        self.precedents.clear()
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item:
                    self.evaluate_cell(item)

    def evaluate_cell(self, item):
        """Evaluates the formula in a cell (if any) and updates its display text."""
        formula = str(item.data(Qt.ItemDataRole.UserRole) or '')
        if not formula.startswith('='):
            item.setText(formula)
            return

        try:
            result = self.parse_formula(formula, (item.row(), item.column()))
            
            if isinstance(result, bool):
                 item.setText(str(result).upper())
            elif isinstance(result, float) and result.is_integer():
                item.setText(str(int(result)))
            else:
                item.setText(str(result))

        except Exception as e:
            item.setText("#ERROR")

    def get_cell_value(self, row, col, as_string=False, dependent_cell=None):
        if dependent_cell:
            if dependent_cell not in self.precedents:
                self.precedents[dependent_cell] = set()
            self.precedents[dependent_cell].add((row, col))
            
        item = self.item(row, col)
        if not item:
            return "" if as_string else 0

        if (row, col) in self._currently_evaluating:
            return 0 

        raw_data = str(item.data(Qt.ItemDataRole.UserRole) or '')

        value = ""
        if raw_data.startswith('='):
            self._currently_evaluating.add((row, col))
            try:
                value = self.parse_formula(raw_data, (row, col))
            except Exception:
                value = "#ERROR"
            finally:
                self._currently_evaluating.remove((row, col))
        else:
            value = raw_data

        if as_string:
            return str(value)

        try:
            if isinstance(value, bool):
                return 1.0 if value else 0.0
            if isinstance(value, str):
                val_upper = value.upper()
                if val_upper == 'TRUE': return 1.0
                if val_upper == 'FALSE': return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0

    def _get_range_values(self, range_str, dependent_cell=None):
        range_match = re.match(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", range_str.upper())
        if not range_match:
            cell_match = re.match(r"([A-Z]+)(\d+)", range_str.upper())
            if cell_match:
                col_str, row_str = cell_match.groups()
                row, col = int(row_str) - 1, self.col_str_to_int(col_str)
                return [[self.get_cell_value(row, col, as_string=True, dependent_cell=dependent_cell)]]
            return []

        start_col_str, start_row_str, end_col_str, end_row_str = range_match.groups()
        start_row, start_col = int(start_row_str) - 1, self.col_str_to_int(start_col_str)
        end_row, end_col = int(end_row_str) - 1, self.col_str_to_int(end_col_str)
        
        table_data = []
        for r in range(start_row, end_row + 1):
            row_data = []
            for c in range(start_col, end_col + 1):
                row_data.append(self.get_cell_value(r, c, as_string=True, dependent_cell=dependent_cell))
            table_data.append(row_data)
        return table_data

    def _evaluate_expression_part(self, part_str, dependent_cell):
        """Evaluates a part of an expression to a value (string, number, or boolean)."""
        part_str = part_str.strip()
        if part_str.startswith('"') and part_str.endswith('"'):
            return part_str[1:-1]
        
        try:
            return float(part_str)
        except (ValueError, TypeError):
            pass

        return self.parse_formula("=" + part_str, dependent_cell)

    def _evaluate_logical_expression(self, expr, dependent_cell):
        """Evaluates an expression that should result in a boolean."""
        expr = expr.strip()
        
        match = re.match(r'(.+?)\s*(>=|<=|<>|!=|>|<|=)\s*(.+)', expr, re.IGNORECASE)
        if match:
            left_str, op, right_str = match.groups()
            
            left_val = self._evaluate_expression_part(left_str, dependent_cell)
            right_val = self._evaluate_expression_part(right_str, dependent_cell)

            try:
                left_num = float(left_val)
                right_num = float(right_val)
                if op == "=": return left_num == right_num
                if op == ">": return left_num > right_num
                if op == "<": return left_num < right_num
                if op == ">=": return left_num >= right_num
                if op == "<=": return left_num <= right_num
                if op == "<>" or op == "!=": return left_num != right_num
            except (ValueError, TypeError):
                left_s = str(left_val).upper()
                right_s = str(right_val).upper()
                if op == "=": return left_s == right_s
                if op == "<>" or op == "!=": return left_s != right_s
                return False
        
        val = self.parse_formula("=" + expr, dependent_cell)
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, str):
            val_upper = val.upper()
            if val_upper == 'TRUE': return True
            if val_upper == 'FALSE': return False
            try:
                return float(val) != 0
            except ValueError:
                return False
        return bool(val)

    def parse_formula(self, formula, current_cell=None):
        expression = formula[1:].strip()

        func_match = re.match(r"\s*(\w+)\s*\((.*)\)\s*$", expression, re.IGNORECASE)
        if func_match:
            func_name = func_match.group(1).upper()
            args_str = func_match.group(2)
            
            if func_name in self.FUNCTION_HINTS:
                args = self._parse_args(args_str)

                if func_name == "IF":
                    if len(args) < 2 or len(args) > 3: raise ValueError("IF arguments")
                    condition = self._evaluate_logical_expression(args[0], current_cell)
                    if condition:
                        return self._evaluate_expression_part(args[1], current_cell)
                    else:
                        return self._evaluate_expression_part(args[2], current_cell) if len(args) == 3 else False

                if func_name == "IFERROR":
                    if len(args) != 2: raise ValueError("IFERROR requires 2 arguments")
                    try:
                        value = self._evaluate_expression_part(args[0], current_cell)
                        if isinstance(value, str) and value.startswith("#"):
                            raise ValueError("Error Value")
                        return value
                    except Exception:
                        return self._evaluate_expression_part(args[1], current_cell)

                if func_name == "IFNA":
                    if len(args) != 2: raise ValueError("IFNA requires 2 arguments")
                    try:
                        value = self._evaluate_expression_part(args[0], current_cell)
                        if str(value) == "#N/A":
                            return self._evaluate_expression_part(args[1], current_cell)
                        return value
                    except Exception as e:
                        raise e

                if func_name == "AND": return all(self._evaluate_logical_expression(arg, current_cell) for arg in args)
                if func_name == "OR": return any(self._evaluate_logical_expression(arg, current_cell) for arg in args)
                if func_name == "NOT": return not self._evaluate_logical_expression(args[0], current_cell)
                if func_name == "TRUE": return True
                if func_name == "FALSE": return False

                if func_name == "VLOOKUP":
                    lookup_value = self._evaluate_expression_part(args[0], current_cell)
                    table_array = self._get_range_values(args[1], dependent_cell=current_cell)
                    col_index = int(self._evaluate_expression_part(args[2], current_cell))
                    if not table_array or col_index > len(table_array[0]): raise ValueError("VLOOKUP error")
                    for row_data in table_array:
                        if str(row_data[0]) == str(lookup_value): return row_data[col_index - 1]
                    return "#N/A"

                if func_name == "HLOOKUP":
                    lookup_value = self._evaluate_expression_part(args[0], current_cell)
                    table_array = self._get_range_values(args[1], dependent_cell=current_cell)
                    row_index = int(self._evaluate_expression_part(args[2], current_cell))
                    if not table_array or row_index > len(table_array): raise ValueError("HLOOKUP error")
                    for col_idx, cell_val in enumerate(table_array[0]):
                        if str(cell_val) == str(lookup_value): return table_array[row_index - 1][col_idx]
                    return "#N/A"

                if func_name in ["UPPER", "LOWER", "LEN", "CONCAT", "LEFT", "RIGHT", "MID", "TRIM", "REPLACE", "SUBSTITUTE", "HEX2DEC", "HEX2BIN", "HEX2OCT", "BIN2DEC", "BIN2HEX", "BIN2OCT", "OCT2DEC", "OCT2BIN", "OCT2HEX"]:
                    vals = self._evaluate_args(args, as_string=True, dependent_cell=current_cell)
                    if func_name == "UPPER": return str(vals[0]).upper()
                    if func_name == "LOWER": return str(vals[0]).lower()
                    if func_name == "LEN": return len(str(vals[0]))
                    if func_name == "CONCAT": return "".join(map(str, vals))
                    if func_name == "LEFT": return str(vals[0])[:int(float(vals[1])) if len(vals) > 1 else 1]
                    if func_name == "RIGHT": return str(vals[0])[-int(float(vals[1])) if len(vals) > 1 else -1:]
                    if func_name == "MID": return str(vals[0])[int(float(vals[1]))-1:int(float(vals[1]))-1+int(float(vals[2]))]
                    if func_name == "TRIM": return str(vals[0]).strip()
                    if func_name == "REPLACE":
                        o, s, n, new = vals; s, n = int(s), int(n); return o[:s-1] + new + o[s-1+n:]
                    if func_name == "SUBSTITUTE":
                        t, o, n = vals[:3]; i = int(vals[3]) if len(vals) > 3 else 0
                        return t.replace(o, n, i) if i > 0 else t.replace(o, n)
                    if func_name == "HEX2DEC": return str(int(str(vals[0]), 16))
                    if func_name == "HEX2BIN": return bin(int(str(vals[0]), 16))[2:]
                    # ... other conversions
                else:
                    vals = self._evaluate_args(args, as_string=False, dependent_cell=current_cell)
                    if func_name == "SUM": return sum(vals)
                    if func_name == "AVERAGE": return sum(vals) / len(vals) if vals else 0
                    if func_name == "MAX": return max(vals) if vals else 0
                    if func_name == "MIN": return min(vals) if vals else 0
                    if func_name == "COUNT": return len(vals)
                    if func_name == "INT": return int(vals[0]) if vals else 0
                    if func_name == "DEC2HEX": return hex(int(vals[0]))[2:].upper()
                    # ... other conversions
            else:
                raise ValueError(f"Unknown function: {func_name}")

        cell_match = re.match(r"^\s*([A-Z]+)(\d+)\s*$", expression, re.IGNORECASE)
        if cell_match:
            col_str, row_str = cell_match.groups()
            row, col = int(row_str) - 1, self.col_str_to_int(col_str)
            return self.get_cell_value(row, col, dependent_cell=current_cell)

        if '&' in expression:
            parts = self._parse_operator_expression(expression, '&')
            return "".join(str(self._evaluate_expression_part(p, current_cell)) for p in parts)

        try:
            expression_with_values = re.sub(r"([A-Z]+)(\d+)", lambda m: str(self.get_cell_value(int(m.group(2))-1, self.col_str_to_int(m.group(1)), dependent_cell=current_cell)), expression, flags=re.IGNORECASE)
            expression_with_values = re.sub(r'TRUE', '1', expression_with_values, flags=re.IGNORECASE)
            expression_with_values = re.sub(r'FALSE', '0', expression_with_values, flags=re.IGNORECASE)
            return self.safe_eval(expression_with_values)
        except Exception:
            return expression

    def _parse_operator_expression(self, expression_str, operator):
        parts, current_part, in_quotes, p_level = [], "", False, 0
        for char in expression_str:
            if char == '"': in_quotes = not in_quotes
            elif char == '(' and not in_quotes: p_level += 1
            elif char == ')' and not in_quotes: p_level -= 1
            if char == operator and not in_quotes and p_level == 0:
                parts.append(current_part.strip()); current_part = ""
            else: current_part += char
        parts.append(current_part.strip())
        return parts

    def _parse_args(self, args_str):
        return self._parse_operator_expression(args_str, ',')

    def _evaluate_args(self, args, as_string=False, dependent_cell=None):
        values = []
        for arg in args:
            if not arg.strip(): continue
            arg_upper = arg.strip().upper()
            range_match = re.match(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", arg_upper)
            if range_match:
                s_col, s_row, e_col, e_row = range_match.groups()
                for r in range(int(s_row) - 1, int(e_row)):
                    for c in range(self.col_str_to_int(s_col), self.col_str_to_int(e_col) + 1):
                        values.append(self.get_cell_value(r, c, as_string=as_string, dependent_cell=dependent_cell))
            else:
                values.append(self._evaluate_expression_part(arg, dependent_cell))
        
        if as_string: return [str(v) for v in values]
        else:
            numeric_values = []
            for v in values:
                if isinstance(v, (int, float)): numeric_values.append(v)
                elif isinstance(v, bool): numeric_values.append(1.0 if v else 0.0)
                else:
                    try: numeric_values.append(float(v))
                    except (ValueError, TypeError): numeric_values.append(0.0)
            return numeric_values

    def safe_eval(self, expression):
        allowed_chars = "0123456789.+-*/() "
        if all(c in allowed_chars for c in expression):
            return eval(expression)
        raise ValueError("Unsupported characters in formula")

    def col_str_to_int(self, col_str):
        num = 0
        for char in col_str:
            num = num * 26 + (ord(char.upper()) - ord('A')) + 1
        return num - 1

    def add_column(self): 
        self.insertColumn(self.currentColumn() + 1)
        self.update_headers()
    def add_row(self): 
        self.insertRow(self.currentRow() + 1)
        self.update_headers()
    def remove_column(self): 
        self.removeColumn(self.currentColumn())
        self.update_headers()
    def remove_row(self): 
        self.removeRow(self.currentRow())
        self.update_headers()

    def set_bold(self): self._toggle_font_property(QFont.Weight.Bold, 700)
    def set_italic(self): self._toggle_font_property("setItalic")
    def set_underline(self): self._toggle_font_property("setUnderline")

    def _toggle_font_property(self, prop, value=None):
        for item in self.selectedItems():
            font = item.font()
            if isinstance(prop, str):
                current_state = getattr(font, prop)()
                getattr(font, prop)(not current_state)
            else:
                 font.setWeight(QFont.Weight.Normal if font.weight() > QFont.Weight.Normal else value)
            item.setFont(font)

    def get_fill_handle_rect(self):
        selected_ranges = self.selectedRanges()
        if not selected_ranges: return None
        last_range = selected_ranges[-1]
        last_item = self.item(last_range.bottomRow(), last_range.rightColumn())
        if not last_item: return None
        last_cell_rect = self.visualItemRect(last_item)
        if last_cell_rect.isValid():
            return QRectF(last_cell_rect.right() - 4, last_cell_rect.bottom() - 4, 8, 8)
        return None

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        
        for (row, col), color in self.referenced_cells:
            rect = self.visualRect(self.model().index(row, col))
            if rect.isValid():
                painter.setPen(QPen(color, 1, Qt.PenStyle.DashLine))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRect(rect.adjusted(0, 0, -1, -1))
        
        for (row, col) in self.highlighted_cells:
            rect = self.visualRect(self.model().index(row, col))
            if rect.isValid():
                painter.setPen(QPen(QColor("blue"), 2))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRect(rect.adjusted(0, 0, -1, -1))
                
        if not self.selectionModel().hasSelection():
            return
        
        selection = self.selectionModel().selection()
        current_index = self.currentIndex()

        if len(selection.indexes()) > 1:
            for sel_range in selection:
                for index in sel_range.indexes():
                    if index != current_index:
                        rect = self.visualRect(index)
                        painter.fillRect(rect, QColor(217, 217, 217, 128))

        selection_rect = self.visualRegionForSelection(selection).boundingRect()
        
        painter.setPen(QPen(QColor(34, 139, 34), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(selection_rect.adjusted(0, 0, -1, -1))
        
        handle_rect = self.get_fill_handle_rect()
        if handle_rect:
            painter.setBrush(QBrush(QColor(34, 139, 34)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(handle_rect)

        if self._is_dragging_fill_handle and self._drag_fill_rect:
            painter.setPen(QPen(QColor(105, 105, 105), 1, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(self._drag_fill_rect)

    def mousePressEvent(self, event):
        self.clear_highlights()
        comment_table = self.parent()
        
        is_editing_in_formula_bar = comment_table.formula_bar.hasFocus() and comment_table.formula_bar.text().startswith('=')
        
        is_editing_in_cell = self.state() == QAbstractItemView.State.EditingState
        editor = QApplication.focusWidget() if is_editing_in_cell else None
        
        if is_editing_in_formula_bar or (is_editing_in_cell and isinstance(editor, QLineEdit) and editor.text().startswith('=')):
            index = self.indexAt(event.pos())
            if index.isValid():
                cell_ref = self.get_cell_ref_str(index.row(), index.column())
                if is_editing_in_formula_bar:
                    comment_table.formula_bar.insert(cell_ref)
                else:
                    editor.insert(cell_ref)
            return

        handle_rect = self.get_fill_handle_rect()
        if handle_rect and handle_rect.contains(event.position()):
            self._is_dragging_fill_handle = True
            self._drag_start_pos = event.position()
            self.setCursor(Qt.CursorShape.CrossCursor)
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self._is_dragging_fill_handle:
            selection_range = self.selectedRanges()[0]
            start_rect = self.visualItemRect(self.item(selection_range.topRow(), selection_range.leftColumn()))
            clamped_pos = event.position()
            if clamped_pos.y() > self.viewport().height():
                 clamped_pos.setY(float(self.viewport().height()))
            self._drag_fill_rect = QRectF(QPointF(start_rect.topLeft()), clamped_pos).normalized()
            self.viewport().update()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._is_dragging_fill_handle:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            if self._drag_fill_rect:
                end_row = self.rowAt(int(self._drag_fill_rect.bottom()))
                if end_row == -1: end_row = self.rowCount() - 1
                self.perform_fill_drag(end_row)
            self._is_dragging_fill_handle = False
            self._drag_start_pos = None
            self._drag_fill_rect = None
            self.viewport().update()
        else:
            super().mouseReleaseEvent(event)

    def perform_fill_drag(self, end_row):
        source_range = self.selectedRanges()[0]
        fill_rows = range(source_range.bottomRow() + 1, end_row + 1)
        for col in range(source_range.leftColumn(), source_range.rightColumn() + 1):
            for i, target_row in enumerate(fill_rows, 1):
                source_row = source_range.topRow() + (i-1) % source_range.rowCount()
                source_item = self.item(source_row, col)
                if not source_item: continue
                
                source_text = str(source_item.data(Qt.ItemDataRole.UserRole) or '')
                
                new_text = ""
                if source_text.startswith('='):
                    offset = target_row - source_row
                    new_text = re.sub(r"([A-Z]+)(\d+)", lambda m: f"{m.group(1)}{int(m.group(2)) + offset}", source_text, flags=re.IGNORECASE)
                else:
                    try:
                        new_value = float(source_text) + i
                        new_text = str(int(new_value) if new_value.is_integer() else new_value)
                    except (ValueError, TypeError):
                        new_text = source_text

                target_item = SpreadsheetItem(new_text)
                target_item.setFont(source_item.font())
                self.setItem(target_row, col, target_item)
        
        self.evaluate_all_cells()
        
    def trace_precedents(self):
        current_item = self.currentItem()
        if not current_item:
            return
        cell = (current_item.row(), current_item.column())
        if cell in self.precedents:
            self.highlighted_cells.update(self.precedents[cell])
            self.viewport().update()
            
    def clear_highlights(self):
        self.highlighted_cells.clear()
        self.viewport().update()

    def on_focus_changed(self, old, new):
        """Hide hints when application loses focus."""
        self.formula_hint.hide()
        self.completer_popup.hide()
