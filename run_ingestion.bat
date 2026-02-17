@echo off
echo ========================================
echo OLIST ERP ANALYTICS - DATA INGESTION
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

echo Running ingestion script...
python ingestion\main.py

echo.
echo ========================================
echo INGESTION COMPLETE!
echo ========================================
echo.
echo Your data is now in: olist_erp.duckdb
echo.
echo To query the data, run:
echo   python -c "import duckdb; conn = duckdb.connect('olist_erp.duckdb'); print(conn.execute('SHOW TABLES').fetchall())"
echo.
pause