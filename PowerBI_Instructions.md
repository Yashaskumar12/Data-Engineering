
# Connecting Power BI to Your Data

There are two main ways to connect Power BI to your DuckDB database (`olist.db`).

## Option A: Direct Connection (Recommended via ODBC)

This allows Power BI to query the database directly.

**Prerequisites:**
1. Download and install the [DuckDB ODBC Driver for Windows](https://github.com/duckdb/duckdb/releases/latest/download/duckdb_odbc-windows-amd64.zip).
2. Unzip and run `setup.exe`.

**Steps:**
1. Open **ODBC Data Sources (64-bit)** app in Windows.
2. Click **Add...** -> Select **DuckDB Driver** -> Finish.
3. **Data Source Name**: `Olist_Local`
4. **Database File**: Browse to `c:\Users\E.Gagan\OneDrive\Documents\DATA ENGINEERING\ingestion\olist.db`
5. Click **OK**.
6. Open **Power BI Desktop**.
7. Click **Get Data** -> **More...** -> **ODBC**.
8. Select `Olist_Local` from the list.
9. In the Navigator, you will see your tables (e.g., `main_marts.fct_orders`, `main_marts.dim_customers`).

---

## Option B: Export to Parquet (No Driver Needed)

If you can't install the ODBC driver, we can export the "Gold" tables to Parquet files, which Power BI reads natively.

1. **Run this Python snippet** (can be added to `run_pipeline.py`):

```python
import duckdb
con = duckdb.connect('ingestion/olist.db')

# Export Marts to Parquet
con.execute("COPY (SELECT * FROM main_marts.fct_orders) TO 'powerbi/fct_orders.parquet' (FORMAT PARQUET)")
con.execute("COPY (SELECT * FROM main_marts.dim_customers) TO 'powerbi/dim_customers.parquet' (FORMAT PARQUET)")
con.execute("COPY (SELECT * FROM main_marts.dim_products) TO 'powerbi/dim_products.parquet' (FORMAT PARQUET)")
```

2. Open **Power BI**.
3. **Get Data** -> **Parquet**.
4. Select the generated `.parquet` files.
