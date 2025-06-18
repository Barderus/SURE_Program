import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
FILE_PATH = "../data/raw/inflation/Japan_Inflation_Data.csv"


FRED_SERIES = {
    "JPNEPUINDXM": {"units": "lin", "frequency": "m"},
    "JPNPROINDAISMEI": {"units": "lin", "frequency": "a"},
    "FPCPITOTLZGJPN": {"units": "lin", "frequency": "a"},
    "LRUN64TTJPA156S": {"units": "lin", "frequency": "a"},
    "JPNRGDPNGS": {"units": "lin", "frequency": "a"},
    "JPNRECDP": {"units": "lin", "frequency": "m"},
    "JPNRGDPEXP": {"units": "lin", "frequency": "a"},
    "JPNRGDPC": {"units": "lin", "frequency": "a"},
    "INTGSBJPM193N": {"units": "lin", "frequency": "m"},
    "JPNRGDPIGS": {"units": "lin", "frequency": "q"},
    "DEXJPUS": {"units": "lin", "frequency": "d"},
}

READABLE_NAMES = {
    "JPNEPUINDXM": "EPU_JAP",
    "JPNPROINDAISMEI": "IP_JAP",
    "FPCPITOTLZGJPN": "INF_YoY_JAP",
    "LRUN64TTJPA156S": "UNEMP_JAP",
    "JPNRGDPNGS": "EX_JAP",
    "JPNRGDPIGS": "IM_JAP",
    "JPNRECDP": "RECESS_JAP",
    "JPNRGDPEXP": "GDP_JAP",
    "JPNRGDPC": "GDPC_JAP",
    "INTGSBJPM193N": "10YS_JAP",
    "DEXJPUS": "EXR_JAP",
}

# --- Functions ---
def fetch_fred_series(series_id, options):
    print(f"Fetching FRED: {series_id}")
    params = {
        "api_key": API_KEY,
        "file_type": "json",
        "series_id": series_id,
        "units": options["units"],
        "frequency": options["frequency"]
    }
    try:
        response = requests.get(FRED_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data["observations"])
        df["date"] = pd.to_datetime(df["date"])
        df[series_id] = pd.to_numeric(df["value"], errors="coerce")

        # Convert daily data to monthly
        if options["frequency"] == "d":
            df = df.resample("MS", on="date").mean(numeric_only=True).reset_index()

        # Always keep only the required columns
        df = df[["date", series_id]]

        return df
    except Exception as e:
        print(f"[FRED] Error fetching {series_id}: {e}")
        return None


def collect_japan_data():
    combined_df = None
    for series_id, options in FRED_SERIES.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            combined_df = df if combined_df is None else pd.merge(combined_df, df, on="date", how="outer")

    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)
        combined_df = combined_df.sort_values("date")

        # --- Add external inflation data ---
        if FILE_PATH and os.path.exists(FILE_PATH):
            print(f"Reading local inflation file: {FILE_PATH}")
            inflation_df = pd.read_csv(FILE_PATH, parse_dates=["date"])

            # Rename inflation column to match convention
            country_code = "JAP"  # update if dynamic
            inflation_col = [col for col in inflation_df.columns if col.lower() != "date"]
            if inflation_col:
                inflation_df.rename(columns={inflation_col[0]: f"INF_{country_code}"}, inplace=True)

            # Merge with renamed & sorted dataset
            combined_df = pd.merge(combined_df, inflation_df, on="date", how="outer")

    return combined_df

def save_to_csv(df, prefix="japan_combined_fred_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"../data/raw/{prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    return filename

def main():
    print("Starting Japan data collection...\n")
    df = collect_japan_data()

    if df is not None:
        filename = save_to_csv(df)
        print(df.tail(10))
        print(f"Total rows: {len(df)}")
        print(df.columns)
    else:
        print("\nNo data was collected.")

if __name__ == "__main__":
    main()
