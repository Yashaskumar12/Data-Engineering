
# Olist Data Engineering: Colab to Snowflake Pipeline

## Prerequisites
1.  **Snowflake Account**: You need a Snowflake account (free trial works).
2.  **Snowflake Connection Details**:
    *   Account Identifier (e.g., `xy12345.us-east-1` - check the URL or bottom-left corner).
    *   Username & Password.
    *   Database & Schema (we'll create them).

## Step 1: Install Libraries
```python
!pip install snowflake-connector-python pandas kagglehub "snowflake-connector-python[pandas]"
```

## Step 2: Configure Connection
*   In Colab, go to the "Keys" (🔑) icon on the left sidebar.
*   Add a new secret called `SNOWFLAKE_PASSWORD`.
*   Replace values below with your actual details.

```python
import snowflake.connector
from google.colab import userdata

# Configuration
ACCOUNT = 'xy12345.us-east-1'  # <--- REPLACE THIS 
USER = 'YOUR_USERNAME'         # <--- REPLACE THIS
PASSWORD = userdata.get('SNOWFLAKE_PASSWORD')
WAREHOUSE = 'COMPUTE_WH'
DATABASE = 'OLIST_BRONZE'
SCHEMA = 'PUBLIC'
ROLE = 'ACCOUNTADMIN'

# Connect
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    role=ROLE
)
cursor = conn.cursor()

# Setup Database
print("Setting up database...")
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
cursor.execute(f"USE DATABASE {DATABASE}")
cursor.execute(f"USE SCHEMA {SCHEMA}")
print(f"Connected to {DATABASE}.{SCHEMA}")
```

## Step 3: Download & Load Data
```python
import kagglehub
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from pathlib import Path

# Download data
print("Downloading Olist dataset...")
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
dataset_dir = Path(path)

# File Mapping
files = {
    "olist_orders_dataset.csv": "BRONZE_ORDERS",
    "olist_order_items_dataset.csv": "BRONZE_ORDER_ITEMS",
    "olist_products_dataset.csv": "BRONZE_PRODUCTS",
    "olist_sellers_dataset.csv": "BRONZE_SELLERS",
    "olist_customers_dataset.csv": "BRONZE_CUSTOMERS",
    "olist_order_payments_dataset.csv": "BRONZE_ORDER_PAYMENT",  # Shortened to avoid length limits
    "olist_order_reviews_dataset.csv": "BRONZE_ORDER_REVIEWS",
    "olist_geolocation_dataset.csv": "BRONZE_GEOLOCATION",
    "product_category_name_translation.csv": "BRONZE_PRODUCT_CATEGORY_TRANSLATION"
}

# Load Loop
for csv_file, table_name in files.items():
    file_path = dataset_dir / csv_file
    print(f"Loading {table_name}...")
    
    # Read CSV
    df = pd.read_csv(file_path)
    
    # Clean Column Names (Snowflake usually likes uppercase)
    df.columns = [c.upper() for c in df.columns]
    
    # Create Table (Drop if exists for idempotency)
    # Using `write_pandas` with auto_create_table=True handles types automatically!
    success, n_chunks, n_rows, _ = write_pandas(
        conn,
        df,
        table_name,
        auto_create_table=True,
        overwrite=True
    )
    
    print(f"Loaded {n_rows} rows to {table_name}")

print("🎉 All data loaded successfully to Snowflake!")
conn.close()
```
