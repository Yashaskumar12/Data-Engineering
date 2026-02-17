
import subprocess
import os
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.absolute()
INGESTION_DIR = BASE_DIR / "ingestion"
DBT_DIR = BASE_DIR / "dbt_project"
VENV_PYTHON = INGESTION_DIR / "venv" / "Scripts" / "python.exe"
DBT_EXE = INGESTION_DIR / "venv" / "Scripts" / "dbt.exe"

def run_step(step_name, command, cwd):
    print("\n" + "=" * 80)
    print(f"RUNNING: {step_name}")
    print("=" * 80)
    
    try:
        # Use shell=True for Windows command execution consistency
        result = subprocess.run(
            command, 
            cwd=cwd, 
            check=True, 
            shell=True,
            capture_output=False  # Stream output directly to console
        )
        print(f"\n✅ {step_name} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {step_name} failed with exit code {e.returncode}")
        return False

def main():
    print("Starting End-to-End Pipeline...")
    
    # Step 1: Ingestion
    if not run_step(
        "Data Ingestion", 
        f'"{VENV_PYTHON}" main.py', 
        INGESTION_DIR
    ):
        sys.exit(1)
        
    # Step 2: dbt Run
    if not run_step(
        "dbt Transformation (Run)", 
        f'"{DBT_EXE}" run', 
        DBT_DIR
    ):
        sys.exit(1)
        
    # Step 3: dbt Test
    if not run_step(
        "dbt Quality Checks (Test)", 
        f'"{DBT_EXE}" test', 
        DBT_DIR
    ):
        sys.exit(1)
        
    # Step 4: Export to CSV (Using Export Script)
    if not run_step(
        "Exporting Data for Power BI", 
        f'"{VENV_PYTHON}" ingestion/export.py', 
        BASE_DIR
    ):
        print("Warning: export failed")
    
    print("\n" + "=" * 80)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"You can now open the CSV files in 'powerbi/' folder directly in Power BI or Excel.")

if __name__ == "__main__":
    main()
