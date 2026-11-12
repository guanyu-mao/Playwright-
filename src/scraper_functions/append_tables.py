import os
import pandas as pd

downloads_dir = r"C:\azure_tables"
excel_files = [os.path.join(downloads_dir, f) for f in os.listdir(downloads_dir) if f.endswith('.xlsx')]
print("Excel files found:", excel_files)

df_list = []
for f in excel_files:
    try:
        # Read all rows from the "Data" tab
        df = pd.read_excel(f, sheet_name="Data")
        print(f"{f}: {df.shape}")
        df_list.append(df)
    except Exception as e:
        print(f"Error reading {f}: {e}")

if not df_list:
    print("No dataframes loaded.")
    exit()

# Append all rows, keeping all columns (outer join)
combined_df = pd.concat(df_list, ignore_index=True, join='outer')
print("Combined shape:", combined_df.shape)
pd.set_option('display.max_rows', None)  # Show all rows in the output
print(combined_df)

# Ensure the output directory exists
output_dir = r"C:\combined_azure_table"
os.makedirs(output_dir, exist_ok=True)

# Overwrite the file if it exists
output_file = os.path.join(output_dir, "combined_azure_tables.csv")
combined_df.to_csv(output_file, index=False)
