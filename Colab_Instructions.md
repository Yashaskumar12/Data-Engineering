
# Olist Ingestion - Google Colab Notebook

## 1. Install Dependencies
```python
!pip install duckdb pandas kagglehub
```

## 2. Ingest Data (Copy & Paste this block)
```python
import pandas as pd
import duckdb
import kagglehub
import os
from pathlib import Path

# --- A. Download Data ---
print("Downloading dataset...")
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
print(f"Dataset downloaded to: {path}")

# --- B. Load into DuckDB ---
con = duckdb.connect('olist.db')

file_mapping = {
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

dataset_dir = Path(path)

for csv_file, table_name in file_mapping.items():
    csv_path = dataset_dir / csv_file
    print(f"Loading {csv_file} -> {table_name}...")
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path}', normalize_names=True)")

print("✅ Ingestion Complete!")
```

## 3. Verify Data
```python
con.sql("SELECT * FROM bronze_orders LIMIT 5").show()
```

## 4. Export for dbt Cloud (Optional)
If you need to move this data to a warehouse dbt Cloud can access (like Snowflake or BigQuery), you would use the authenticated upload code here.
Since dbt Cloud cannot connect to your Colab notebook, **where do you want dbt Cloud to run against?**
- Snowflake?
- BigQuery?
- Databricks?

(If you just want to learn dbt syntax in dbt Cloud, you usually need a cloud data warehouse).
