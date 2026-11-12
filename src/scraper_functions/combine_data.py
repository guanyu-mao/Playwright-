import os
import pandas as pd

def combine_data(source_folder: str, target_folder: str):
    """
    Appends all CSV files from source_folder to the first file found in target_folder.
    The target file can be Excel (.xlsx) or CSV (.csv).
    The file must already exist and will be updated by appending new data below the existing rows.
    Only columns matching the target file will be appended.
    """
    # Find the first file (Excel or CSV) in the target folder
    target_files = [f for f in os.listdir(target_folder) if f.endswith('.xlsx') or f.endswith('.csv')]
    if not target_files:
        print(f"ERROR: No Excel or CSV file found in {target_folder}.")
        return

    target_filename = target_files[0]
    target_path = os.path.join(target_folder, target_filename)
    print(f"Target file: {target_path}")

    # Read the existing target file
    if target_filename.endswith('.xlsx'):
        existing_df = pd.read_excel(target_path)
    elif target_filename.endswith('.csv'):
        existing_df = pd.read_csv(target_path)
    else:
        print(f"ERROR: Unsupported file type for {target_filename}")
        return

    target_columns = existing_df.columns.tolist()

    # Collect all CSVs from the source folder
    dfs = []
    for file in os.listdir(source_folder):
        if file.endswith('.csv'):
            file_path = os.path.join(source_folder, file)
            df = pd.read_csv(file_path)
            # Match columns to target file
            df = df.reindex(columns=target_columns)
            dfs.append(df)
            print(f"Loaded {file_path} with {len(df)} rows and columns matched to target.")

    if not dfs:
        print("No CSV files found to append.")
        return

    # Concatenate all new data
    new_data = pd.concat(dfs, ignore_index=True)
    print(f"Total new rows to append: {len(new_data)}")

    # Append new data to existing data
    updated_df = pd.concat([existing_df, new_data], ignore_index=True)

    # Save back to the same file (overwriting it)
    if target_filename.endswith('.xlsx'):
        updated_df.to_excel(target_path, index=False)
    elif target_filename.endswith('.csv'):
        updated_df.to_csv(target_path, index=False)
    print(f"Appended data and updated file: {target_path}")

# Example usage:
if __name__ == "__main__":
    try:
        print("Starting combine_data function...")
        combine_data(
            source_folder=r"C:\combined_azure_table",
            target_folder=r"C:\updated_azure_table"
        )
        print("combine_data completed successfully!")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()