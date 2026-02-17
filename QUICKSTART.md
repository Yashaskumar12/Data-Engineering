# Olist ERP Analytics - Quick Start Guide

## What You Need to Do Now

### 1. Set Up Kaggle API (5 minutes)

The `kagglehub` API will automatically download the Olist dataset for you!

**Steps:**
1. Go to https://www.kaggle.com (create account if needed)
2. Click your profile picture → Settings
3. Scroll to "API" section → Click "Create New API Token"
4. This downloads `kaggle.json` to your computer
5. Move it to the right location:
   - **Windows**: `C:\Users\<YourUsername>\.kaggle\kaggle.json`
   - **Mac/Linux**: `~/.kaggle/kaggle.json`

### 2. Set Up Snowflake (10 minutes)

**Get a Free Snowflake Account:**
1. Go to https://signup.snowflake.com/
2. Choose "Standard" edition (free trial)
3. Select a cloud provider (AWS, Azure, or GCP)
4. Complete registration

**Note Your Credentials:**
- Account Identifier (looks like: `xy12345.us-east-1`)
- Username
- Password
- Warehouse name (default: `COMPUTE_WH`)

### 3. Configure Your Project (2 minutes)

```bash
# Navigate to ingestion folder
cd ingestion

# Create Python virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install all dependencies (including kagglehub!)
pip install -r requirements.txt

# Create your .env file
copy .env.template .env  # Windows
# cp .env.template .env  # Mac/Linux
```

**Edit `.env` file** with your Snowflake credentials:
```
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=BRONZE
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

### 4. Run the Ingestion! (5-10 minutes)

```bash
python main.py
```

**What happens:**
1. ✓ Downloads Olist dataset from Kaggle (9 CSV files, ~100MB)
2. ✓ Connects to your Snowflake account
3. ✓ Creates BRONZE database and tables
4. ✓ Loads all CSV data into Snowflake
5. ✓ Shows you a summary report

### 5. Verify in Snowflake

Log into Snowflake web UI and run:
```sql
USE DATABASE BRONZE;
USE SCHEMA PUBLIC;

-- Check all tables were created
SHOW TABLES;

-- Check row counts
SELECT COUNT(*) FROM bronze_orders;
SELECT COUNT(*) FROM bronze_order_items;
SELECT COUNT(*) FROM bronze_products;
```

## Next Steps

Once Bronze layer is loaded:

1. **Set up dbt** - Transform data into Silver and Gold layers
2. **Build Power BI dashboards** - Create executive, logistics, and vendor dashboards
3. **Add data quality tests** - Ensure data integrity

## Troubleshooting

**Kaggle API Error:**
- Make sure `kaggle.json` is in the correct location
- Check file permissions (should be readable)

**Snowflake Connection Error:**
- Verify account identifier format (include region: `xy12345.us-east-1`)
- Check username/password are correct
- Ensure warehouse is running in Snowflake UI

**CSV Loading Error:**
- Check Snowflake has enough credits (free trial includes credits)
- Verify you have ACCOUNTADMIN role or appropriate permissions

## Project Structure

```
├── ingestion/
│   ├── main.py                 # Main script (uses kagglehub!)
│   ├── config.py               # Snowflake configuration
│   ├── logger.py               # Logging utilities
│   ├── ingestion_engine.py     # CSV → Snowflake engine
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Your credentials (create this)
│   └── .env.template           # Template for credentials
├── dbt_project/                # dbt transformations (coming next)
├── airflow/                    # Orchestration (optional)
└── powerbi/                    # Dashboards (final step)
```

## Questions?

Check the logs in `ingestion/logs/ingestion.log` for detailed error messages.
