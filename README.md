# Olist ERP Analytics - Complete Data Engineering Project

A **100% FREE** data engineering project using the Olist Brazilian E-Commerce dataset. No cloud signups, no credit cards, no costs!

## 🎯 What This Project Does

1. **Downloads** the Olist dataset from Kaggle (9 CSV files, ~100k rows)
2. **Loads** data into DuckDB (free, fast, local database)
3. **Transforms** data using dbt (coming next)
4. **Visualizes** with Power BI (coming next)

## 🚀 Quick Start (Windows)

### Step 1: Set Up Kaggle API (5 minutes)

1. Go to https://www.kaggle.com/settings
2. Click "Create New API Token" → downloads `kaggle.json`
3. Move it to: `C:\Users\<YourUsername>\.kaggle\kaggle.json`

### Step 2: Run Setup Script

```bash
setup.bat
```

This will:
- Create Python virtual environment
- Install all dependencies (DuckDB, pandas, kagglehub)
- Create configuration files

### Step 3: Run Ingestion

```bash
run_ingestion.bat
```

This will:
- Download Olist dataset from Kaggle
- Create `olist_erp.duckdb` database
- Load all 9 CSV files
- Show you a summary report

### Step 4: Query Your Data

```bash
query_data.bat
```

Or use the interactive query tool:
```bash
python query_tool.py
```

## 📁 Project Structure

```
├── ingestion/              # Data ingestion scripts
│   ├── main.py            # Main script (downloads from Kaggle)
│   ├── config.py          # DuckDB configuration
│   ├── logger.py          # Logging utilities
│   ├── ingestion_engine.py # CSV → DuckDB engine
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Configuration (created by setup)
├── dbt_project/           # dbt transformations (coming next)
├── powerbi/              # Power BI dashboards (coming next)
├── setup.bat             # Windows setup script
├── run_ingestion.bat     # Run ingestion
├── query_data.bat        # Query database
├── query_tool.py         # Interactive query tool
└── README.md             # This file
```

## 🔧 Technology Stack

- **DuckDB**: Free, fast, local database (no signup needed!)
- **Kagglehub**: Automatically downloads datasets
- **Python**: Data processing and automation
- **dbt**: Data transformations (next phase)
- **Power BI**: Dashboards (final phase)

## 📊 What You'll Get

After running the ingestion, you'll have:

1. **9 Bronze tables** in DuckDB:
   - `bronze_orders` (99,441 rows)
   - `bronze_order_items` (112,650 rows)
   - `bronze_products` (32,951 rows)
   - `bronze_sellers` (3,095 rows)
   - `bronze_customers` (99,441 rows)
   - `bronze_order_payments` (103,886 rows)
   - `bronze_order_reviews` (99,224 rows)
   - `bronze_geolocation` (1,000,163 rows)
   - `bronze_product_category_translation` (71 rows)

2. **Complete data pipeline** for your portfolio
3. **Ready for dbt transformations** (Silver/Gold layers)

## 🎓 Perfect For

- **Data Engineering students**: Learn real-world pipelines
- **Portfolio projects**: Showcase modern data stack skills
- **Job seekers**: Demonstrate end-to-end data engineering
- **Learning dbt/Power BI**: Foundation for next steps

## 🚀 Next Steps

After ingestion is complete, we'll:
1. Set up dbt for Silver/Gold transformations
2. Create star schema with fact/dimension tables
3. Build Power BI dashboards
4. Add data quality tests

## ❓ Troubleshooting

**Kaggle API Error**: Make sure `kaggle.json` is in the right location
**Python Errors**: Run `setup.bat` to ensure all dependencies are installed
**Dataset Download Issues**: Check your internet connection

## 📚 Resources

- [Olist Dataset on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [dbt Documentation](https://docs.getdbt.com/)

---

**Ready to start?** Run `setup.bat` then `run_ingestion.bat`!