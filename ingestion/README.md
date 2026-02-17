# Olist ERP Analytics - Data Ingestion

Python-based data ingestion system for loading Olist Brazilian E-Commerce CSV files into Snowflake Bronze layer.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Kaggle API (for dataset download):
   - Go to https://www.kaggle.com/settings
   - Click "Create New API Token" to download `kaggle.json`
   - Place `kaggle.json` in:
     - Linux/Mac: `~/.kaggle/kaggle.json`
     - Windows: `C:\Users\<username>\.kaggle\kaggle.json`

4. Configure Snowflake credentials:
```bash
cp .env.template .env
# Edit .env with your Snowflake credentials
```

## Usage

Run the ingestion script (automatically downloads dataset from Kaggle):
```bash
python main.py
```

The script will:
1. Download the Olist dataset from Kaggle (if not already cached)
2. Connect to Snowflake
3. Create Bronze layer tables
4. Load all 9 CSV files
5. Report summary of results

## Project Structure

- `config.py` - Snowflake configuration management
- `logger.py` - Logging utilities
- `ingestion_engine.py` - CSV to Snowflake ingestion engine
- `main.py` - Main execution script
- `tests/` - Unit and property-based tests
