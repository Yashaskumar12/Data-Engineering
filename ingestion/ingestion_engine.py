"""
CSV to DuckDB ingestion engine for Olist ERP Analytics.
"""
import duckdb
import pandas as pd
from typing import Dict, Optional, Any
from pathlib import Path

from config import DuckDBConfig
from logger import IngestionLogger


class CSVIngestionEngine:
    """Engine for loading CSV files into local DuckDB database."""
    
    def __init__(self, config: DuckDBConfig, logger: Optional[IngestionLogger] = None):
        """
        Initialize the ingestion engine.
        
        Args:
            config: DuckDB configuration object
            logger: Optional logger instance
        """
        self.config = config
        self.logger = logger or IngestionLogger()
        self.connection = None
    
    def connect(self) -> duckdb.DuckDBPyConnection:
        """
        Establish connection to local DuckDB file.
        """
        try:
            self.logger.logger.info(f"Connecting to DuckDB at {self.config.db_path}...")
            
            # Connect to local file (creates it if doesn't exist)
            self.connection = duckdb.connect(str(self.config.db_path))
            
            # Install and load spatial extension if needed (good for geolocation)
            # self.connection.execute("INSTALL spatial; LOAD spatial;")
            
            self.logger.logger.info("Successfully connected to DuckDB")
            return self.connection
            
        except Exception as e:
            self.logger.logger.error(f"Connection failed: {str(e)}")
            raise
    
    def close(self) -> None:
        """Close DuckDB connection."""
        if self.connection:
            self.connection.close()
            self.logger.logger.info("DuckDB connection closed")
    
    def create_table_from_csv(self, csv_path: str, table_name: str) -> int:
        """
        Load CSV file into DuckDB table using native read_csv_auto.
        
        Args:
            csv_path: Path to CSV file
            table_name: Name of target table
            
        Returns:
            Number of rows loaded
        """
        csv_file = Path(csv_path)
        
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        self.logger.log_start(csv_file.name)
        
        try:
            # DuckDB's read_csv_auto is extremely efficient
            # We use CREATE OR REPLACE TABLE ... AS SELECT ...
            query = f"""
                CREATE OR REPLACE TABLE {table_name} AS 
                SELECT * FROM read_csv_auto(
                    '{str(csv_file.absolute())}', 
                    normalize_names=True,
                    ignore_errors=True
                )
            """
            
            self.logger.logger.info(f"Loading {csv_file.name} into {table_name}...")
            self.connection.execute(query)
            
            # Get row count
            count_result = self.connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
            loaded_rows = count_result[0] if count_result else 0
            
            self.logger.log_success(csv_file.name, loaded_rows)
            return loaded_rows
            
        except Exception as e:
            self.logger.log_error(csv_file.name, e)
            raise

    def load_all_files(self, file_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Load multiple CSV files into DuckDB.
        
        Args:
            file_mapping: Dictionary mapping CSV file paths to table names
        
        Returns:
            Dictionary with results for each file
        """
        results = {}
        
        for csv_path, table_name in file_mapping.items():
            file_name = Path(csv_path).name
            
            try:
                rows = self.create_table_from_csv(csv_path, table_name)
                results[file_name] = {
                    'status': 'success',
                    'rows': rows,
                    'table': table_name
                }
            except Exception as e:
                results[file_name] = {
                    'status': 'failed',
                    'rows': 0,
                    'error': str(e)
                }
                continue
        
        return results
