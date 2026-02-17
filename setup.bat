@echo off
echo ========================================
echo OLIST ERP ANALYTICS - SETUP SCRIPT
echo ========================================
echo.

echo Step 1: Creating Python virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Step 3: Installing dependencies...
pip install -r ingestion\requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Step 4: Creating .env file...
if not exist ingestion\.env (
    copy ingestion\.env.template ingestion\.env
    echo Created ingestion\.env file
) else (
    echo ingestion\.env already exists
)

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure you have kaggle.json in C:\Users\%USERNAME%\.kaggle\
echo 2. Run: python ingestion\main.py
echo.
echo The script will:
echo - Download Olist dataset from Kaggle
echo - Create local DuckDB database
echo - Load all 9 CSV files
echo.
pause