import logging
import os
import sys

def setup_logger(name: str, log_filename: str, level=logging.INFO) -> logging.Logger:
    """
    Sets up a logger that outputs to the specified log_filename inside the 'logs' directory
    at the root of the project.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    log_dir = os.path.join(project_root, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, log_filename)
    
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    
    # File handler
    file_handler = logging.FileHandler(log_file)        
    file_handler.setFormatter(formatter)
    
    # Stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
