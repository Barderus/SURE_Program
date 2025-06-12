import os
import pandas as pd

# Directory containing the CSVs
data_dir = "../data/raw"

# Mapping of each file to its yield column names
file_column_map = {
    "CAN_yields.csv": ("10YS_CAN", "2YS_CAN"),
    "MEX_yields.csv": ("10YS_MEX", "2YS_MEX"),
    "GER_yields.csv": ("10YS_GER", "2YS_GER"),
    "CHI_yields.csv": ("10YS_CHI", "2YS_CHI"),
    "JAP_yields.csv": ("10YS_JAP", "2YS_JAP")
}

for file_name, (col_10y, col_2y) in file_column_map.items():
    path = os.path.join(data_dir, file_name)

    try:
        df = pd.read_csv(path, parse_dates=["date"])

        # Normalize all dates to the first of the month
        df["date"] = df["date"].dt.to_period("M").dt.to_timestamp()

        if col_10y not in df.columns or col_2y not in df.columns:
            print(f"Missing required columns in {file_name} — skipping.")
            continue

        df["Spread"] = df[col_10y] - df[col_2y]
        print(f"\n===== {file_name.replace('_yields.csv','')} Spread Preview =====")
        print(df[["date", col_10y, col_2y, "Spread"]].dropna().head())

        # Save back to the same file
        df.to_csv(path, index=False)

    except Exception as e:
        print(f"Error with {file_name}: {e}")
