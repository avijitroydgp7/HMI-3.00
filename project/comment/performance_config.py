# project\comment\performance_config.py
"""
Performance configuration and utilities for the comment table system.
Centralized settings for optimization behavior.
"""

# Global configuration constants
MAX_COLUMNS = 30
MAX_ROWS = 1000000

class PerformanceConfig:
    """
    Configuration for performance optimizations.
    Adjust these values based on your hardware and datasets.
    """
    
    # Batch Operation Settings
    # ========================
    
    # Number of rows to process before showing progress
    BATCH_SIZE_FOR_PROGRESS = 1000
    
    # Chunk size for batch deletions (process 100 rows at a time)
    DELETE_BATCH_CHUNK_SIZE = 100
    
    # Chunk size for batch insertions
    INSERT_BATCH_CHUNK_SIZE = 10
    
    # Minimum number of rows to trigger optimization
    LARGE_OPERATION_THRESHOLD = 100
    
    # Minimum rows for showing progress dialog
    MIN_ROWS_FOR_PROGRESS = 1000
    
    # Progress update interval (every N operations)
    PROGRESS_UPDATE_INTERVAL = 100
    
    
    # UI Settings
    # ===========
    
    # Show progress dialog for operations
    SHOW_PROGRESS_DIALOGS = True
    
    # Allow user to cancel long operations
    ALLOW_OPERATION_CANCELLATION = True
    
    # Deferred update batching
    USE_DEFERRED_UPDATES = True
    
    
    # Memory Settings
    # ===============
    
    # Use virtual rendering (VirtualSpreadsheet) for large tables
    ENABLE_VIRTUAL_RENDERING = False  # Set True for 100,000+ rows
    
    # Pre-render buffer (extra rows/cols beyond viewport)
    VIEWPORT_BUFFER_ROWS = 20
    VIEWPORT_BUFFER_COLS = 5
    
    # Maximum cached rows in memory
    MAX_CACHED_ROWS = 1000
    
    
    # Formula Evaluation Settings
    # ==========================
    
    # Evaluate formulas in background thread
    BACKGROUND_FORMULA_EVALUATION = True
    
    # Defer formula evaluation during bulk operations
    DEFER_FORMULA_EVALUATION = True
    
    # Batch size for formula evaluation
    FORMULA_EVAL_BATCH_SIZE = 100
    
    
    # Data Persistence Settings
    # ==========================
    
    # Delay before saving after operations (milliseconds)
    AUTO_SAVE_DELAY_MS = 2000
    
    # Batch saves to reduce I/O
    BATCH_SAVES = True
    
    # Maximum rows to save per batch
    SAVE_BATCH_SIZE = 500
    
    
    # Virtual Spreadsheet Settings
    # ============================
    
    # Cell dimensions (pixels)
    CELL_WIDTH = 100
    CELL_HEIGHT = 24
    HEADER_HEIGHT = 24
    HEADER_WIDTH = 50
    
    # Initial grid size
    INITIAL_ROWS = 100
    INITIAL_COLS = 10
    
    # Lazy load data
    LAZY_LOAD_ENABLED = True
    
    
    # Table Limits
    # ============
    
    # Maximum rows allowed
    MAX_ROWS = 1000000
    
    # Maximum columns allowed  
    MAX_COLUMNS = 30
    
    # Maximum cells per operation
    MAX_CELLS_PER_OP = 100000
    
    
    # Advanced Settings
    # =================
    
    # Thread pool size for background operations
    BACKGROUND_THREAD_POOL_SIZE = 2
    
    # Enable detailed logging
    ENABLE_PERFORMANCE_LOGGING = False
    
    # Profile operations (may impact performance slightly)
    ENABLE_PROFILING = False
    
    
    @classmethod
    def get_optimization_strategy(cls, row_count: int, col_count: int, operation_type: str) -> dict:
        """
        Determine optimization strategy based on table size and operation.
        
        Args:
            row_count: Current number of rows
            col_count: Current number of columns
            operation_type: 'delete_rows', 'add_columns', 'paste', etc.
        
        Returns:
            Dictionary with optimization settings
        """
        total_cells = row_count * col_count
        
        strategy = {
            'use_background_thread': False,
            'show_progress': False,
            'batch_size': cls.DELETE_BATCH_CHUNK_SIZE,
            'use_deferred': False,
            'chunk_operations': False,
        }
        
        # Determine if background processing needed
        if operation_type == 'delete_rows':
            if row_count > 10000:
                strategy['use_background_thread'] = True
                strategy['show_progress'] = True
                strategy['use_deferred'] = True
                strategy['chunk_operations'] = True
            elif row_count > 1000:
                strategy['show_progress'] = True
                strategy['use_deferred'] = True
                strategy['chunk_operations'] = True
        
        # Column operations
        elif operation_type == 'add_columns':
            if row_count > 10000:
                strategy['show_progress'] = True
                strategy['use_deferred'] = True
            elif row_count > 5000:
                strategy['use_deferred'] = True
        
        # Paste operations
        elif operation_type == 'paste':
            if total_cells > 100000:
                strategy['use_background_thread'] = True
                strategy['show_progress'] = True
                strategy['use_deferred'] = True
        
        # Formula evaluation
        elif operation_type == 'evaluate_formulas':
            if row_count > 5000:
                strategy['use_background_thread'] = True
        
        return strategy
    
    @classmethod
    def should_use_virtual_spreadsheet(cls, row_count: int, col_count: int) -> bool:
        """
        Determine if VirtualSpreadsheet should be used instead of QTableWidget.
        
        Returns True if table is very large.
        """
        if cls.ENABLE_VIRTUAL_RENDERING:
            return row_count > 50000
        return False
    
    @classmethod
    def get_chunk_size(cls, operation_type: str) -> int:
        """Get appropriate chunk size for operation."""
        if operation_type == 'delete':
            return cls.DELETE_BATCH_CHUNK_SIZE
        elif operation_type == 'insert':
            return cls.INSERT_BATCH_CHUNK_SIZE
        elif operation_type == 'evaluate':
            return cls.FORMULA_EVAL_BATCH_SIZE
        elif operation_type == 'save':
            return cls.SAVE_BATCH_SIZE
        return 100


