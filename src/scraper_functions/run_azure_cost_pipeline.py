import os
import sys
import subprocess
import pandas as pd

def validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        assert not df.empty, "CSV is empty!"
        assert df.isnull().sum().sum() < df.size * 0.5, "Too many missing values!"
        print(f"Validation passed for {file_path}")
        return True
    except Exception as e:
        print(f"Validation failed for {file_path}: {e}")
        return False

def run_script(script_path):
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Script {script_path} failed.")

if __name__ == "__main__":
    # 1. Scrape Azure cost data
    print("Starting scraping...")
    run_script(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "scrape.py")))

    # 2. Combine and append data
    print("Combining and appending data...")
    run_script(os.path.join(os.path.dirname(__file__), "combine_data.py"))
    run_script(os.path.join(os.path.dirname(__file__), "update_table.py"))

    # 3. Validate combined data
    updated_file = r"C:\updated_azure_table\Combined Resource Groups for Prod & Pre-Prod.csv"
    if not validate_csv(updated_file):
        sys.exit("Validation failed. Stopping pipeline.")

    # 4. Run analysis and generate report
    print("Running analysis and generating report...")
    run_script(os.path.join(os.path.dirname(__file__), "tech_analysis.py"))

    print("Pipeline completed successfully.")