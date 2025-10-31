"""
This is the Logger Configuration Module

Purpose: This enables debugging of potential false LLM answers by tracing data origin.
All data retrieval steps, queries, and responses are logged to enable
identification of where false information originated.
"""

#required imports
import logging
import sys
import os
from datetime import datetime
from pathlib import Path


def setup_logger(name: str) -> logging.Logger:
    """
    This function sets up the logger with console and file handlers.
    
    Console handler shows INFO level messages for user visibility.
    File handler captures DEBUG level messages for detailed debugging.
    Based on the challenge document requirements, this enables tracing the 
    origin of any false answers by logging;
    - All Wikidata SPARQL queries and responses
    - All Wikipedia API calls and responses
    - Entity extraction results
    - Data transformations
    
    Args:
        name: Logger name (typically module or class name)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Console handler - INFO level for user visibility
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)
    
    # File handler - DEBUG level for detailed debugging
    # Filename includes date for daily log rotation
    # Logs stored in 'logs' directory for proper documentation
    log_filename = logs_dir / f'bundesliga_rag_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger