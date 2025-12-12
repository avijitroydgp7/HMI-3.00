
import logging
import os

LOG_FILE_NAME = 'app_debug.log'

def setup_logging(debug_mode=False):
    """
    Set up logging for the application.
    
    Args:
        debug_mode (bool): If True, sets the logging level to DEBUG. 
                           Otherwise, it's set to INFO.
    """
    if os.path.exists(LOG_FILE_NAME):
        # Clear the log file on each run
        with open(LOG_FILE_NAME, 'w'):
            pass

    log_level = logging.DEBUG if debug_mode else logging.INFO
    
    logging.basicConfig(
        filename=LOG_FILE_NAME,
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # To also see logs in the console, uncomment the following lines
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(log_level)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(formatter)
    # logging.getLogger('').addHandler(console_handler)

    logging.info("Logging initialized.")

def get_logger(name):
    """
    Get a logger instance.
    
    Args:
        name (str): The name of the logger, usually __name__.
        
    Returns:
        logging.Logger: A logger instance.
    """
    return logging.getLogger(name)
