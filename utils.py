"""Utility functions for the Photo Auto-Categorizer."""

import os
from pathlib import Path
from typing import Set
import logging

from config import SUPPORTED_EXTENSIONS


def is_valid_image_file(file_path: Path) -> bool:
    """Check if a file has a supported image extension.
    
    Args:
        file_path: Path to the file to check.
        
    Returns:
        True if the file has a supported image extension, False otherwise.
    """
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def validate_input_directory(input_dir: Path) -> bool:
    """Validate that the input directory exists and is readable.
    
    Args:
        input_dir: Path to the input directory.
        
    Returns:
        True if the directory is valid, False otherwise.
    """
    if not input_dir.exists():
        return False
    if not input_dir.is_dir():
        return False
    if not os.access(input_dir, os.R_OK):
        return False
    return True


def validate_output_directory(output_dir: Path) -> bool:
    """Validate that the output directory can be created or is writable.
    
    Args:
        output_dir: Path to the output directory.
        
    Returns:
        True if the directory is valid or can be created, False otherwise.
    """
    if output_dir.exists():
        return output_dir.is_dir() and os.access(output_dir, os.W_OK)
    # Check if parent directory exists and is writable
    parent = output_dir.parent
    return parent.exists() and os.access(parent, os.W_OK)


def get_image_files(input_dir: Path) -> Set[Path]:
    """Recursively find all image files in the input directory.
    
    Args:
        input_dir: Path to the input directory to scan.
        
    Returns:
        Set of Path objects pointing to image files.
    """
    image_files = set()
    logger = logging.getLogger(__name__)
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = Path(root) / file
            if is_valid_image_file(file_path):
                image_files.add(file_path)
                logger.debug(f"Found image file: {file_path}")
    
    return image_files


def setup_logging(log_level: str, output_dir: Path) -> logging.Logger:
    """Configure logging to both console and file.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR).
        output_dir: Directory where log file will be created.
        
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger('photo_categorizer')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = output_dir / 'categorizer.log'
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)  # Always log DEBUG to file
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
