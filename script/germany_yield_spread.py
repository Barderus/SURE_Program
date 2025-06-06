import os
from datetime import datetime
import pandas as pd
import pandas_datareader.data as web
from dotenv import load_dotenv

load_dotenv()

# Get the absolute path to the project root (one level up from /script)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# --- Fetch 10Y and 3M rates ---
print("Fetching 10Y and 3M yields for Germany...")
long_term = web.DataReader("IRLTLT01DEM156N", "fred")  # 10-Year
short_term = web.DataReader("IR3TIB01DEM156N", "fred")  # 3-Month

# --- Build Yield Spread DataFrame ---
spread_df = pd.DataFrame({
    "10Y": long_term["IRLTLT01DEM156N"],
    "3M": short_term["IR3TIB01DEM156N"]
})
spread_df["Spread"] = spread_df["10Y"] - spread_df["3M"]
spread_df.dropna(inplace=True)
spread_df.reset_index(inplace=True)
spread_df.rename(columns={"DATE": "date"}, inplace=True)

print("Yield spread data prepared.")

# --- Load latest Germany FRED dataset ---
files = [f for f in os.listdir(RAW_DIR) if f.startswith("germany_combined_fred_data") and f.endswith(".csv")]
if not files:
    raise FileNotFoundError("No Germany FRED data file found in /data/raw")

latest_file = sorted(files)[-1]
germany_df = pd.read_csv(os.path.join(RAW_DIR, latest_file), parse_dates=["date"])
print(f"Loaded: {latest_file}")

# --- Merge and Save ---
merged_df = pd.merge(germany_df, spread_df[["date", "Spread"]], on="date", how="outer")
merged_df = merged_df.sort_values("date")

timestamp = datetime.now().strftime("%m-%d-%Y")
merged_filename = os.path.join(RAW_DIR, f"germany_combined_fred_data_{timestamp}_with_yield_spread.csv")
merged_df.to_csv(merged_filename, index=False)

print(f"\nSaved merged data to: {merged_filename}")
print(merged_df.tail(10))
print(f"Total rows: {len(merged_df)}")
