# project/comment/optimized_operations.py
"""
Optimized batch operations for comment table
Prevents freeze when handling 10,000+ rows
"""

import threading
from typing import List, Callable
from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QApplication


class AsyncOperationThread(QThread):
    """Thread for async operations to prevent UI freeze."""
    
    progress = Signal(int, int)  # current, total
    finished = Signal()
    error = Signal(str)
    
    def __init__(self, operation: Callable, batch_size: int = 100):
        super().__init__()
        self.operation = operation
        self.batch_size = batch_size
        self._should_stop = False
    
    def run(self):
        """Execute operation in background."""
        try:
            self.operation(self._on_progress)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
    
    def _on_progress(self, current: int, total: int):
        """Report progress."""
        self.progress.emit(current, total)
    
    def stop(self):
        """Stop operation."""
        self._should_stop = True


class OptimizedBatchDelete:
    """
    Optimized deletion of large numbers of rows/columns.
    Handles 10,000+ rows without freezing.
    """
    
    @staticmethod
    def delete_multiple_rows_optimized(spreadsheet, rows: List[int], show_progress=True):
        """
        Efficiently delete multiple rows with chunked processing.
        
        Args:
            spreadsheet: The Spreadsheet widget
            rows: List of row indices to delete
            show_progress: Whether to show progress dialog
        """
        if not rows:
            return
        
        total_rows = len(rows)
        
        # For small batches, use original method
        if total_rows < 100:
            spreadsheet.set_updates_deferred(True)
            try:
                for row in sorted(rows, reverse=True):
                    if row < spreadsheet.rowCount():
                        spreadsheet.removeRow(row)
            finally:
                spreadsheet.set_updates_deferred(False)
            return
        
        # For large batches, use chunked approach
        progress = None
        if show_progress and total_rows > 1000:
            progress = QProgressDialog(
                f"Deleting {total_rows} rows...",
                "Cancel",
                0,
                total_rows,
                spreadsheet
            )
            progress.setWindowTitle("Deleting Rows")
            # REMOVED: Stylesheet now handled by global stylesheet.qss
        
        spreadsheet.set_updates_deferred(True)
        try:
            sorted_rows = sorted(rows, reverse=True)
            
            for idx, row in enumerate(sorted_rows):
                if row < spreadsheet.rowCount():
                    spreadsheet.removeRow(row)
                
                # Update progress every 100 rows
                if progress and idx % 100 == 0:
                    progress.setValue(idx)
                    QApplication.processEvents()
                    
                    if progress.wasCanceled():
                        break
            
            if progress:
                progress.setValue(total_rows)
                progress.close()
        
        finally:
            spreadsheet.set_updates_deferred(False)
    
    @staticmethod
    def delete_multiple_columns_optimized(spreadsheet, cols: List[int], show_progress=True):
        """
        Efficiently delete multiple columns with chunked processing.
        
        Args:
            spreadsheet: The Spreadsheet widget
            cols: List of column indices to delete
            show_progress: Whether to show progress dialog
        """
        if not cols:
            return
        
        total_cols = len(cols)
        
        # For small batches, use original method
        if total_cols < 5:
            spreadsheet.set_updates_deferred(True)
            try:
                for col in sorted(cols, reverse=True):
                    if col < spreadsheet.columnCount():
                        spreadsheet.removeColumn(col)
            finally:
                spreadsheet.set_updates_deferred(False)
            return
        
        progress = None
        if show_progress and total_cols > 10:
            progress = QProgressDialog(
                f"Deleting {total_cols} columns...",
                "Cancel",
                0,
                total_cols,
                spreadsheet
            )
            progress.setWindowTitle("Deleting Columns")
        
        spreadsheet.set_updates_deferred(True)
        try:
            sorted_cols = sorted(cols, reverse=True)
            
            for idx, col in enumerate(sorted_cols):
                if col < spreadsheet.columnCount():
                    spreadsheet.removeColumn(col)
                
                if progress and idx % 5 == 0:
                    progress.setValue(idx)
                    QApplication.processEvents()
                    
                    if progress.wasCanceled():
                        break
            
            if progress:
                progress.setValue(total_cols)
                progress.close()
        
        finally:
            spreadsheet.set_updates_deferred(False)
    
    @staticmethod
    def delete_all_cells_optimized(spreadsheet, show_progress=True):
        """
        Efficiently delete all cells in a large table.
        Handles tables with 10,000+ rows without freezing.
        
        Args:
            spreadsheet: The Spreadsheet widget
            show_progress: Whether to show progress dialog
        """
        row_count = spreadsheet.rowCount()
        col_count = spreadsheet.columnCount()
        total_cells = row_count * col_count
        
        if total_cells == 0:
            return
        
        # Confirm operation
        reply = QMessageBox.question(
            spreadsheet,
            "Delete All Cells",
            f"Delete all {total_cells:,} cells? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        progress = None
        if show_progress and total_cells > 10000:
            progress = QProgressDialog(
                f"Deleting {total_cells:,} cells...",
                "Cancel",
                0,
                row_count,
                spreadsheet
            )
            progress.setWindowTitle("Clearing Table")
            # REMOVED: Stylesheet now handled by global stylesheet.qss
        
        spreadsheet.set_updates_deferred(True)
        try:
            # Process in chunks to keep UI responsive
            for row in range(row_count):
                for col in range(col_count):
                    item = spreadsheet.item(row, col)
                    if item:
                        if hasattr(item, 'set_data'):
                            item.set_data({'value': ''})
                        else:
                            item.setText('')
                
                # Update progress and process events
                if progress and row % 50 == 0:
                    progress.setValue(row)
                    QApplication.processEvents()
                    
                    if progress.wasCanceled():
                        break
            
            if progress:
                progress.setValue(row_count)
                progress.close()
        
        finally:
            spreadsheet.set_updates_deferred(False)


class OptimizedColumnAddition:
    """
    Optimized column addition.
    Handles adding columns to tables with 10,000+ rows efficiently.
    """
    
    @staticmethod
    def add_columns_optimized(spreadsheet, index: int, count: int, show_progress=True):
        """
        Add multiple columns efficiently.
        
        Args:
            spreadsheet: The Spreadsheet widget
            index: Column index to insert at
            count: Number of columns to add
            show_progress: Whether to show progress
        """
        if count <= 0:
            return
        
        # Check limits
        if spreadsheet.columnCount() + count > 30:
            QMessageBox.warning(spreadsheet, "Limit", "Max 30 columns allowed.")
            return
        
        row_count = spreadsheet.rowCount()
        total_ops = count * row_count
        
        progress = None
        if show_progress and total_ops > 1000:
            progress = QProgressDialog(
                f"Adding {count} columns...",
                "Cancel",
                0,
                count,
                spreadsheet
            )
            progress.setWindowTitle("Adding Columns")
        
        spreadsheet.set_updates_deferred(True)
        try:
            for col_idx in range(count):
                spreadsheet.insertColumn(index + col_idx)
                
                if progress:
                    progress.setValue(col_idx + 1)
                    QApplication.processEvents()
                    
                    if progress.wasCanceled():
                        break
            
            if progress:
                progress.close()
        
        finally:
            spreadsheet.set_updates_deferred(False)
