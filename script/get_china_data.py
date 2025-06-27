from datetime import datetime
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# FRED series configuration
FRED_SERIES = {
    "CHNPRINTO01IXPYM": {"units": "lin", "frequency": "m"},
    "INTDSRCNM193N": {"units": "lin", "frequency": "m"},
    "CHNCPIALLMINMEI": {"units": "lin", "frequency": "m"},
    "NXRXDCCNA": {"units": "lin", "frequency": "a"},
    "NMRXDCCNA": {"units": "lin", "frequency": "a"},
    "CHNRECDM": {"units": "lin", "frequency": "m"},
    "CHNGDPNQDSMEI": {"units": "lin", "frequency": "q"},
    "CCUSSP02CNM650N": {"units": "lin", "frequency": "m"},
}

# Human-readable column names
READABLE_NAMES = {
    "CHNPRINTO01IXPYM": "IP_CHI",
    "INTDSRCNM193N": "10YS_CHI",
    "CHNCPIALLMINMEI": "CPI_CHI",   # CPI previous month - current month / 100
    "NXRXDCCNA": "EX_CHI",
    "NMRXDCCNA": "IM_CHI",
    "CHNRECDM": "RECESS_CHI",
    "CHNGDPNQDSMEI": "GDP_CHI",
    "CCUSSP02CNM650N": "EXR_CHI",
}

MANUAL_DATA = {
    "../data/manual-data/EPU_CHI.csv",
    "../data/manual-data/2YS_CHI.csv",
    "../data/manual-data/UNEMP_CHI.csv",
    "../data/manual-data/EX_M_CHI.csv",
    "../data/manual-data/IM_M_CHI.csv",
    "../data/manual-data/GDPC_CHI.csv",
    "../data/manual-data/CCI_CHI.csv",
    "../data/manual-data/GDPG_CHI.csv",
    "../data/manual-data/POP_CHI.csv"
}

MILLION_TO_BILLION = {"NXRXDCCNA", "NMRXDCCNA", "CHNGDPNQDSMEI"}
# --- Functions ---

def fetch_fred_series(series_id, options):
    print(f"Fetching FRED series: {series_id}")
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

        # Convert from millions to billions
        if series_id in MILLION_TO_BILLION:
            df[series_id] /= 1_000

        return df[["date", series_id]]

    except Exception as e:
        print(f"[FRED] Error fetching {series_id}: {e}")
        return None


def main():
    print("Starting data collection...\n")
    combined_df = None

    # Fetch FRED data
    for series_id, options in FRED_SERIES.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            if combined_df is None:
                combined_df = df
            else:
                combined_df = pd.merge(combined_df, df, on="date", how="outer")

    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)

    # Save to CSV
    if combined_df is not None:
        combined_df = combined_df.sort_values("date")
        filename = f"../data/raw/china_combined_data_{datetime.now().strftime('%m-%d-%Y')}.csv"
        combined_df.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")
    else:
        print("\nNo data was collected or merged.")

# --- Entry Point ---

if __name__ == "__main__":
    main()
