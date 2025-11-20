import copy
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QToolBar, QComboBox, QMessageBox, QStyledItemDelegate, QCheckBox,
    QAbstractItemView, QLineEdit, QApplication, QSizePolicy,
    QDateEdit, QTimeEdit, QDateTimeEdit
)
from PyQt6.QtCore import Qt, QMimeData, QDate, QTime, QDateTime
from PyQt6.QtGui import QAction, QUndoStack, QUndoCommand, QKeySequence, QColor, QBrush
from main_window.services.icon_service import IconService

# Define validation ranges for data types
DATA_TYPE_RANGES = {
    "Bit": (0, 1),
    "Sign Int8": (-128, 127),
    "Sign Int16": (-32768, 32767),
    "Sign Int32": (-2147483648, 2147483647),
    "Unsign Int8": (0, 255),
    "Unsign Int16": (0, 65535),
    "Unsign Int32": (0, 4294967295),
}

# --- Undo Commands ---

class TagChangeCommand(QUndoCommand):
    """Command for changing a single cell's value."""
    def __init__(self, table, row, col, old_val, new_val, text="Edit Tag"):
        super().__init__(text)
        self.table = table
        self.row = row
        self.col = col
        self.old_val = old_val
        self.new_val = new_val

    def redo(self):
        self.table.block_signals(True)
        self.table._set_cell_value(self.row, self.col, self.new_val)
        self.table.block_signals(False)
        self.table.save_data()

    def undo(self):
        self.table.block_signals(True)
        self.table._set_cell_value(self.row, self.col, self.old_val)
        self.table.block_signals(False)
        self.table.save_data()

class TagAddCommand(QUndoCommand):
    """Command for adding a new tag."""
    def __init__(self, table, row_index, tag_data, text="Add Tag"):
        super().__init__(text)
        self.table = table
        self.row_index = row_index
        self.tag_data = tag_data

    def redo(self):
        self.table.block_signals(True)
        self.table._insert_row_visual(self.row_index, self.tag_data)
        self.table.block_signals(False)
        self.table.save_data()

    def undo(self):
        self.table.block_signals(True)
        self.table.table.removeRow(self.row_index)
        self.table.block_signals(False)
        self.table.save_data()

class TagRemoveCommand(QUndoCommand):
    """Command for removing tags."""
    def __init__(self, table, rows_data, text="Remove Tag"):
        super().__init__(text)
        self.table = table
        # rows_data is a list of tuples: (row_index, tag_data_dict)
        # Sort by row index descending to handle removals correctly
        self.rows_data = sorted(rows_data, key=lambda x: x[0], reverse=True)

    def redo(self):
        self.table.block_signals(True)
        for row, _ in self.rows_data:
            self.table.table.removeRow(row)
        self.table.block_signals(False)
        self.table.save_data()

    def undo(self):
        self.table.block_signals(True)
        # Re-insert in reverse order of removal (ascending index)
        for row, data in reversed(self.rows_data):
            self.table._insert_row_visual(row, data)
        self.table.block_signals(False)
        self.table.save_data()

# --- Delegates ---

class DataTypeDelegate(QStyledItemDelegate):
    def __init__(self, tag_table, parent=None):
        super().__init__(parent)
        self.tag_table = tag_table
        self.data_types = [
            "Bit", "Sign Int8", "Sign Int16", "Sign Int32",
            "Unsign Int8", "Unsign Int16", "Unsign Int32",
            "Real", "Time", "Date", "Date Time",
            "String", "Timer", "Counter"
        ]

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(self.data_types)
        # Style the editor to match the dark theme
        # editor.setStyleSheet("""
        #     QComboBox {
        #         background-color: #2b2b2b;
        #         color: #dcdcdc;
        #         border: 1px solid #555555;
        #         padding: 2px;
        #     }
        #     QComboBox::drop-down {
        #         border: none;
        #     }
        #     QComboBox QAbstractItemView {
        #         background-color: #2b2b2b;
        #         color: #dcdcdc;
        #         selection-background-color: #3a3a3a;
        #     }
        # """)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        if value in self.data_types:
            editor.setCurrentText(value)
        # Open the popup immediately to simulate single-click behavior
        editor.showPopup()

    def setModelData(self, editor, model, index):
        new_val = editor.currentText()
        old_val = index.model().data(index, Qt.ItemDataRole.EditRole)
        
        if new_val != old_val:
            # Begin a macro so that changing type and resetting value are one undo step
            self.tag_table.undo_stack.beginMacro("Change Data Type")

            # 1. Change the Data Type
            cmd_type = TagChangeCommand(self.tag_table, index.row(), index.column(), old_val, new_val, "Change Data Type")
            self.tag_table.undo_stack.push(cmd_type)

            # 2. Reset Initial Value to "0" (or appropriate default)
            row = index.row()
            init_val_col = 2 # Initial Value is column 2
            init_val_item = self.tag_table.table.item(row, init_val_col)
            old_init_val = init_val_item.text() if init_val_item else "0"
            
            # Reset to "0" when type changes to prevent type mismatch errors validation
            # For Date/Time types, the delegate will handle "0" by defaulting to current time on next edit
            if old_init_val != "0":
                 cmd_reset = TagChangeCommand(self.tag_table, row, init_val_col, old_init_val, "0", "Reset Initial Value")
                 self.tag_table.undo_stack.push(cmd_reset)

            self.tag_table.undo_stack.endMacro()

