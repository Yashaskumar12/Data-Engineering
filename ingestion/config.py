"""
Configuration management for Olist ERP Analytics (DuckDB).
"""
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class DuckDBConfig:
    """DuckDB configuration parameters."""
    db_path: Path

    @classmethod
    def from_env(cls) -> 'DuckDBConfig':
        """Create configuration from environment variables."""
        # Default to a local olist.db file in the same directory as the script if not specified
        default_path = Path(__file__).parent / "olist.db"
        db_path_str = os.getenv("DUCKDB_PATH", str(default_path))
        
        return cls(
            db_path=Path(db_path_str)
        )
