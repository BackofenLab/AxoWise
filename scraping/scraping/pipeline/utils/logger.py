"""
Logging utilities for the research data extraction pipeline.
"""

import os
import logging
from datetime import datetime
from pathlib import Path


def get_logger(name, level=logging.INFO, log_dir=None):
    """
    Get a logger instance.
    
    Args:
        name (str): Logger name.
        level (int, optional): Logging level. Defaults to logging.INFO.
        log_dir (str, optional): Directory to store log files. Defaults to None.
        
    Returns:
        logging.Logger: Logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # Add file handler if log_dir is provided
    if log_dir:
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        
        # Create file handler
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        
        # Add file handler to logger
        logger.addHandler(file_handler)
    
    return logger