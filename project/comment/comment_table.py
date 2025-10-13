# project/comment/comment_table.py
import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QToolBar, QTableWidget, QTableWidgetItem, 
    QLineEdit, QMessageBox, QAbstractItemView, QHeaderView, QApplication
)
from PyQt6.QtGui import QColor, QBrush, QFont, QPainter, QPen
from PyQt6.QtCore import Qt, QRegularExpression, QRectF, QPointF

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
        # The logic is now in Spreadsheet.mousePressEvent, so this is not strictly needed
        # but we leave it in case of other uses.
        self.table_widget.cellClicked.connect(self.handle_cell_click_for_formula)


    def handle_cell_click_for_formula(self, row, column):
        """Appends a cell reference to the formula bar if it's in formula-entry mode."""
        # This logic is mostly handled by Spreadsheet.mousePressEvent to keep focus,
        # but this can serve as a backup.
        if self.formula_bar.hasFocus() and self.formula_bar.text().startswith('='):
            cell_ref = self.table_widget.get_cell_ref_str(row, column)
            self.formula_bar.insert(cell_ref)


    def update_formula_bar(self, currentRow, currentColumn, previousRow, previousColumn):
        """Update the formula bar with the content of the selected cell."""
        item = self.table_widget.item(currentRow, currentColumn)
        if item:
            edit_data = item.data(Qt.ItemDataRole.EditRole)
            self.formula_bar.setText(str(edit_data) if edit_data is not None else "")

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
    """Custom item to store both formula and evaluated value."""
    def __init__(self, text=''):
        super().__init__()
        self.formula = None
        self.setData(Qt.ItemDataRole.EditRole, text)

    def setData(self, role, value):
        if role == Qt.ItemDataRole.EditRole:
            str_value = str(value)
            self.formula = str_value if str_value.startswith('=') else None
            super().setData(role, str_value)
            # Initially set display to the formula itself
            super().setData(Qt.ItemDataRole.DisplayRole, str_value)
        else:
            # This will be called by evaluate_cell to set the calculated result
            super().setData(role, value)


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
            bg_color = QColor("#E7F5E7")
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


class Spreadsheet(QTableWidget):
    """A QTableWidget with spreadsheet-like formula and fill capabilities."""
    def __init__(self, parent=None):
        super().__init__(20, 10, parent) # Default size 20 rows, 10 columns
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._is_dragging_fill_handle = False
        self._drag_start_pos = None
        self._drag_fill_rect = None
        self.referenced_cells = []
        self.ref_colors = [QColor("#0070C0"), QColor("#C00000"), QColor("#00B050"), QColor("#7030A0")]


        self.setHorizontalHeader(ExcelHeaderView(Qt.Orientation.Horizontal, self))
        self.setVerticalHeader(ExcelHeaderView(Qt.Orientation.Vertical, self))

        self.blockSignals(True)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.setItem(row, col, SpreadsheetItem())
        self.blockSignals(False)
        
        self.update_headers()
        
        self.itemSelectionChanged.connect(self.horizontalHeader().update)
        self.itemSelectionChanged.connect(self.verticalHeader().update)
        self.itemSelectionChanged.connect(self.viewport().update)
        self.itemChanged.connect(self.on_item_changed)
        parent.formula_bar.textChanged.connect(self.on_formula_bar_text_changed)


        self.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                outline: none;
                selection-background-color: transparent;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: white;
            }
        """)

    def on_formula_bar_text_changed(self, text):
        """Highlights cells referenced in the formula bar."""
        self.referenced_cells.clear()
        if text.startswith('='):
            # Find all cell references like A1, B2, etc.
            refs = re.findall(r"([A-Z]+)(\d+)", text.upper())
            for i, (col_str, row_str) in enumerate(refs):
                row = int(row_str) - 1
                col = self.col_str_to_int(col_str)
                color = self.ref_colors[i % len(self.ref_colors)]
                self.referenced_cells.append(((row, col), color))
        self.viewport().update()

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
        if not isinstance(item, SpreadsheetItem):
            return

        self.blockSignals(True)
        self.evaluate_all_cells()
        self.blockSignals(False)
        self.viewport().update()

    def evaluate_all_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item and isinstance(item, SpreadsheetItem) and item.formula:
                    self.evaluate_cell(item)

    def evaluate_cell(self, item):
        try:
            result = self.parse_formula(item.formula)
            item.setData(Qt.ItemDataRole.DisplayRole, str(result))
        except Exception as e:
            item.setData(Qt.ItemDataRole.DisplayRole, "#ERROR")
            print(f"Error evaluating formula '{item.formula}': {e}")
    
    def get_cell_value(self, row, col):
        item = self.item(row, col)
        if item:
            try:
                # Use EditRole to get value during calculation to avoid circular deps with display
                return float(item.data(Qt.ItemDataRole.DisplayRole))
            except (ValueError, TypeError):
                return 0.0
        return 0.0

    def parse_formula(self, formula):
        formula = formula[1:].upper()
        
        match = re.match(r"(\w+)\((.+)\)", formula)
        if match:
            func, args = match.groups()
            range_match = re.match(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", args)
            if range_match:
                start_col_str, start_row_str, end_col_str, end_row_str = range_match.groups()
                start_row, start_col = int(start_row_str) - 1, self.col_str_to_int(start_col_str)
                end_row, end_col = int(end_row_str) - 1, self.col_str_to_int(end_col_str)
                values = [self.get_cell_value(r, c) for r in range(start_row, end_row + 1) for c in range(start_col, end_col + 1)]
                if func == "SUM": return sum(values)
                if func == "AVERAGE": return sum(values) / len(values) if values else 0
                if func == "MAX": return max(values) if values else 0
                if func == "MIN": return min(values) if values else 0
        
        def replace_cell_ref(match_obj):
            col_str, row_str = match_obj.groups()
            row, col = int(row_str) - 1, self.col_str_to_int(col_str)
            return str(self.get_cell_value(row, col))
        
        formula = re.sub(r"([A-Z]+)(\d+)", replace_cell_ref, formula)
        return self.safe_eval(formula)

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
        
        # Draw borders for referenced cells
        for (row, col), color in self.referenced_cells:
            rect = self.visualRect(self.model().index(row, col))
            if rect.isValid():
                painter.setPen(QPen(color, 1, Qt.PenStyle.DashLine))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRect(rect.adjusted(0, 0, -1, -1))
        
        if not self.selectionModel().hasSelection():
            return
        
        selection = self.selectionModel().selection()
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
                target_item = SpreadsheetItem()
                target_item.setFont(source_item.font())
                if isinstance(source_item, SpreadsheetItem) and source_item.formula:
                    offset = target_row - source_row
                    new_formula = re.sub(r"([A-Z]+)(\d+)", lambda m: f"{m.group(1)}{int(m.group(2)) + offset}", source_item.formula)
                    target_item.setData(Qt.ItemDataRole.EditRole, new_formula)
                else:
                    try:
                        new_value = float(source_item.text()) + i
                        target_item.setText(str(int(new_value) if new_value.is_integer() else new_value))
                    except ValueError:
                        target_item.setText(source_item.text())
                self.setItem(target_row, col, target_item)
        self.evaluate_all_cells()

