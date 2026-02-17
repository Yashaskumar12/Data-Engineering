"""
Logging utilities for Olist ERP Analytics ingestion system.
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Dict, Any


class IngestionLogger:
    """Logger class for tracking ingestion operations."""
    
    def __init__(self, log_dir: str = "logs", log_file: str = "ingestion.log"):
        """
        Initialize the ingestion logger.
        
        Args:
            log_dir: Directory to store log files
            log_file: Name of the log file
        """
        self.log_dir = log_dir
        self.log_file = log_file
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """
        Set up logger with file and console handlers.
        
        Returns:
            Configured logger instance
        """
        # Create logs directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create logger
        logger = logging.getLogger('olist_ingestion')
        logger.setLevel(logging.INFO)
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # File handler with rotation (10MB max, keep 5 backups)
        log_path = os.path.join(self.log_dir, self.log_file)
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter with timestamp
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_start(self, file_name: str) -> None:
        """
        Log the start of a file ingestion.
        
        Args:
            file_name: Name of the CSV file being processed
        """
        self.logger.info(f"Starting ingestion for file: {file_name}")
    
    def log_success(self, file_name: str, row_count: int) -> None:
        """
        Log successful file ingestion.
        
        Args:
            file_name: Name of the CSV file processed
            row_count: Number of rows loaded
        """
        self.logger.info(
            f"Successfully loaded {file_name}: {row_count:,} rows"
        )
    
    def log_error(self, file_name: str, error: Exception) -> None:
        """
        Log ingestion error with details.
        
        Args:
            file_name: Name of the CSV file that failed
            error: Exception that occurred
        """
        self.logger.error(
            f"Failed to load {file_name}: {type(error).__name__} - {str(error)}"
        )
    
    def log_summary(self, results: Dict[str, Any]) -> None:
        """
        Log summary of all ingestion operations.
        
        Args:
            results: Dictionary with ingestion results
                    Format: {file_name: {'status': 'success'|'failed', 'rows': int, 'error': str}}
        """
        self.logger.info("=" * 80)
        self.logger.info("INGESTION SUMMARY")
        self.logger.info("=" * 80)
        
        successful = []
        failed = []
        total_rows = 0
        
        for file_name, result in results.items():
            if result['status'] == 'success':
                successful.append(file_name)
                total_rows += result.get('rows', 0)
            else:
                failed.append(file_name)
        
        self.logger.info(f"Total files processed: {len(results)}")
        self.logger.info(f"Successful: {len(successful)}")
        self.logger.info(f"Failed: {len(failed)}")
        self.logger.info(f"Total rows loaded: {total_rows:,}")
        
        if successful:
            self.logger.info("\nSuccessful files:")
            for file_name in successful:
                rows = results[file_name].get('rows', 0)
                self.logger.info(f"  ✓ {file_name}: {rows:,} rows")
        
        if failed:
            self.logger.warning("\nFailed files:")
            for file_name in failed:
                error = results[file_name].get('error', 'Unknown error')
                self.logger.warning(f"  ✗ {file_name}: {error}")
        
        self.logger.info("=" * 80)
