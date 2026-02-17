"""
Main ingestion script for Olist ERP Analytics.
Downloads Olist dataset from Kaggle and loads into local DuckDB.
"""
import sys
from pathlib import Path

try:
    import kagglehub
except ImportError:
    print("Error: kagglehub not installed. Run: pip install kagglehub")
    sys.exit(1)

from config import DuckDBConfig
from logger import IngestionLogger
from ingestion_engine import CSVIngestionEngine


# File mapping: CSV filename -> DuckDB table name
# We stick to bronze_ prefix for consistency with dbt structure
FILE_MAPPING = {
    "olist_orders_dataset.csv": "bronze_orders",
    "olist_order_items_dataset.csv": "bronze_order_items",
    "olist_products_dataset.csv": "bronze_products",
    "olist_sellers_dataset.csv": "bronze_sellers",
    "olist_customers_dataset.csv": "bronze_customers",
    "olist_order_payments_dataset.csv": "bronze_order_payments",
    "olist_order_reviews_dataset.csv": "bronze_order_reviews",
    "olist_geolocation_dataset.csv": "bronze_geolocation",
    "product_category_name_translation.csv": "bronze_product_category_translation"
}


def download_dataset() -> str:
    """
    Get dataset path. Uses local path if available, otherwise would download from Kaggle.
    """
    local_path = Path(r"C:\Users\E.Gagan\Downloads\dataset")
    
    if local_path.exists():
        print(f"✓ Using local dataset at: {local_path}")
        return str(local_path)

    print("=" * 80)
    print("DOWNLOADING OLIST DATASET FROM KAGGLE")
    print("=" * 80)
    
    try:
        # Download latest version of the dataset
        path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
        print(f"\n✓ Dataset downloaded successfully!")
        print(f"Path to dataset files: {path}")
        return path
    except Exception as e:
        print(f"\n✗ Failed to download dataset: {e}")
        # Even if Kaggle fails, check if we have local files
        # Only exit if user truly needs to download
        sys.exit(1)


def build_file_paths(dataset_path: str) -> dict:
    """
    Build full file paths for CSV files.
    """
    file_paths = {}
    dataset_dir = Path(dataset_path)
    
    for csv_file, table_name in FILE_MAPPING.items():
        csv_path = dataset_dir / csv_file
        if csv_path.exists():
            file_paths[str(csv_path)] = table_name
        else:
            print(f"Warning: File not found: {csv_file}")
    
    return file_paths


def main():
    """Main execution function."""
    print("\n" + "=" * 80)
    print("OLIST ERP ANALYTICS - DATA INGESTION (DUCKDB)")
    print("=" * 80)
    print()
    
    # Initialize logger
    logger = IngestionLogger()
    
    try:
        # Step 1: Download dataset
        dataset_path = download_dataset()
        
        # Step 2: Build file paths
        print("\n" + "=" * 80)
        print("PREPARING FILE PATHS")
        print("=" * 80)
        file_paths = build_file_paths(dataset_path)
        print(f"Found {len(file_paths)} CSV files to process")
        
        # Step 3: Configure DuckDB
        print("\n" + "=" * 80)
        print("CONFIGURING LOCAL DATABASE")
        print("=" * 80)
        config = DuckDBConfig.from_env()
        print(f"✓ Using database path: {config.db_path}")
        
        # Step 4: Initialize ingestion engine
        print("\n" + "=" * 80)
        print("INITIALIZING INGESTION ENGINE")
        print("=" * 80)
        engine = CSVIngestionEngine(config, logger)
        
        # Step 5: Connect
        engine.connect()
        
        # Step 6: Load files
        print("\n" + "=" * 80)
        print("LOADING CSV FILES INTO DUCKDB")
        print("=" * 80)
        results = engine.load_all_files(file_paths)
        
        # Step 7: Log summary
        logger.log_summary(results)
        
        # Step 8: Close connection
        engine.close()
        
        # Step 9: Final Report
        failed_count = sum(1 for r in results.values() if r['status'] == 'failed')
        if failed_count > 0:
            print(f"\n⚠ Ingestion completed with {failed_count} failures")
            sys.exit(1)
        else:
            print("\n✓ All files loaded successfully!")
            print(f"\nData is now waiting in: {config.db_path}")
            sys.exit(0)
            
    except Exception as e:
        logger.logger.error(f"Unexpected error: {type(e).__name__} - {str(e)}")
        print(f"\n✗ Unexpected error: {type(e).__name__} - {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
