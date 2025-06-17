import os
import pandas as pd

# Input directory with full yield data
input_dir = "../data/raw/spread"
# Output directory to save spread-only files
output_dir = "../data/raw/spread/spread_only"
os.makedirs(output_dir, exist_ok=True)

# Map of filenames to their 10Y and 2Y yield column names
file_column_map = {
    "CAN_yields.csv": ("10YS_CAN", "2YS_CAN"),
    "MEX_yields.csv": ("10YS_MEX", "2YS_MEX"),
    "CHI_yields.csv": ("10YS_CHI", "2YS_CHI"),
    "JAP_yields.csv": ("10YS_JAP", "2YS_JAP")
}

for file_name, (col_10y, col_2y) in file_column_map.items():
    input_path = os.path.join(input_dir, file_name)

    try:
        df = pd.read_csv(input_path, parse_dates=["date"])

        # Normalize date to month-start
        df["date"] = df["date"].dt.to_period("M").dt.to_timestamp()

        if col_10y not in df.columns or col_2y not in df.columns:
            print(f"Missing required columns in {file_name} — skipping.")
            continue

        df["Spread"] = df[col_10y] - df[col_2y]
        spread_df = df[["date", "Spread"]].dropna()

        print(f"\n===== {file_name.replace('_yields.csv','')} Spread Preview =====")
        print(spread_df.head())

        # Save only the spread
        output_file = file_name.replace("_yields.csv", "_spread.csv")
        output_path = os.path.join(output_dir, output_file)
        spread_df.to_csv(output_path, index=False)

    except Exception as e:
        print(f"Error with {file_name}: {e}")
