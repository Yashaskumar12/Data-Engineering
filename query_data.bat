@echo off
echo ========================================
echo QUERY OLIST DATA IN DUCKDB
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

echo Connecting to DuckDB...
python -c "
import duckdb
import pandas as pd

# Connect to the database
conn = duckdb.connect('olist_erp.duckdb')

print('=== DATABASE OVERVIEW ===')
print()

# Show all tables
tables = conn.execute('SHOW TABLES').fetchall()
print(f'Found {len(tables)} tables:')
for table in tables:
    print(f'  - {table[0]}')

print()
print('=== TABLE ROW COUNTS ===')
print()

# Count rows in each table
for table in tables:
    table_name = table[0]
    count = conn.execute(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]
    print(f'{table_name}: {count:,} rows')

print()
print('=== SAMPLE DATA ===')
print()

# Show sample from orders table
if 'bronze_orders' in [t[0] for t in tables]:
    print('First 5 orders:')
    sample = conn.execute('SELECT * FROM bronze_orders LIMIT 5').fetchdf()
    print(sample.to_string())

print()
print('=== QUERY EXAMPLES ===')
print()
print('To run your own queries:')
print('1. python -c \"import duckdb; conn = duckdb.connect(\"olist_erp.duckdb\"); result = conn.execute(\"YOUR SQL HERE\").fetchdf(); print(result)\"')
print('2. Or use: python query_tool.py')
"

echo.
pause