"""
This script merges the files in the MERGE folder since pandas was being super annoying about it, ugh
"""

import os
import pandas as pd

DATA_DIR = "../../data/merge_data"

# List of all cleaned CSV filenames
files_to_merge = [
    "US_cleaned_1950_onward.csv",
    "POP_ALL.csv",
    "MEX_spread_YYYY-MM.csv",
    "JAP_spread_YYYY-MM.csv",
    "GDPG_All.csv",
    "CHI_spread_YYYY-MM.csv",
    "CAN_cleaned_1950_onward.csv",
    "CAN_spread_YYYY-MM.csv",
    "MEX_cleaned_1950_onward.csv",
    "GER_cleaned_1950_onward.csv",
    "JAP_cleaned_1950_onward.csv",
    "CHI_cleaned_1950_onward.csv",
    "CCI_ALL.csv"
]

merged_df = None

# Merge all files on 'date'
for filename in files_to_merge:
    path = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(path)

    if "date" not in df.columns:
        raise ValueError(f"'date' column missing in {filename}")

    if merged_df is None:
        merged_df = df
    else:
        merged_df = pd.merge(merged_df, df, on="date", how="outer")

# Sort by date and reset index
merged_df = merged_df.sort_values("date").reset_index(drop=True)

output_path = os.path.join(DATA_DIR, "master_file_merged.csv")
merged_df.to_csv(output_path, index=False)
print(f"Merged file saved to: {output_path}")
