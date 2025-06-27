import pandas as pd

# Load the master dataset
master_file = pd.read_csv("../data/processed/clean_master_file1.csv", parse_dates=["date"], index_col="date")

# Ensure the index is monthly and continuous
full_index = pd.date_range(start=master_file.index.min(), end=master_file.index.max(), freq="MS")

# Extract all country codes from column suffixes (e.g., GDP_CAN → CAN)
countries = sorted({col.split("_")[-1] for col in master_file.columns if "_" in col})

# Path to save output
output_path = "../data/summary_tables/country_aligned_timeseries1.xlsx"

# Save one sheet per country
with pd.ExcelWriter(output_path) as writer:
    for country in countries:
        # Filter columns for the current country
        country_cols = [col for col in master_file.columns if col.endswith(f"_{country}")]
        if not country_cols:
            continue

        # Extract just the variable name (drop suffix)
        country_df = master_file[country_cols].copy()
        country_df.columns = [col.rsplit("_", 1)[0] for col in country_cols]

        # Reindex to create a balanced time series
        country_df = country_df.reindex(full_index)
        country_df.index.name = "date"

        # Drop rows where all values are NaN
        country_df = country_df.dropna(how="all")

        # Write to individual sheet
        country_df.to_excel(writer, sheet_name=country)
