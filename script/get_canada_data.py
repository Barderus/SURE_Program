import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# --- Configuration ---

load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
WB_CANADA_UNEMPLOYMENT = "SL.UEM.TOTL.ZS"

FRED_SERIES = {
    "CANEPUINDXM": {"units": "lin", "frequency": "m"},
    "CANPROINDMISMEI": {"units": "lin", "frequency": "m"},
    "IRLTLT01CAQ156N": {"units": "lin", "frequency": "q"},
    "FPCPITOTLZGCAN": {"units": "lin", "frequency": "a"},
    "NXRSAXDCCAQ": {"units": "lin", "frequency": "q"},
    "NMRSAXDCCAQ": {"units": "lin", "frequency": "q"},
    "CANRECDM": {"units": "lin", "frequency": "m"},
    "NGDPRSAXDCCAQ": {"units": "lin", "frequency": "q"},
    "CANRGDPC": {"units": "lin", "frequency": "a"},
    #"INTGSBCAM193N": {"units": "lin", "frequency": "m"},
    "DEXCAUS": {"units": "lin", "frequency": "d"}, # Convert to monthly
    "CSCICP03CAM665S": {"units": "lin", "frequency": "m"},
}

READABLE_NAMES = {
    "CANEPUINDXM": "EPU_CAN",
    "CANPROINDMISMEI": "IP_CAN",
    "IRLTLT01CAQ156N": "10YS_CAN",
    "FPCPITOTLZGCAN": "INF_CAN",
    "NXRSAXDCCAQ": "EX_CAN",
    "NMRSAXDCCAQ": "IM_CAN",
    "CANRECDM": "RECESS_CAN",
    "NGDPRSAXDCCAQ": "GDP_CAN",
    "CANRGDPC": "GDPC_CAN",
    #"INTGSBCAM193N": "GBR_CAN",
    "DEXCAUS": "EXR_CAN",
    "CSCICP03CAM665S": "CCI_CAN"
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

        df = df[["date", series_id]]

        return df
    except Exception as e:
        print(f"[FRED] Error fetching {series_id}: {e}")
        return None


def fetch_worldbank_unemployment():
    print("Fetching World Bank: Canada Unemployment Rate")
    url = f"https://api.worldbank.org/v2/country/CA/indicator/{WB_CANADA_UNEMPLOYMENT}?format=json&per_page=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[1]
        df = pd.DataFrame([
            {"year": item["date"], "UNEMP_CAN": item["value"]}
            for item in data if item["value"] is not None
        ])
        df["date"] = pd.to_datetime(df["year"], format="%Y").dt.to_period("Y").dt.to_timestamp()
        return df.drop(columns="year")
    except Exception as e:
        print(f"[World Bank] Error fetching unemployment: {e}")
        return None


def collect_canada_data():
    combined_df = None

    # FRED data
    for series_id, options in FRED_SERIES.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            combined_df = df if combined_df is None else pd.merge(combined_df, df, on="date", how="outer")

    # Rename columns
    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)

    # World Bank: Unemployment
    wb_df = fetch_worldbank_unemployment()
    if wb_df is not None:
        combined_df = pd.merge(combined_df, wb_df, on="date", how="outer")

    if combined_df is not None:
        combined_df = combined_df.sort_values("date")
    return combined_df

def save_to_csv(df, prefix="canada_combined_fred_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"../data/raw/{prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    return filename

def main():
    print("Starting Canada data collection...\n")
    df = collect_canada_data()

    if df is not None:
        filename = save_to_csv(df)
        print(df.tail(10))
        print(f"Total rows: {len(df)}")
    else:
        print("\nNo data was collected.")

if __name__ == "__main__":
    main()