class TagNameDelegate(QStyledItemDelegate):
    def __init__(self, tag_table, parent=None):
        super().__init__(parent)
        self.tag_table = tag_table

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        # editor.setStyleSheet("QLineEdit { background-color: #2b2b2b; color: #dcdcdc; border: none; }")
        return editor

    def setEditorData(self, editor, index):
        editor.setText(index.model().data(index, Qt.ItemDataRole.EditRole))

    def setModelData(self, editor, model, index):
        new_name = editor.text().strip()
        old_name = index.model().data(index, Qt.ItemDataRole.EditRole)
        
        if new_name == old_name:
            return

        # Check for duplicates
        table_widget = self.tag_table.table
        for row in range(table_widget.rowCount()):
            if row == index.row(): continue
            item = table_widget.item(row, 0)
            if item and item.text().lower() == new_name.lower():
                QMessageBox.warning(table_widget, "Duplicate Name", f"The tag name '{new_name}' already exists.")
                return 

        command = TagChangeCommand(self.tag_table, index.row(), index.column(), old_name, new_name, "Rename Tag")
        self.tag_table.undo_stack.push(command)

class InitialValueDelegate(QStyledItemDelegate):
    """Delegate for Initial Value with validation based on Data Type."""
    def __init__(self, tag_table, parent=None):
        super().__init__(parent)
        self.tag_table = tag_table

    def createEditor(self, parent, option, index):
        # Determine Data Type
        row = index.row()
        type_item = self.tag_table.table.item(row, 1)
        data_type = type_item.text() if type_item else "Bit"

        style = """
            background-color: #2b2b2b; 
            color: #dcdcdc; 
            border: none;
        """
        
        # Specific editors for Time/Date types
        if data_type == "Date":
            editor = QDateEdit(parent)
            editor.setDisplayFormat("yyyy-MM-dd")
            editor.setCalendarPopup(True)
            # editor.setStyleSheet(style)
            return editor
        elif data_type == "Time":
            editor = QTimeEdit(parent)
            editor.setDisplayFormat("HH:mm:ss")
            # editor.setStyleSheet(style)
            return editor
        elif data_type == "Date Time":
            editor = QDateTimeEdit(parent)
            editor.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
            editor.setCalendarPopup(True)
            # editor.setStyleSheet(style)
            return editor

        # Default editor for other types
        editor = QLineEdit(parent)
        # editor.setStyleSheet(f"QLineEdit {{ {style} }}")
        return editor

    def setEditorData(self, editor, index):
        value_str = str(index.model().data(index, Qt.ItemDataRole.EditRole))
        
        if isinstance(editor, QDateEdit):
            qdate = QDate.fromString(value_str, "yyyy-MM-dd")
            if not qdate.isValid():
                qdate = QDate.currentDate()
            editor.setDate(qdate)
        elif isinstance(editor, QTimeEdit):
            qtime = QTime.fromString(value_str, "HH:mm:ss")
            if not qtime.isValid():
                qtime = QTime.currentTime()
            editor.setTime(qtime)
        elif isinstance(editor, QDateTimeEdit):
            qdt = QDateTime.fromString(value_str, "yyyy-MM-dd HH:mm:ss")
            if not qdt.isValid():
                qdt = QDateTime.currentDateTime()
            editor.setDateTime(qdt)
        elif isinstance(editor, QLineEdit):
            editor.setText(value_str)

    def setModelData(self, editor, model, index):
        old_val_str = str(index.model().data(index, Qt.ItemDataRole.EditRole))
        new_val_str = ""

        # Extract value based on editor type
        if isinstance(editor, QDateEdit):
            new_val_str = editor.date().toString("yyyy-MM-dd")
        elif isinstance(editor, QTimeEdit):
            new_val_str = editor.time().toString("HH:mm:ss")
        elif isinstance(editor, QDateTimeEdit):
            new_val_str = editor.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        elif isinstance(editor, QLineEdit):
            new_val_str = editor.text().strip()

            # Perform numeric validation only for QLineEdit based types
            row = index.row()
            type_item = self.tag_table.table.item(row, 1)
            data_type = type_item.text() if type_item else "Bit"
            
            is_valid = True
            error_msg = ""

            if data_type in DATA_TYPE_RANGES:
                min_val, max_val = DATA_TYPE_RANGES[data_type]
                try:
                    val = int(new_val_str)
                    if not (min_val <= val <= max_val):
                        is_valid = False
                        error_msg = f"Value must be between {min_val} and {max_val}."
                except ValueError:
                    is_valid = False
                    error_msg = f"Invalid integer format for {data_type}."
            elif data_type == "Real":
                try:
                    float(new_val_str)
                except ValueError:
                    is_valid = False
                    error_msg = "Invalid float format."

            if not is_valid:
                QMessageBox.warning(self.tag_table, "Invalid Value", error_msg)
                return # Reject change

        if new_val_str != old_val_str:
            command = TagChangeCommand(self.tag_table, index.row(), index.column(), old_val_str, new_val_str, "Edit Initial Value")
            self.tag_table.undo_stack.push(command)

