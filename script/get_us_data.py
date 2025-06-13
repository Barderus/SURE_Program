import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

SERIES_LIST = {
    "USEPUINDXD": {"units": "lin", "frequency": "m"},
    "INDPRO": {"units": "lin", "frequency": "m"},
    "T10Y2Y": {"units": "lin", "frequency": "m"},
    "FPCPITOTLZGUSA": {"units": "lin", "frequency": "a"},
    "UNRATE": {"units": "lin", "frequency": "m"},
    "EXPGSC1": {"units": "lin", "frequency": "q"},
    "IMPGSC1":{"units": "lin", "frequency": "q"},
    "BOPGSTB": {"units": "lin", "frequency": "q"},
    "USARECDM": {"units": "lin", "frequency": "m"},
    "GDPC1": {"units": "lin", "frequency": "q"},
    "A939RX0Q048SBEA": {"units": "lin", "frequency": "q"},
    "UMCSENT": {"units": "lin", "frequency": "m"},
}

READABLE_NAMES = {
    "USEPUINDXD": "EPU_USA",
    "INDPRO": "IP_USA",
    "T10Y2Y": "YS_USA",
    "FPCPITOTLZGUSA": "INF_USA",
    "UNRATE": "UNEMP_USA",
    "EXPGSC1": "EX_USA",
    "IMPGSC1": "IM_USA",
    "USARECDM": "RECESS_USA",
    "GDPC1": "GDP_USA",
    "A939RX0Q048SBEA": "GDPC_USA",
    "UMCSENT": "CCI_USA",
}

# --- Functions ---
def fetch_fred_series(series_id, options):
    print(f"Fetching {series_id}...")
    params = {
        "api_key": API_KEY,
        "file_type": "json",
        "series_id": series_id,
        "units": options["units"],
        "frequency": options["frequency"]
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data["observations"])
        df["date"] = pd.to_datetime(df["date"])
        df[series_id] = pd.to_numeric(df["value"], errors="coerce")
        return df[["date", series_id]]
    except Exception as e:
        print(f"[FRED] Error fetching {series_id}: {e}")
        return None

def collect_us_data():
    combined_df = None
    for series_id, options in SERIES_LIST.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            combined_df = df if combined_df is None else pd.merge(combined_df, df, on="date", how="outer")

    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)
        combined_df = combined_df.sort_values("date")
    return combined_df

def save_to_csv(df, prefix="us_combined_fred_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"../data/raw/{prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    return filename

def main():
    print("Starting US FRED data collection...\n")
    df = collect_us_data()

    if df is not None:
        filename = save_to_csv(df)
        print(df.tail(10))
        print(f"Total rows: {len(df)}")
    else:
        print("\nNo data was collected.")

if __name__ == "__main__":
    main()
