
# Olist Data Engineering: Colab to Databricks Pipeline

## Prerequisites
1.  **Databricks Community Edition**: [Sign Up Here](https://community.cloud.databricks.com/login.html).
    *   Click "Get Started for Free" -> "Get started with Community Edition" (small link at bottom).
2.  **Access Token**:
    *   Go to **Settings** -> **User Settings** -> **Access Tokens**.
    *   Click **Generate New Token**. Copy it immediately!
3.  **Compute Cluster**:
    *   Go to **Compute** -> **Create Compute**.
    *   Name: `Analytic_Cluster` (or anything).
    *   Select `12.2 LTS` or similar (standard settings are fine).
    *   Wait for it to start (green circle).
    *   Copy the **Server Hostname** & **HTTP Path** from "Advanced Options" -> "JDBC/ODBC".

## Step 1: Install Libraries
```python
!pip install databricks-sql-connector pandas kagglehub
```

## Step 2: Configure Connection
*   In Colab, go to "Keys" (🔑).
*   Add secret: `DATABRICKS_TOKEN`.

```python
from databricks import sql
from google.colab import userdata

# Configuration
SERVER_HOSTNAME = "community.cloud.databricks.com"  # <--- REPLACE IF DIFFERENT
HTTP_PATH = "/sql/1.0/warehouses/unique_cluster_id" # <--- REPLACE THIS (from Compute -> JDBC)
ACCESS_TOKEN = userdata.get('DATABRICKS_TOKEN')
CATALOG = "hive_metastore" # Community Edition uses hive_metastore by default
SCHEMA = "default"

# Connect
conn = sql.connect(
    server_hostname=SERVER_HOSTNAME,
    http_path=HTTP_PATH,
    access_token=ACCESS_TOKEN
)
cursor = conn.cursor()

# Setup Schema
print("Setting up schema...")
cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
print(f"Connected to {CATALOG}.{SCHEMA}")
```

## Step 3: Download & Load Data
Databricks SQL Connector doesn't have a direct `write_pandas` equivalent for community edition easily accessible via SQL Endpoint, so we use `INSERT` in batches or volume upload. 
**Simpler approach for Colab -> Community Edition**: We generate `INSERT` statements.

```python
import kagglehub
import pandas as pd
from pathlib import Path

# Download data
print("Downloading Olist dataset...")
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
dataset_dir = Path(path)

# File Mapping
files = {
    "olist_orders_dataset.csv": "bronze_orders",
    "olist_customers_dataset.csv": "bronze_customers",
    # Add other files here...
}

def load_table(table_name, df):
    # Create Table Logic (Simplified for brevity - relies on string types mostly for bronze)
    cols = ", ".join([f"{c} STRING" for c in df.columns])
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute(f"CREATE TABLE {table_name} ({cols})")
    print(f"Created table {table_name}")
    
    # Insert Data (Batching to avoid timeouts)
    batch_size = 1000
    total_rows = len(df)
    
    insert_sql_base = f"INSERT INTO {table_name} VALUES "
    
    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i : i + batch_size]
        values = []
        for _, row in batch.iterrows():
            # Escape strings to avoid SQL errors
            row_vals = [f"'{str(x).replace("'", "''")}'" for x in row]
            values.append(f"({','.join(row_vals)})")
        
        full_sql = insert_sql_base + ",".join(values)
        cursor.execute(full_sql)
        print(f"  Inserted rows {i} to {min(i+batch_size, total_rows)}")

# Load Loop
for csv_file, table_name in files.items():
    file_path = dataset_dir / csv_file
    print(f"Processing {table_name}...")
    df = pd.read_csv(file_path).fillna('') # Replace NaNs with empty string for simplicity
    load_table(table_name, df)

print("🎉 All data loaded successfully to Databricks!")
conn.close()
```