class GenericDelegate(QStyledItemDelegate):
    """Generic delegate for other columns to handle Undo/Redo."""
    def __init__(self, tag_table, parent=None):
        super().__init__(parent)
        self.tag_table = tag_table
        
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        # editor.setStyleSheet("QLineEdit { background-color: #2b2b2b; color: #dcdcdc; border: none; }")
        return editor

    def setEditorData(self, editor, index):
        editor.setText(str(index.model().data(index, Qt.ItemDataRole.EditRole)))

    def setModelData(self, editor, model, index):
        new_val = editor.text()
        old_val = str(index.model().data(index, Qt.ItemDataRole.EditRole))
        
        if new_val != old_val:
            command = TagChangeCommand(self.tag_table, index.row(), index.column(), old_val, new_val, "Edit Cell")
            self.tag_table.undo_stack.push(command)

# --- Custom Table Widget ---

class SingleClickTableWidget(QTableWidget):
    """A QTableWidget that starts editing on a single click for specific columns."""
    def mousePressEvent(self, event):
        # First, let the standard behavior handle selection
        super().mousePressEvent(event)
        
        # Now check if we clicked on a valid item
        index = self.indexAt(event.position().toPoint())
        if index.isValid():
            # If it's the Data Type column (Column 1), start editing immediately
            if index.column() == 1:
                self.edit(index)

# --- Main Widget ---

