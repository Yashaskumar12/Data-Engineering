
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
*   Replace `YOUR_PROJECT_ID` with your actual GCP Project ID.
*   We will create a dataset called `olist_bronze`.

```python
project_id = 'YOUR_PROJECT_ID'  # <--- REPLACE THIS 
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
