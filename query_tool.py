"""
Interactive query tool for Olist DuckDB database.
"""
import duckdb
import pandas as pd
from pathlib import Path

def main():
    print("=" * 80)
    print("OLIST DATA QUERY TOOL")
    print("=" * 80)
    print()
    
    # Check if database exists
    db_path = Path("olist_erp.duckdb")
    if not db_path.exists():
        print("❌ Database not found. Run the ingestion script first.")
        print("   Run: python ingestion/main.py")
        return
    
    # Connect to DuckDB
    conn = duckdb.connect(str(db_path))
    
    print("✅ Connected to database")
    print()
    
    # Show available tables
    tables = conn.execute("SHOW TABLES").fetchall()
    print(f"Available tables ({len(tables)}):")
    for i, (table_name,) in enumerate(tables, 1):
        count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"  {i}. {table_name} ({count:,} rows)")
    
    print()
    print("=" * 80)
    print("QUERY EXAMPLES:")
    print("=" * 80)
    print()
    print("1. Top 10 products by price:")
    print("   SELECT product_id, product_category_name FROM bronze_products LIMIT 10")
    print()
    print("2. Order status distribution:")
    print("   SELECT order_status, COUNT(*) as count FROM bronze_orders GROUP BY order_status ORDER BY count DESC")
    print()
    print("3. Seller performance:")
    print("   SELECT seller_id, COUNT(*) as order_count FROM bronze_order_items GROUP BY seller_id ORDER BY order_count DESC LIMIT 10")
    print()
    print("4. Customer orders:")
    print("   SELECT customer_id, COUNT(*) as order_count FROM bronze_orders GROUP BY customer_id ORDER BY order_count DESC LIMIT 10")
    print()
    
    while True:
        print("=" * 80)
        print("Enter your SQL query (or 'exit' to quit):")
        print("=" * 80)
        
        query = input("\nSQL> ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if not query:
            continue
        
        try:
            # Execute query
            result = conn.execute(query).fetchdf()
            
            if result.empty:
                print("✅ Query executed successfully (0 rows returned)")
            else:
                print(f"\n✅ Result ({len(result)} rows):")
                print("-" * 80)
                print(result.to_string())
                print("-" * 80)
                
                # Show basic stats
                print(f"\n📊 Summary: {len(result)} rows, {len(result.columns)} columns")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    main()