import pandas as pd
from pathlib import Path

from IPython.core.display_functions import display

data_dir = Path("../../data/manual-data/")
csv_files = sorted(data_dir.glob("*.csv"))

merged_df = None

print(f"Found {len(csv_files)} CSV files in: {data_dir.resolve()}")

for file in csv_files:
    try:
        print(f"\nReading: {file.name}")
        df = pd.read_csv(file)
        df["date"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp()
        print(f" -> Shape: {df.shape}")
        print(f" -> Columns: {list(df.columns)}")

        df.set_index("date", inplace=True)
        if merged_df is None:
            merged_df = df
        else:
            merged_df = merged_df.join(df, how="outer")  # outer merge keeps all dates

    except Exception as e:
        print(f"[Error] Problem reading {file.name}: {e}")

# Filter to only include data from 1995-01-01 onward
if merged_df is not None:
    merged_df.index = pd.to_datetime(merged_df.index, errors="coerce")
    merged_df = merged_df[merged_df.index >= pd.Timestamp("1995-01-01")]

    merged_df.reset_index(inplace=True)

    print(f"\nFinal merged DataFrame shape (1995+): {merged_df.shape}")
    display(merged_df.head())

    merged_df.to_csv("combined_df.csv", index=False)
else:
    print("\nNo data merged. Please check your files.")

