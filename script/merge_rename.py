import pandas as pd
import re
import os

# --- Define your selected files
selected_files = [
    "../data/canada_combined_fred_data_06-10-2025.csv",
    "../data/CCI_OECD.csv",
    "../data/china_combined_data_06-10-2025.csv",
    "../data/germany_combined_fred_data_06-10-2025.csv",
    "../data/japan_combined_fred_data_06-10-2025.csv",
    "../data/us_combined_fred_data_06-10-2025.csv",
    "../data/yield_spreads_by_country_monthly.csv"
]

# --- Column renaming function
def standardize_column_name(col):
    if col == "date":
        return "date"

    country_map = {
        "us": "us",
        "canada": "canada",
        "china": "china",
        "germany": "germany",
        "japan": "japan",
        "mexico": "mexico"
    }

    for key in country_map:
        if col.lower().startswith(key):
            country = country_map[key]
            break
    else:
        if "CCI_OECD" in col:
            match = re.search(r"– ([\w\s]+) –", col)
            if match:
                country_name = match.group(1).lower().split()[0]
                return f"{country_name}_cci"
            else:
                return "unknown_cci"

        if "yield_spreads_by_country_monthly" in col.lower():
            match = re.search(r"yield_spreads_by_country_monthly_([A-Za-z]+)", col)
            if match:
                return f"{match.group(1).lower()}_yield_spread"
            else:
                return col.lower()

        return col.lower()

    parts = col.split("_")
    indicators = [
        "gdp", "cci", "inflation", "yield", "unemployment",
        "bonds", "rate", "spread", "sentiment", "epu",
        "exports", "imports", "balance", "production"
    ]

    for part in reversed(parts):
        clean = part.lower()
        if clean in indicators:
            return f"{country}_{clean}"
        if "gdp" in clean:
            return f"{country}_gdp"
        if "epu" in clean:
            return f"{country}_epu"
        if "unemployment" in clean:
            return f"{country}_unemployment"
        if "inflation" in clean:
            return f"{country}_inflation"
        if "sentiment" in clean:
            return f"{country}_sentiment"
        if "yield" in clean or "spread" in clean:
            return f"{country}_yield_spread"

    return f"{country}_{parts[-1].lower()}"

# --- Merge files
def merge_selected_files(file_list):
    merged_df = None

    for file in file_list:
        try:
            df = pd.read_csv(file, parse_dates=["date"])
            print(f"Loaded: {file} — shape: {df.shape}")

            # Create a unique prefix from the filename (without extension)
            prefix = os.path.splitext(os.path.basename(file))[0]

            # Rename columns except 'date'
            df = df.rename(columns={col: f"{prefix}_{col}" for col in df.columns if col != "date"})

        except Exception as e:
            print(f"Failed to read {file}: {e}")
            continue

        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on="date", how="outer")

    return merged_df


# --- Apply column renaming
def rename_columns(df):
    renamed = {col: standardize_column_name(col) for col in df.columns}
    return df.rename(columns=renamed)

if __name__ == "__main__":
    df = merge_selected_files(selected_files)

    if df is None:
        print("No data merged.")
        exit(1)

    df = rename_columns(df)
    df = df.sort_values("date").reset_index(drop=True)

    print("\nPreview of merged and renamed DataFrame:")
    print(df.head())

    # Save output
    output_path = "../data/merged_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")
