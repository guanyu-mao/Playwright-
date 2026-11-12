import os
import pandas as pd

# Paths to the files and directories
updated_dir = r"C:\updated_azure_table"
combined_dir = r"C:\combined_azure_table"

updated_file = os.path.join(updated_dir, "Combined Resource Groups for Prod & Pre-Prod.csv")
combined_file = os.path.join(combined_dir, "combined_azure_tables.csv")

# Read the updated table (this will define the format)
updated_df = pd.read_csv(updated_file)
print(f"Updated table shape: {updated_df.shape}")

# Read the combined table
combined_df = pd.read_csv(combined_file)
print(f"Combined table shape: {combined_df.shape}")

# Align combined_df to updated_df columns, filling missing columns with blanks
combined_aligned = combined_df.reindex(columns=updated_df.columns)

# Append the combined data to the updated data
final_df = pd.concat([updated_df, combined_aligned], ignore_index=True)

print("Final table shape:", final_df.shape)

# Overwrite the updated file with the new data
final_df.to_csv(updated_file, index=False)
print(f"Updated file saved to: {updated_file}")