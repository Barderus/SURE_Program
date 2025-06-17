import os
import re
import pandas as pd
from datetime import datetime

# --- Config ---
RAW_DIR = "../data/raw"
OUTPUT_DIR = "data/processed"
OUTPUT_NAME = "global_combined_data"

# Get project root: one level above the script folder
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Ensure output dir exists ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Helper to extract country from filename ---
def extract_country(filename):
    match = re.match(r"([a-z]+)_combined_fred_data_", filename)
    return match.group(1).capitalize() if match else "Unknown"

# --- Load all country CSVs ---
def load_country_csvs(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    dataframes = []

    for file in csv_files:
        path = os.path.join(directory, file)
        country = extract_country(file)
        try:
            df = pd.read_csv(path)
            if "date" not in df.columns:
                print(f"Skipping {file} (no 'date' column)")
                continue
            df["date"] = pd.to_datetime(df["date"])
            df["country"] = country
            dataframes.append(df)
            print(f"Loaded: {file} as {country}")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    return dataframes


# --- Merge on date ---
def merge_all_by_date(dfs):
    combined = pd.concat(dfs, axis=0)
    combined = combined.sort_values("date")
    return combined

# --- Save ---
def save_combined_csv(df, prefix="combined_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = os.path.join(OUTPUT_DIR, f"{prefix}_{timestamp}.csv")
    df.to_csv(filename, index=False)
    print(f"\nCombined data saved to: {filename}")
    return filename

# --- Main ---
def main():
    print("Combining country CSVs by date from data/raw...\n")
    dfs = load_country_csvs(RAW_DIR)
    if dfs:
        combined = merge_all_by_date(dfs)
        save_combined_csv(combined)
        print(combined.tail(10))
        print(f"\nTotal records: {len(combined)}")
    else:
        print("\nNo CSV files found in data/raw.")

if __name__ == "__main__":
    main()
