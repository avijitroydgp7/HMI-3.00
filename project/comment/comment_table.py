# project/comment/comment_table.py
import re
import statistics
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QToolBar, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QAbstractItemView, QHeaderView, QApplication, QLabel,
    QStyledItemDelegate, QMenu, QListWidget
)
from main_window.widgets.color_selector import ColorSelector
from PyQt6.QtGui import (
    QColor, QBrush, QFont, QPainter, QPen, QKeySequence, QUndoStack, QUndoCommand
)
from PyQt6.QtCore import Qt, QRegularExpression, QRectF, QPointF, pyqtSignal
import operator

# --- Safe Formula Parser ---
# A robust parser to handle arithmetic, cell references, ranges, and a wide variety of functions.

class FormulaParser:
    def __init__(self, table, cell):
        self.table = table
        self.cell = cell
        self.ops = {
            '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,
            '^': operator.pow,
            '=': operator.eq, '==': operator.eq,
            '<': operator.lt, '>': operator.gt,
            '<=': operator.le, '>=': operator.ge, 
            '!=': operator.ne, '<>': operator.ne,
        }
        self.precedence = {
            '+': 1, '-': 1, '*': 2, '/': 2, '^': 3,
            '=': 0, '==': 0, '<': 0, '>': 0, '<=': 0, '>=': 0, '!=': 0, '<>': 0
        }
        self.functions = {
            'SUM': sum,
            'AVERAGE': statistics.mean,
            'MAX': max,
            'MIN': min,
            'COUNT': len,
            'IF': lambda cond, t_val, f_val: t_val if cond else f_val,
            'AND': lambda *args: all(args),
            'OR': lambda *args: any(args),
            'NOT': lambda x: not x,
            'TRUE': lambda: True,
            'FALSE': lambda: False,
            'UPPER': lambda s: str(s).upper(),
            'LOWER': lambda s: str(s).lower(),
            'LEN': lambda s: len(str(s)),
            'LEFT': lambda s, n=1: str(s)[:int(n)],
            'RIGHT': lambda s, n=1: str(s)[-int(n):],
            'MID': lambda s, start, n: str(s)[int(start)-1:int(start)-1+int(n)],
            'CONCAT': lambda *args: "".join(map(str, args)),
            'INT': int,
            'DEC2HEX': hex,
            'DEC2BIN': bin,
            'DEC2OCT': oct,
            'HEX2DEC': lambda h: int(h, 16),
            'HEX2BIN': lambda h: bin(int(h, 16)),
            'HEX2OCT': lambda h: oct(int(h, 16)),
            'BIN2DEC': lambda b: int(b, 2),
            'BIN2HEX': lambda b: hex(int(b, 2)),
            'BIN2OCT': lambda b: oct(int(b, 2)),
            'OCT2DEC': lambda o: int(o, 8),
            'OCT2BIN': lambda o: bin(int(o, 8)),
            'OCT2HEX': lambda o: hex(int(o, 8)),
            'CHAR': chr,
            'VLOOKUP': self._vlookup,
            'HLOOKUP': self._hlookup,
            'TRIM': lambda s: str(s).strip(),
            'REPLACE': lambda old_text, start_num, num_chars, new_text: self._replace(old_text, start_num, num_chars, new_text),
            'SUBSTITUTE': lambda text, old_text, new_text, instance_num=None: self._substitute(text, old_text, new_text, instance_num),
            'IFERROR': self._iferror,
            'IFNA': self._ifna,
        }

    def evaluate(self, expression):
        try:
            tokens = self._tokenize(expression)
            rpn = self._shunting_yard(tokens)
            return self._evaluate_rpn(rpn)
        except Exception as e:
            # Check for IFERROR/IFNA at the top level
            match = re.match(r"^\s*IF(ERROR|NA)\((.*)\)\s*$", expression, re.IGNORECASE)
            if match:
                func_type = match.group(1).upper()
                inner_expr = match.group(2)
                # This is a simplified fallback for top-level IFERROR/IFNA
                # The robust solution is within _evaluate_rpn
                try:
                    # Attempt to evaluate the value part
                    value_expr, value_if_error_expr = self._split_if_args(inner_expr)
                    self.evaluate(value_expr) # This will raise an error if it fails
                except Exception:
                    _, value_if_error_expr = self._split_if_args(inner_expr)
                    return self.evaluate(value_if_error_expr)

            raise e # Re-raise if not a top-level IFERROR/IFNA

    def _split_if_args(self, args_str):
        paren_level = 0
        split_index = -1
        for i, char in enumerate(args_str):
            if char == '(':
                paren_level += 1
            elif char == ')':
                paren_level -= 1
            elif char == ',' and paren_level == 0:
                split_index = i
                break
        if split_index == -1:
            raise ValueError("Invalid IFERROR/IFNA arguments")
        return args_str[:split_index], args_str[split_index+1:]
        
    def _tokenize(self, expression):
        token_specification = [
            ('FUNCTION',  r'[A-Z][A-Z0-9_]*\('),
            ('CELLRANGE', r'[A-Z]+[0-9]+:[A-Z]+[0-9]+'),
            ('CELL',      r'[A-Z]+[0-9]+'),
            ('NUMBER',    r'[0-9]+(\.[0-9]*)?'),
            ('OP',        r'<=|>=|<>|!=|==|<|>|[\+\-\*/\^]'),
            ('LPAREN',    r'\('),
            ('RPAREN',    r'\)'),
            ('COMMA',     r','),
            ('STRING',    r'"[^"]*"'),
            ('MISMATCH',  r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, expression, re.IGNORECASE):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'FUNCTION':
                tokens.append((kind, value[:-1].upper()))
                tokens.append(('LPAREN', '('))
            elif kind not in ['MISMATCH']:
                tokens.append((kind, value))
        return tokens

    def _shunting_yard(self, tokens):
        output = []
        operators = []
        arg_counts = []

        for i, (kind, value) in enumerate(tokens):
            if kind in ('NUMBER', 'CELL', 'CELLRANGE', 'STRING'):
                output.append((kind, value))
            elif kind == 'FUNCTION':
                operators.append((kind, value))
                if i + 1 < len(tokens) and tokens[i+1][0] == 'RPAREN':
                    arg_counts.append(0)
                else:
                    arg_counts.append(1)
            elif kind == 'COMMA':
                if not arg_counts: raise ValueError("Comma outside of function arguments")
                arg_counts[-1] += 1
                while operators and operators[-1][0] != 'LPAREN':
                    output.append(operators.pop())
            elif kind == 'OP':
                while (operators and operators[-1][0] == 'OP' and
                       self.precedence.get(operators[-1][1], 0) >= self.precedence.get(value, 0)):
                    output.append(operators.pop())
                operators.append((kind, value))
            elif kind == 'LPAREN':
                operators.append((kind, value))
            elif kind == 'RPAREN':
                while operators and operators[-1][0] != 'LPAREN':
                    output.append(operators.pop())
                if not operators or operators.pop()[0] != 'LPAREN':
                    raise ValueError("Mismatched parentheses")

                if operators and operators[-1][0] == 'FUNCTION':
                    func_token = operators.pop()
                    arg_count = arg_counts.pop() if arg_counts else 0
                    output.append(('FUNCTION_EXEC', (func_token[1], arg_count)))


        while operators:
            op_kind, op_val = operators.pop()
            if op_kind in ('LPAREN', 'RPAREN'):
                raise ValueError("Mismatched parentheses in operator stack")
            output.append((op_kind, op_val))
        return output

    def _evaluate_rpn(self, rpn_tokens):
        stack = []
        for kind, value in rpn_tokens:
            if kind == 'NUMBER':
                stack.append(float(value))
            elif kind == 'STRING':
                stack.append(value[1:-1])
            elif kind == 'CELL':
                row, col = self.table.cell_ref_to_indices(value)
                stack.append(self.table.get_cell_value(row, col, dependent_cell=self.cell))
            elif kind == 'CELLRANGE':
                stack.append(self._get_range_values(value))
            elif kind == 'OP':
                if len(stack) < 2: raise ValueError(f"Syntax Error: Not enough operands for '{value}'")
                right, left = stack.pop(), stack.pop()
                stack.append(self.ops[value](left, right))
            elif kind == 'FUNCTION_EXEC':
                func_name, arg_count = value
                if len(stack) < arg_count: raise ValueError(f"Not enough arguments for {func_name}")
                
                args = [stack.pop() for _ in range(arg_count)]
                args.reverse()

                flat_args = []
                for arg in args:
                    if isinstance(arg, list) and func_name not in ('VLOOKUP', 'HLOOKUP'):
                        flat_args.extend(arg)
                    else:
                        flat_args.append(arg)
                
                result = self.functions[func_name](*flat_args)
                stack.append(result)

        return stack[0] if stack else 0
        
    def _get_range_values(self, range_str, as_string=False):
        values = []
        start_ref, end_ref = range_str.split(':')
        start_row, start_col = self.table.cell_ref_to_indices(start_ref)
        end_row, end_col = self.table.cell_ref_to_indices(end_ref)

        if start_row > end_row: start_row, end_row = end_row, start_row
        if start_col > end_col: start_col, end_col = end_col, start_col

        for r in range(start_row, end_row + 1):
            row_values = []
            for c in range(start_col, end_col + 1):
                 row_values.append(self.table.get_cell_value(r, c, as_string=as_string, dependent_cell=self.cell))
            values.append(row_values)
        return values

    def _vlookup(self, lookup_value, table_array, col_index_num, range_lookup=True):
        col_index_num = int(col_index_num) - 1
        
        for row in table_array:
            if (range_lookup and str(lookup_value).lower() in str(row[0]).lower()) or \
               (not range_lookup and str(lookup_value) == str(row[0])):
                return row[col_index_num]
        return "#N/A"

    def _hlookup(self, lookup_value, table_array, row_index_num, range_lookup=True):
        row_index_num = int(row_index_num) - 1
        
        num_cols = len(table_array[0])
        for c in range(num_cols):
            if (range_lookup and str(lookup_value).lower() in str(table_array[0][c]).lower()) or \
               (not range_lookup and str(lookup_value) == str(table_array[0][c])):
                return table_array[row_index_num][c]
        return "#N/A"
        
    def _replace(self, old_text, start_num, num_chars, new_text):
        old_text = str(old_text)
        start_num = int(start_num) - 1
        num_chars = int(num_chars)
        return old_text[:start_num] + str(new_text) + old_text[start_num + num_chars:]

    def _substitute(self, text, old_text, new_text, instance_num=None):
        text = str(text)
        old_text = str(old_text)
        new_text = str(new_text)
        if instance_num:
            return text.replace(old_text, new_text, int(instance_num))
        return text.replace(old_text, new_text)

    def _iferror(self, value, value_if_error):
        # This will be called by the evaluation logic.
        # The value is already evaluated at this point.
        # We need a way to check if it was an error.
        # A simple check for string error codes can work here.
        if isinstance(value, str) and value.startswith('#'):
            return value_if_error
        return value

    def _ifna(self, value, value_if_na):
        if value == "#N/A":
            return value_if_na
        return value

# --- End Safe Formula Parser ---

# --- Undo Commands ---

class ChangeCellCommand(QUndoCommand):
    """An undo command for changing the data of one or more cells."""
    def __init__(self, table, changes, text="Cell Change"):
        super().__init__(text)
        self.table = table
        self.changes = changes

    def redo(self):
        self.table.blockSignals(True)
        for row, col, old_data, new_data in self.changes:
            item = self.table.item(row, col)
            if not item:
                item = SpreadsheetItem()
                self.table.setItem(row, col, item)
            item.set_data(new_data)
        self.table.blockSignals(False)
        self.table.evaluate_all_cells()
        self.table.viewport().update()
        self.table.save_data_to_service()

    def undo(self):
        self.table.blockSignals(True)
        for row, col, old_data, new_data in self.changes:
            item = self.table.item(row, col)
            if not item:
                item = SpreadsheetItem()
                self.table.setItem(row, col, item)
            item.set_data(old_data)
        self.table.blockSignals(False)
        self.table.evaluate_all_cells()
        self.table.viewport().update()
        self.table.save_data_to_service()

class ResizeCommand(QUndoCommand):
    """An undo command for adding/removing rows or columns."""
    def __init__(self, table, action, index, count=1):
        super().__init__(f"{action.replace('_', ' ').title()}")
        self.table = table
        self.action = action # 'add_row', 'remove_row', 'add_col', 'remove_col'
        self.index = index
        self.count = count # For future use
        self.data = []

    def redo(self):
        if self.action == 'add_row': self.table.insertRow(self.index)
        elif self.action == 'remove_row':
            self._store_data()
            self.table.removeRow(self.index)
        elif self.action == 'add_col': self.table.insertColumn(self.index)
        elif self.action == 'remove_col':
            self._store_data()
            self.table.removeColumn(self.index)
        self.table.update_headers()
        self.table.save_data_to_service()

    def undo(self):
        if self.action == 'add_row': self.table.removeRow(self.index)
        elif self.action == 'remove_row':
            self.table.insertRow(self.index)
            self._restore_data()
        elif self.action == 'add_col': self.table.removeColumn(self.index)
        elif self.action == 'remove_col':
            self.table.insertColumn(self.index)
            self._restore_data()
        self.table.update_headers()
        self.table.save_data_to_service()

    def _store_data(self):
        self.data = []
        if self.action == 'remove_row':
            for c in range(self.table.columnCount()):
                item = self.table.item(self.index, c)
                self.data.append(item.get_data() if item else {'value': ''})
        elif self.action == 'remove_col':
             for r in range(self.table.rowCount()):
                item = self.table.item(r, self.index)
                self.data.append(item.get_data() if item else {'value': ''})

    def _restore_data(self):
        if self.action == 'remove_row':
            for c, cell_data in enumerate(self.data):
                 self.table.item(self.index, c).set_data(cell_data)
        elif self.action == 'remove_col':
            for r, cell_data in enumerate(self.data):
                self.table.item(r, self.index).set_data(cell_data)

# --- End Undo Commands ---

class CommentTable(QWidget):
    """
    A widget that provides a spreadsheet-like interface for comments, 
    supporting formulas, cell referencing, and basic Excel features.
    """
    def __init__(self, comment_data, main_window, common_menu, comment_service, parent=None):
        super().__init__(parent)
        self.comment_data = comment_data
        self.main_window = main_window
        self.common_menu = common_menu
        self.comment_service = comment_service
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        toolbar = self._create_toolbar()
        self.formula_bar = QLineEdit()
        self.formula_bar.setPlaceholderText("Enter formula here")
        self.table_widget = Spreadsheet(self, self.comment_service, self.comment_data['number'])

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
        self.common_menu.fill_text_action.triggered.connect(self.table_widget.set_text_color)
        self.common_menu.fill_background_action.triggered.connect(self.table_widget.set_background_color)

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
            data = item.get_data()
            self.formula_bar.setText(str(data.get('value', '')))


    def update_cell_from_formula_bar(self):
        """Update the selected cell with the content from the formula bar."""
        current_item = self.table_widget.currentItem()
        if current_item:
            row = self.table_widget.currentRow()
            col = self.table_widget.currentColumn()
            
            old_data = current_item.get_data()
            new_data = old_data.copy()
            new_data['value'] = self.formula_bar.text()

            if new_data != old_data:
                changes = [(row, col, old_data, new_data)]
                command = ChangeCellCommand(self.table_widget, changes, "Edit Cell")
                self.table_widget.undo_stack.push(command)


class SpreadsheetItem(QTableWidgetItem):
    """Custom item that stores its data as a dictionary in UserRole."""
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data = {'value': ''}
        self.set_data(data)

    def get_data(self):
        """Returns the dictionary stored in the item."""
        return self.data(Qt.ItemDataRole.UserRole) or {'value': ''}

    def set_data(self, data):
        """Sets the data dictionary and updates the item's appearance."""
        self.setData(Qt.ItemDataRole.UserRole, data)
        
        # Update font
        font = QFont()
        font_data = data.get('font', {})
        font.setBold(font_data.get('bold', False))
        font.setItalic(font_data.get('italic', False))
        font.setUnderline(font_data.get('underline', False))
        self.setFont(font)
        
        # Update colors
        bg_color_str = data.get('bg_color')
        if bg_color_str:
            self.setBackground(QColor(bg_color_str))
        else:
            self.setBackground(QBrush()) # Reset to default
            
        text_color_str = data.get('text_color')
        if text_color_str:
            self.setForeground(QColor(text_color_str))
        else:
            self.setForeground(QBrush()) # Reset to default


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
        """Populate the editor with the raw value from the data dictionary."""
        data = index.model().data(index, Qt.ItemDataRole.UserRole) or {}
        value = data.get('value', '')
        if isinstance(editor, QLineEdit):
            editor.setText(str(value))
            
    def setModelData(self, editor, model, index):
        """When editing is finished, create a command to perform the change."""
        if isinstance(editor, QLineEdit):
            table = self.parent()
            new_value = editor.text()
            
            old_data = index.model().data(index, Qt.ItemDataRole.UserRole) or {'value': ''}
            new_data = old_data.copy()
            new_data['value'] = new_value

            if old_data != new_data:
                changes = [(index.row(), index.column(), old_data, new_data)]
                command = ChangeCellCommand(table, changes, "Edit Cell")
                table.undo_stack.push(command)

class Spreadsheet(QTableWidget):
    """A QTableWidget with spreadsheet-like formula and fill capabilities."""
    def __init__(self, parent=None, comment_service=None, comment_number=None):
        super().__init__(20, 10, parent) # Default size 20 rows, 10 columns
        self.comment_service = comment_service
        self.comment_number = comment_number
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._is_dragging_fill_handle = False
        self._drag_start_pos = None
        self._drag_fill_rect = None
        self._currently_evaluating = set()
        self.precedents = {} 
        self.highlighted_cells = set()
        self.referenced_cells = []
        self.ref_colors = [QColor("#54B8FF"), QColor("#FF3C3C"), QColor("#39FF92"), QColor("#BE6AFF")]
        
        self.undo_stack = QUndoStack(self)

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
            "TRIM": "TRIM(text)",
            "REPLACE": "REPLACE(old_text, start_num, num_chars, new_text)",
            "SUBSTITUTE": "SUBSTITUTE(text, old_text, new_text, [instance_num])",
            "IFERROR": "IFERROR(value, value_if_error)",
            "IFNA": "IFNA(value, value_if_na)",
        }
        # --- End Hinting Widgets ---

        self.setHorizontalHeader(ExcelHeaderView(Qt.Orientation.Horizontal, self))
        self.setVerticalHeader(ExcelHeaderView(Qt.Orientation.Vertical, self))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.delegate = SpreadsheetDelegate(self)
        self.setItemDelegate(self.delegate)
        # The delegate now handles updating the formula bar
        self.delegate.editingTextChanged.connect(parent.formula_bar.setText)

        self.blockSignals(True)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.setItem(row, col, SpreadsheetItem())
        self.blockSignals(False)
        
        self.update_headers()
        
        self.itemSelectionChanged.connect(self.on_selection_changed)
        parent.formula_bar.textChanged.connect(self.on_formula_bar_text_changed)

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

        self.load_data_from_service()

    def load_data_from_service(self):
        if not self.comment_service:
            return
        table_data = self.comment_service.get_table_data(self.comment_number)
        
        if not table_data:
            self.save_data_to_service() 
            return

        num_rows = len(table_data)
        num_cols = len(table_data[0]) if num_rows > 0 else 0
        self.setRowCount(num_rows)
        self.setColumnCount(num_cols)
        self.update_headers()

        self.blockSignals(True)
        for r, row_data in enumerate(table_data):
            for c, cell_data in enumerate(row_data):
                item = self.item(r, c)
                if not item:
                    item = SpreadsheetItem()
                    self.setItem(r, c, item)
                item.set_data(cell_data)
        self.blockSignals(False)
        self.evaluate_all_cells()

    def save_data_to_service(self):
        if not self.comment_service:
            return
        table_data = []
        for r in range(self.rowCount()):
            row_data = []
            for c in range(self.columnCount()):
                item = self.item(r, c)
                raw_data = item.get_data() if item else {'value': ''}
                row_data.append(raw_data)
            table_data.append(row_data)
        self.comment_service.update_table_data(self.comment_number, table_data)
        self.parent().main_window.project_modified()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        cut_action = menu.addAction("Cut")
        copy_action = menu.addAction("Copy")
        paste_action = menu.addAction("Paste")
        delete_action = menu.addAction("Delete")
        
        cut_action.triggered.connect(self.cut)
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)
        delete_action.triggered.connect(self.delete)
        
        paste_action.setEnabled(bool(QApplication.clipboard().text()))
        
        item = self.itemAt(event.pos())
        if item and str(item.get_data().get('value', '')).startswith('='):
            menu.addSeparator()
            trace_precedents_action = menu.addAction("Trace Precedents")
            trace_precedents_action.triggered.connect(self.trace_precedents)
            if self.highlighted_cells:
                clear_highlights_action = menu.addAction("Clear Highlights")
                clear_highlights_action.triggered.connect(self.clear_highlights)

        menu.exec(event.globalPos())

    def keyPressEvent(self, event):
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
        selection = self.selectedRanges()
        if not selection: return

        first_range = selection[0]
        rows = range(first_range.topRow(), first_range.bottomRow() + 1)
        cols = range(first_range.leftColumn(), first_range.rightColumn() + 1)
        
        clipboard_text = ""
        for r in rows:
            row_data = []
            for c in cols:
                item = self.item(r, c)
                if item:
                    row_data.append(str(item.get_data().get('value', '')))
                else:
                    row_data.append("")
            clipboard_text += "\t".join(row_data) + "\n"

        QApplication.clipboard().setText(clipboard_text)

    def cut(self):
        self.copy()
        self.delete()

    def delete(self):
        selection = self.selectedRanges()
        if not selection: return
        
        changes = []
        for r in selection:
            for row in range(r.topRow(), r.bottomRow() + 1):
                for col in range(r.leftColumn(), r.rightColumn() + 1):
                    item = self.item(row, col)
                    if item:
                        old_data = item.get_data()
                        if old_data.get('value'): # Only delete if there's content
                            new_data = old_data.copy()
                            new_data['value'] = ''
                            changes.append((row, col, old_data, new_data))
        
        if changes:
            command = ChangeCellCommand(self, changes, "Delete")
            self.undo_stack.push(command)

    def paste(self):
        selection = self.selectedRanges()
        if not selection: return

        start_row = selection[0].topRow()
        start_col = selection[0].leftColumn()

        clipboard_text = QApplication.clipboard().text()
        rows = clipboard_text.strip('\n').split('\n')
        
        changes = []
        for r, row_data in enumerate(rows):
            columns = row_data.split('\t')
            for c, cell_text in enumerate(columns):
                target_row = start_row + r
                target_col = start_col + c

                if target_row < self.rowCount() and target_col < self.columnCount():
                    item = self.item(target_row, target_col)
                    old_data = item.get_data() if item else {'value': ''}
                    new_data = old_data.copy()
                    new_data['value'] = cell_text
                    
                    if old_data != new_data:
                        changes.append((target_row, target_col, old_data, new_data))

        if changes:
            command = ChangeCellCommand(self, changes, "Paste")
            self.undo_stack.push(command)
        
    def undo(self):
        self.undo_stack.undo()

    def redo(self):
        self.undo_stack.redo()

    def on_selection_changed(self):
        self.horizontalHeader().update()
        self.verticalHeader().update()
        self.viewport().update()
        self.formula_hint.hide()
        self.completer_popup.hide()

    def on_formula_bar_text_changed(self, text):
        self.referenced_cells.clear()
        self.formula_hint.hide()
        self.completer_popup.hide()

        if text.startswith('='):
            text_upper = text.upper()
            
            # Show all functions if only "=" is typed
            if text == '=':
                self.show_completer_popup('')
                return

            refs = re.findall(r"([A-Z]+)(\d+)", text_upper)
            for i, (col_str, row_str) in enumerate(refs):
                row = int(row_str) - 1
                col = self.col_str_to_int(col_str)
                color = self.ref_colors[i % len(self.ref_colors)]
                self.referenced_cells.append(((row, col), color))

            syntax_match = re.search(r"([A-Z_]+)\(([^)]*)$", text_upper)
            if syntax_match:
                func_name = syntax_match.group(1)
                if func_name in self.FUNCTION_HINTS:
                    self.show_syntax_hint(func_name)
            else:
                completer_match = re.search(r"=([A-Z_]*)$", text_upper)
                if completer_match:
                    self.show_completer_popup(completer_match.group(1))


        self.viewport().update()

    def show_syntax_hint(self, func_name):
        hint_text = self.FUNCTION_HINTS[func_name]
        self.formula_hint.setText(hint_text)
        self.formula_hint.adjustSize()
        current_rect = self.visualRect(self.currentIndex())
        if current_rect.isValid():
            global_pos = self.viewport().mapToGlobal(current_rect.bottomLeft())
            self.formula_hint.move(global_pos)
            self.formula_hint.show()
    
    def show_completer_popup(self, partial_func):
        matches = [f for f in self.FUNCTION_HINTS if f.startswith(partial_func)]
        if matches:
            self.completer_popup.clear()
            self.completer_popup.addItems(matches)
            current_rect = self.visualRect(self.currentIndex())
            if current_rect.isValid():
                global_pos = self.viewport().mapToGlobal(current_rect.bottomLeft())
                self.completer_popup.move(global_pos)
                self.completer_popup.adjustSize()
                self.completer_popup.setMinimumWidth(150)
                self.completer_popup.show()

    def complete_formula(self, item):
        full_func = item.text()
        editor = self.focusWidget()
        if not isinstance(editor, QLineEdit):
             editor = self.parent().formula_bar
        
        current_text = editor.text()
        # Find the start of the partial function name
        last_equal = current_text.rfind('=')
        last_paren = current_text.rfind('(')
        last_comma = current_text.rfind(',')
        start_pos = max(last_equal, last_paren, last_comma) + 1
        
        new_text = current_text[:start_pos] + full_func + "("
        editor.setText(new_text)
        editor.setFocus()
        editor.setCursorPosition(len(new_text))
        self.completer_popup.hide()


    def get_cell_ref_str(self, row, col):
        col_str = ""
        temp = col
        while temp >= 0:
            col_str = chr(ord('A') + temp % 26) + col_str
            temp = temp // 26 - 1
        return f"{col_str}{row + 1}"

    def cell_ref_to_indices(self, ref):
        match = re.match(r"([A-Z]+)(\d+)", ref.upper())
        if not match:
            raise ValueError("Invalid cell reference")
        col_str, row_str = match.groups()
        row = int(row_str) - 1
        col = self.col_str_to_int(col_str)
        return row, col

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

    def evaluate_all_cells(self):
        self.precedents.clear()
        for _ in range(self.rowCount()):
            for row in range(self.rowCount()):
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    if item:
                        self.evaluate_cell(item)

    def evaluate_cell(self, item):
        data = item.get_data()
        formula = str(data.get('value', ''))
        if not formula.startswith('='):
            item.setText(formula)
            return
            
        cell_coords = (item.row(), item.column())
        if cell_coords in self._currently_evaluating:
            item.setText("#REF!")
            return

        self._currently_evaluating.add(cell_coords)

        try:
            parser = FormulaParser(self, cell_coords)
            result = parser.evaluate(formula[1:])
            
            if isinstance(result, bool):
                 item.setText(str(result).upper())
            elif isinstance(result, float) and result.is_integer():
                item.setText(str(int(result)))
            else:
                item.setText(f"{result:.2f}" if isinstance(result, float) else str(result))

        except Exception as e:
            item.setText("#ERROR")
        finally:
            if cell_coords in self._currently_evaluating:
                self._currently_evaluating.remove(cell_coords)

    def get_cell_value(self, row, col, as_string=False, dependent_cell=None):
        if dependent_cell:
            if dependent_cell not in self.precedents:
                self.precedents[dependent_cell] = set()
            self.precedents[dependent_cell].add((row, col))
            
        item = self.item(row, col)
        if not item: return "" if as_string else 0

        text = item.text()
        if as_string: return text
        
        try:
            return float(text)
        except (ValueError, TypeError):
             if text == 'TRUE': return True
             if text == 'FALSE': return False
             if text.startswith('#'): return text
             return 0

    def col_str_to_int(self, col_str):
        num = 0
        for char in col_str:
            num = num * 26 + (ord(char.upper()) - ord('A')) + 1
        return num - 1

    def add_column(self):
        command = ResizeCommand(self, 'add_col', self.currentColumn() + 1)
        self.undo_stack.push(command)

    def add_row(self):
        command = ResizeCommand(self, 'add_row', self.currentRow() + 1)
        self.undo_stack.push(command)

    def remove_column(self):
        if self.columnCount() > 0:
            command = ResizeCommand(self, 'remove_col', self.currentColumn())
            self.undo_stack.push(command)

    def remove_row(self):
        if self.rowCount() > 0:
            command = ResizeCommand(self, 'remove_row', self.currentRow())
            self.undo_stack.push(command)

    def set_bold(self): self._toggle_font_property('bold')
    def set_italic(self): self._toggle_font_property('italic')
    def set_underline(self): self._toggle_font_property('underline')

    def _toggle_font_property(self, prop_name):
        changes = []
        for item in self.selectedItems():
            old_data = item.get_data()
            new_data = old_data.copy()
            
            font_data = new_data.setdefault('font', {})
            font_data[prop_name] = not font_data.get(prop_name, False)
            
            changes.append((item.row(), item.column(), old_data, new_data))
        
        if changes:
            command = ChangeCellCommand(self, changes, f"Toggle {prop_name.title()}")
            self.undo_stack.push(command)
            
    def set_text_color(self):
        self._set_color('text_color', "Set Text Color")

    def set_background_color(self):
        self._set_color('bg_color', "Set Background Color")

    def _set_color(self, prop_name, command_text):
        initial_color = QColor("black")
        if self.currentItem():
            data = self.currentItem().get_data()
            color_str = data.get(prop_name)
            if color_str:
                initial_color = QColor(color_str)

        color = ColorSelector.getColor(initial_color, self)
        if not color.isValid():
            return

        changes = []
        for item in self.selectedItems():
            old_data = item.get_data()
            new_data = old_data.copy()
            new_data[prop_name] = color.name()
            changes.append((item.row(), item.column(), old_data, new_data))

        if changes:
            command = ChangeCellCommand(self, changes, command_text)
            self.undo_stack.push(command)


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
        if not fill_rows:
            return

        changes = []
        for col in range(source_range.leftColumn(), source_range.rightColumn() + 1):
            for i, target_row in enumerate(fill_rows, 1):
                source_row = source_range.topRow() + (i - 1) % source_range.rowCount()
                source_item = self.item(source_row, col)
                if not source_item: continue
                
                source_data = source_item.get_data()
                source_text = str(source_data.get('value', ''))
                
                new_data = source_data.copy()
                
                if source_text.startswith('='):
                    offset = target_row - source_row
                    new_data['value'] = re.sub(r"([A-Z]+)(\d+)", lambda m: f"{m.group(1)}{int(m.group(2)) + offset}", source_text, flags=re.IGNORECASE)
                else:
                    try:
                        match = re.match(r"^(.*?)(\d+)$", source_text)
                        if match:
                            prefix, num_str = match.groups()
                            new_value = int(num_str) + i
                            new_data['value'] = f"{prefix}{new_value}"
                        else:
                            new_data['value'] = source_text
                    except (ValueError, TypeError):
                        new_data['value'] = source_text

                target_item = self.item(target_row, col)
                old_data = target_item.get_data() if target_item else {'value': ''}
                changes.append((target_row, col, old_data, new_data))

        if changes:
            command = ChangeCellCommand(self, changes, "Fill Drag")
            self.undo_stack.push(command)
        
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