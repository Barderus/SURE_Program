import pandas as pd
import os

# --- Define your selected files
selected_files = [
    "../data/raw/canada_combined_fred_data_06-21-2025.csv",
    "../data/raw/germany_combined_fred_data_06-21-2025.csv",
    "../data/raw/japan_combined_fred_data_06-21-2025.csv",
    "../data/raw/us_combined_fred_data_06-21-2025.csv",
    "../data/raw/mexico_combined_data_06-21-2025.csv",
    "../data/raw/china_combined_data_06-22-2025.csv",

    "../script/combined_df.csv",

    "../data/processed/CLEAN_CAN_EX_IM.csv",
    "../data/processed/CLEAN_USA_EX_IM.csv",
    "../data/processed/CLEAN_JPN_EX_IM.csv",
    "../data/processed/CLEAN_EX_IM.csv",    # New Germany EX/IM in USD dollars
    "../data/processed/CLEAN_GER_EX_IM.csv",
    "../data/processed/CLEAN_CHI_EX_IM.csv",

    "../data/EPU/EPU_USA_cleaned.csv",
    "../data/EPU/EPU_CAN_cleaned.csv",
    "../data/EPU/EPU_MEX_cleaned.csv",
    "../data/EPU/EPU_GER_cleaned.csv",
    "../data/EPU/EPU_JAP_cleaned.csv",
    "../data/EPU/EPU_CHI_cleaned.csv",

    "../data/raw/CCI_OECD.csv",

    "../data/raw/spread/spread_only/CAN_spread.csv",
    "../data/raw/spread/spread_only/MEX_spread.csv",
    "../data/raw/spread/spread_only/JAP_spread.csv",
    "../data/raw/spread/spread_only/CHI_spread.csv",
    "../data/raw/spread/GER_yields.csv"
]


def rename_spread_column(df, file):
    if "Spread" in df.columns:
        country_code = os.path.basename(file).split("_")[0].upper()
        df = df.rename(columns={"Spread": f"YS_{country_code}"})
    return df

# --- Merge files
def merge_selected_files(file_list):
    merged_df = None
    for file in file_list:
        if not os.path.isfile(file):
            print(f"File not found: {file}")
            continue

        try:
            df = pd.read_csv(file, parse_dates=["date"])
            df = df.loc[:, ~df.columns.str.contains("^Unnamed", case=False)]  # drop Unnamed columns
            print(f"Loaded: {file} — shape: {df.shape}")
            df = rename_spread_column(df, file)
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on="date", how="outer")

        except Exception as e:
            print(f"Failed to read {file}: {e}")
            continue

    return merged_df

if __name__ == "__main__":
    df = merge_selected_files(selected_files)

    if df is None or df.empty:
        print("No data merged.")
        exit(1)

    df = df.sort_values("date").reset_index(drop=True)

    print("\nPreview of merged DataFrame:")
    print(df.head())
    print(df.columns)

    # Save output
    output_path = "../data/processed/master_file1.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")