class PerformanceMonitor:
    """Monitor and log performance metrics."""
    
    def __init__(self):
        self.operations = {}
        self.enabled = PerformanceConfig.ENABLE_PERFORMANCE_LOGGING
    
    def start_operation(self, operation_name: str):
        """Mark operation start."""
        if self.enabled:
            import time
            self.operations[operation_name] = {
                'start': time.time(),
                'elapsed': 0
            }
    
    def end_operation(self, operation_name: str):
        """Mark operation end and log result."""
        if self.enabled and operation_name in self.operations:
            import time
            end_time = time.time()
            start_time = self.operations[operation_name]['start']
            elapsed = end_time - start_time
            self.operations[operation_name]['elapsed'] = elapsed
            
            print(f"[PERF] {operation_name}: {elapsed:.2f}s")
    
    def get_report(self) -> dict:
        """Get performance report."""
        return self.operations


# Global performance monitor
perf_monitor = PerformanceMonitor()


def optimize_operation(operation_name: str, row_count: int, col_count: int, operation_type: str) -> dict:
    """
    Get optimization settings for an operation.
    
    Usage:
        config = optimize_operation("delete_10000_rows", 10000, 10, "delete_rows")
        if config['show_progress']:
            # Show progress dialog
        if config['use_deferred']:
            spreadsheet.set_updates_deferred(True)
    """
    perf_monitor.start_operation(operation_name)
    return PerformanceConfig.get_optimization_strategy(row_count, col_count, operation_type)


def log_operation_complete(operation_name: str):
    """Log operation completion."""
    perf_monitor.end_operation(operation_name)
