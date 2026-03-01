
# Olist Data Engineering: Colab to BigQuery Pipeline

## Prerequisites
1.  **Google Cloud Project**: You need a Google Cloud Project with BigQuery API enabled.
2.  **Authentication**: This notebook will ask for authentication to access your Google Cloud account.

## Step 1: Install Libraries
```python
!pip install google-cloud-bigquery pandas kagglehub db-dtypes
```

## Step 2: Authenticate
```python
from google.colab import auth
auth.authenticate_user()
print("Authenticated")
```

## Step 3: Define Project & Dataset
*   We will create a dataset called `olist_bronze`.

```python
project_id = 'data-engineering-488606'  # Your exact Project ID
dataset_id = 'olist_bronze'

from google.cloud import bigquery
client = bigquery.Client(project=project_id)

# Create dataset if not exists
dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
dataset.location = "US"
dataset = client.create_dataset(dataset, exists_ok=True)
print(f"Dataset {dataset_id} created.")
```

## Step 4: Download & Load Data
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
    "olist_order_items_dataset.csv": "bronze_order_items",
    "olist_products_dataset.csv": "bronze_products",
    "olist_sellers_dataset.csv": "bronze_sellers",
    "olist_customers_dataset.csv": "bronze_customers",
    "olist_order_payments_dataset.csv": "bronze_order_payments",
    "olist_order_reviews_dataset.csv": "bronze_order_reviews",
    "olist_geolocation_dataset.csv": "bronze_geolocation",
    "product_category_name_translation.csv": "bronze_product_category_translation"
}

# Load Loop
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
)

for csv_file, table_name in files.items():
    file_path = dataset_dir / csv_file
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    
    print(f"Loading {table_name}...")
    
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    
    job.result()  # Wait for job to complete
    
    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows to {table_id}")

print("🎉 All data loaded successfully to BigQuery!")
```

## Step 5: Automate Transformations (Run SQL Queries)
Run this single cell to automatically execute the dimensional modeling SQL code and build the final Gold tables.

```python
print("Starting Data Transformations...")

query_dim_customers = f"""
CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.vw_dim_customers` AS
WITH customers AS (
    SELECT * FROM `{project_id}.{dataset_id}.bronze_customers`
),
geolocation AS (
    SELECT * FROM `{project_id}.{dataset_id}.bronze_geolocation`
),
final AS (
    SELECT
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix AS zip_code,
        customer_city AS city,
        customer_state AS state
    FROM customers
)
SELECT * FROM final;
"""

query_fct_orders = f"""
CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.vw_fct_orders` AS
WITH orders AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        CAST(order_purchase_timestamp AS TIMESTAMP) as order_purchase_at,
        CAST(order_approved_at AS TIMESTAMP) as order_approved_at,
        CAST(order_delivered_carrier_date AS TIMESTAMP) as order_delivered_carrier_at,
        CAST(order_delivered_customer_date AS TIMESTAMP) as order_delivered_customer_at,
        CAST(order_estimated_delivery_date AS TIMESTAMP) as order_estimated_delivery_at
    FROM `{project_id}.{dataset_id}.bronze_orders`
),
order_items AS (
    SELECT
        order_id,
        order_item_id,
        product_id,
        seller_id,
        price,
        freight_value
    FROM `{project_id}.{dataset_id}.bronze_order_items`
),
order_payments AS (
    SELECT * FROM `{project_id}.{dataset_id}.bronze_order_payments`
),
order_items_agg AS (
    SELECT
        order_id,
        COUNT(order_item_id) as total_items,
        SUM(price) as total_item_value,
        SUM(freight_value) as total_freight_value
    FROM order_items
    GROUP BY 1
),
order_payments_agg AS (
    SELECT
        order_id,
        SUM(payment_value) as total_payment_value,
        STRING_AGG(DISTINCT payment_type, ', ') as payment_types
    FROM order_payments
    GROUP BY 1
),
final AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_status,
        o.order_purchase_at,
        o.order_approved_at,
        o.order_delivered_carrier_at,
        o.order_delivered_customer_at,
        o.order_estimated_delivery_at,
        COALESCE(i.total_items, 0) as number_of_items,
        COALESCE(i.total_item_value, 0) as item_value,
        COALESCE(i.total_freight_value, 0) as freight_value,
        COALESCE(p.total_payment_value, 0) as total_amount,
        p.payment_types,
        TIMESTAMP_DIFF(o.order_delivered_customer_at, o.order_purchase_at, DAY) as delivery_time_days,
        CASE 
            WHEN o.order_delivered_customer_at > o.order_estimated_delivery_at THEN TRUE 
            ELSE FALSE 
        END as is_delayed
    FROM orders o
    LEFT JOIN order_items_agg i ON o.order_id = i.order_id
    LEFT JOIN order_payments_agg p ON o.order_id = p.order_id
)
SELECT * FROM final;
"""

# Run the queries!
print("Building Dimension Table: vw_dim_customers...")
client.query(query_dim_customers).result()

print("Building Fact Table: vw_fct_orders...")
client.query(query_fct_orders).result()

print("✅ Data Transformations Complete! Your Data Pipeline is built.")
```
