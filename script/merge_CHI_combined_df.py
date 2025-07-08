import pandas as pd

# Load both cleaned CSVs
manual_path = "../data/combined_data/CHI_manual_data.csv"
combined_path = "../data/combined_data/china_combined_data_06-27-2025_FIXED.csv"

df_manual = pd.read_csv(manual_path)
print(df_manual.head())
print(df_manual.columns)
print()
df_combined = pd.read_csv(combined_path)
print(df_combined.head())
print(df_combined.columns)
# Ensure date format is consistent as 'YYYY-MM'
df_manual["date"] = pd.to_datetime(df_manual["date"], errors="coerce").dt.strftime("%Y-%m")
df_combined["date"] = pd.to_datetime(df_combined["date"], errors="coerce").dt.strftime("%Y-%m")

# Drop duplicates just in case
df_manual = df_manual.drop_duplicates()
df_combined = df_combined.drop_duplicates()

# Merge on 'date'
merged_df = pd.merge(df_combined, df_manual, on="date", how="outer", suffixes=("", "_manual"))

for col in merged_df.columns:
    if col.endswith("_manual") and col[:-7] in merged_df.columns:
        base = col[:-7]
        merged_df[base] = merged_df[base].combine_first(merged_df[col])
        merged_df.drop(columns=[col], inplace=True)

# Sort by date
merged_df = merged_df.sort_values("date")

# Save result
output_path = "../data/combined_data/china_final_merged_data.csv"
merged_df.to_csv(output_path, index=False)
print(f"Merged file saved to: {output_path}")
