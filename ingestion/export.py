
import duckdb
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.absolute()
DB_PATH = BASE_DIR / "ingestion" / "olist.db"
POWERBI_DIR = BASE_DIR / "powerbi"

def export_data():
    print(f"Connecting to database at: {DB_PATH}")
    
    if not DB_PATH.exists():
        print(f"Error: Database file not found at {DB_PATH}")
        sys.exit(1)
        
    try:
        con = duckdb.connect(str(DB_PATH))
        
        # Ensure output directory exists
        POWERBI_DIR.mkdir(exist_ok=True)
        
        tables_to_export = [
            "main_marts.dim_products",
            "main_marts.dim_customers",
            "main_marts.fct_orders"
        ]
        
        print(f"Exporting to: {POWERBI_DIR}")
        
        for table in tables_to_export:
            filename = table.split('.')[-1] + ".csv"
            output_path = POWERBI_DIR / filename
            print(f"  - Exporting {table} -> {filename}...")
            
            # Using COPY command for efficient export
            query = f"COPY (SELECT * FROM {table}) TO '{output_path}' (HEADER, DELIMITER ',')"
            con.execute(query)
            
        con.close()
        print("✅ Export completed successfully!")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    export_data()