class TagTable(QWidget):
    def __init__(self, tag_data, main_window, parent=None):
        super().__init__(parent)
        self.tag_data = tag_data
        self.main_window = main_window
        self.undo_stack = QUndoStack(self)
        
        if 'tags' not in self.tag_data:
            self.tag_data['tags'] = []

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Toolbar ---
        self.toolbar = QToolBar("Tag Toolbar")
        self.toolbar.setIconSize(self.main_window.iconSize())
        # Dark theme toolbar style
        # self.toolbar.setStyleSheet("""
        #     QToolBar {
        #         background: #3c3f41;
        #         border-bottom: 1px solid #555555;
        #         spacing: 5px; 
        #         padding: 5px;
        #     }
        #     QToolButton {
        #         background: transparent;
        #         border: 1px solid transparent;
        #         border-radius: 4px;
        #         padding: 4px;
        #         color: #dcdcdc;
        #     }
        #     QToolButton:hover {
        #         background-color: #4e5254;
        #         border: 1px solid #666666;
        #     }
        #     QToolButton:pressed {
        #         background-color: #2b2b2b;
        #     }
        # """)
        
        self.add_action = QAction(IconService.get_icon('common-add-row'), "Add Tag", self)
        self.add_action.triggered.connect(self.add_tag)
        self.toolbar.addAction(self.add_action)

        self.remove_action = QAction(IconService.get_icon('common-remove-row'), "Remove Tag", self)
        self.remove_action.triggered.connect(self.remove_tag)
        self.toolbar.addAction(self.remove_action)
        
        # Spacer
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(empty)

        layout.addWidget(self.toolbar)

        # --- Table Widget ---
        # Use the custom SingleClickTableWidget
        self.table = SingleClickTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Tag Name", "Data Type", "Initial Value", 
            "Array Elements", "Constant", "Comment"
        ])
        
        # Install Delegates for Undo/Redo support
        self.table.setItemDelegateForColumn(0, TagNameDelegate(self, self.table))
        self.table.setItemDelegateForColumn(1, DataTypeDelegate(self, self.table))
        self.table.setItemDelegateForColumn(2, InitialValueDelegate(self, self.table)) # Use validating delegate
        self.table.setItemDelegateForColumn(3, GenericDelegate(self, self.table))
        self.table.setItemDelegateForColumn(5, GenericDelegate(self, self.table))
        
        header = self.table.horizontalHeader()
        
        # Column Sizing
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 120)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 140) # Increased for DateTime
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 100)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 70)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.setShowGrid(True)
        
        # Dark Theme Table Stylesheet
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                alternate-background-color: #323232;
                gridline-color: #3c3f41;
                selection-background-color: #0078d7;
                selection-color: #ffffff;
                border: none;
                font-size: 12px;
                color: #dcdcdc;
            }
            QHeaderView::section {
                background-color: #3c3f41;
                color: #dcdcdc;
                padding: 6px 4px;
                border: 1px solid #555555;
                border-left: none;
                font-weight: 600;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:focus {
                border: none; 
                outline: none;
            }
            QScrollBar:vertical {
                background: #2b2b2b;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            QCheckBox { 
                margin-left: 25px; 
            }
            /* Calendar Widget Styling for Date/DateTime Edits */
            QCalendarWidget QWidget {
                background-color: #2b2b2b;
                color: #dcdcdc;
            }
            QCalendarWidget QToolButton {
                color: #dcdcdc;
            }
            QCalendarWidget QMenu {
                background-color: #3c3f41;
                color: #dcdcdc;
            }
        """)
        
        # Connect signals
        self.table.itemChanged.connect(self.on_item_changed)
        
        layout.addWidget(self.table)

    def block_signals(self, block):
        self.table.blockSignals(block)

    def load_data(self):
        self.block_signals(True)
        self.table.setRowCount(0)
        tags = self.tag_data.get('tags', [])
        for tag in tags:
            self._insert_row_visual(self.table.rowCount(), tag)
        self.block_signals(False)

    def _insert_row_visual(self, row, tag_dict):
        self.table.insertRow(row)
        
        # Helper to create items
        def create_item(text):
            item = QTableWidgetItem(str(text))
            return item

        # 0: Name
        self.table.setItem(row, 0, create_item(tag_dict.get('name', f'Tag_{row}')))
        # 1: Type
        self.table.setItem(row, 1, create_item(tag_dict.get('type', 'Bit')))
        # 2: Initial Value
        self.table.setItem(row, 2, create_item(tag_dict.get('initial_value', '0')))
        # 3: Array Elements
        self.table.setItem(row, 3, create_item(tag_dict.get('array_elements', '1')))
        
        # 4: Constant (Checkbox)
        const_item = QTableWidgetItem()
        const_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        const_item.setCheckState(Qt.CheckState.Checked if tag_dict.get('constant', False) else Qt.CheckState.Unchecked)
        self.table.setItem(row, 4, const_item)
        
        # 5: Comment
        self.table.setItem(row, 5, create_item(tag_dict.get('comment', '')))

    def _get_row_data(self, row):
        """Extracts data dict from a row."""
        name_item = self.table.item(row, 0)
        type_item = self.table.item(row, 1)
        init_item = self.table.item(row, 2)
        array_item = self.table.item(row, 3)
        const_item = self.table.item(row, 4)
        comment_item = self.table.item(row, 5)

        return {
            'name': name_item.text() if name_item else "",
            'type': type_item.text() if type_item else "Bit",
            'initial_value': init_item.text() if init_item else "0",
            'array_elements': array_item.text() if array_item else "1",
            'constant': const_item.checkState() == Qt.CheckState.Checked if const_item else False,
            'comment': comment_item.text() if comment_item else ""
        }

    def _set_cell_value(self, row, col, value):
        item = self.table.item(row, col)
        if not item:
            item = QTableWidgetItem()
            self.table.setItem(row, col, item)
        
        if col == 4: # Checkbox
            item.setCheckState(Qt.CheckState.Checked if value else Qt.CheckState.Unchecked)
        else:
            item.setText(str(value))

    def on_item_changed(self, item):
        """Handles changes. For checkboxes, we must manually push commands as delegates don't cover them."""
        if self.table.signalsBlocked(): return

        row, col = item.row(), item.column()
        
        # Handle Checkbox (Column 4) specifically
        if col == 4:
            self.save_data()
        else:
            self.save_data()

    def add_tag(self):
        row = self.table.rowCount()
        
        # Generate unique name
        base_name = "Tag"
        count = 1
        new_name = f"{base_name}_{count}"
        existing_names = [self.table.item(r, 0).text() for r in range(row)]
        while new_name in existing_names:
            count += 1
            new_name = f"{base_name}_{count}"

        new_tag = {
            'name': new_name,
            'type': 'Bit',
            'initial_value': '0',
            'array_elements': '1',
            'constant': False,
            'comment': ''
        }
        
        command = TagAddCommand(self, row, new_tag)
        self.undo_stack.push(command)

    def remove_tag(self):
        # Get selected rows. Handle individual cell selections by mapping to rows.
        rows = sorted(list(set(index.row() for index in self.table.selectedIndexes())), reverse=True)
        
        # If no specific selection, try current row
        if not rows and self.table.currentRow() != -1:
            rows = [self.table.currentRow()]

        if not rows:
            return

        # Collect data for undo
        rows_data = []
        for r in rows:
            rows_data.append((r, self._get_row_data(r)))

        command = TagRemoveCommand(self, rows_data)
        self.undo_stack.push(command)
        
    def delete(self):
        """Public method for MainWindow to call (Edit -> Delete)."""
        self.remove_tag()

    def undo(self):
        self.undo_stack.undo()

    def redo(self):
        self.undo_stack.redo()

    def copy(self):
        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes: return
        
        # Organize by row
        rows_dict = {}
        for idx in selected_indexes:
            r, c = idx.row(), idx.column()
            if r not in rows_dict: rows_dict[r] = {}
            rows_dict[r][c] = idx
            
        text_rows = []
        sorted_rows = sorted(rows_dict.keys())
        
        for r in sorted_rows:
            # Get min/max col to ensure formatting
            cols = sorted(rows_dict[r].keys())
            row_text = []
            for c in cols:
                item = self.table.item(r, c)
                if c == 4: # Checkbox
                    row_text.append("1" if item.checkState() == Qt.CheckState.Checked else "0")
                else:
                    row_text.append(item.text())
            text_rows.append("\t".join(row_text))
            
        QApplication.clipboard().setText("\n".join(text_rows))

    def cut(self):
        self.copy()
        self.delete()

    def paste(self):
        text = QApplication.clipboard().text()
        if not text: return
        
        rows = text.strip().split('\n')
        if not rows: return

        self.undo_stack.beginMacro("Paste Tags")
        
        for row_text in rows:
            cols = row_text.split('\t')
            if not cols: continue
            
            # Ensure unique name
            name = cols[0] if len(cols) > 0 else "NewTag"
            existing = [self.table.item(r, 0).text() for r in range(self.table.rowCount())]
            if name in existing:
                name += "_Copy"
                
            new_tag = {
                'name': name,
                'type': cols[1] if len(cols) > 1 else 'Bit',
                'initial_value': cols[2] if len(cols) > 2 else '0',
                'array_elements': cols[3] if len(cols) > 3 else '1',
                'constant': (cols[4] == '1' or cols[4].lower() == 'true') if len(cols) > 4 else False,
                'comment': cols[5] if len(cols) > 5 else ''
            }
            
            cmd = TagAddCommand(self, self.table.rowCount(), new_tag)
            self.undo_stack.push(cmd)
            
        self.undo_stack.endMacro()

    def save_data(self):
        """Syncs the table contents back to the persistent storage."""
        tags = []
        for row in range(self.table.rowCount()):
            tags.append(self._get_row_data(row))
        
        # Update local data structure
        self.tag_data['tags'] = tags
        
        # Update the ProjectService data structure
        if hasattr(self.main_window, 'project_service'):
            tag_number = str(self.tag_data.get('number'))
            if tag_number:
                if 'tag_lists' not in self.main_window.project_service.project_data:
                    self.main_window.project_service.project_data['tag_lists'] = {}
                
                self.main_window.project_service.project_data['tag_lists'][tag_number] = self.tag_data
                self.main_window.project_service.mark_as_unsaved()