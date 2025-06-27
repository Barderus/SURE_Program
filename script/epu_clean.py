import pandas as pd
import os

# Directory paths
raw_dir = "../data/EPU/"
processed_dir = "../data/EPU/"

# List of country codes and file names
countries = {
    "MEX": "Mexico_Policy_Uncertainty_Data.xlsx",
    "USA": "US_Policy_Uncertainty_Data.xlsx",
    "GER": "Europe_Policy_Uncertainty_Data.xlsx",
    "JAP": "Japan_Policy_Uncertainty_Data.xlsx",
    "CAN": "Canada_Policy_Uncertainty_Data.xlsx",
    "CHI": "SCMP_China_Policy_Uncertainty_Data.xlsx",
}

# Loop through each country
for code, filename in countries.items():
    filepath = os.path.join(raw_dir, filename)

    try:
        df = pd.read_excel(filepath)

        # Build 'date' column
        df["date"] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))

        epu_col = f"EPU_{code}"
        df = df[["date", epu_col]].sort_values("date").reset_index(drop=True)

        # Keep only relevant columns
        df = df[["date", epu_col]].sort_values("date").reset_index(drop=True)

        # Save cleaned file
        output_path = os.path.join(processed_dir, f"{epu_col}_cleaned.csv")
        df.to_csv(output_path, index=False)
        print(f"{code} processed successfully.")

    except Exception as e:
        print(f"Error processing {code}: {e}")
