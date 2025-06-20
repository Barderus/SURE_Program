import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# --- Configuration ---

load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
WB_EXCHANGE_INDICATOR = "PA.NUS.FCRF"  # Official exchange rate (LCU per USD)
FILE_PATH = "../data/raw/inflation/Germany_Inflation_Data.csv"


FRED_SERIES = {
    "DEEPUINDXM": {"units": "lin", "frequency": "m"},
    "DEUPROINDMISMEI": {"units": "lin", "frequency": "a"},
    "FPCPITOTLZGDEU": {"units": "lin", "frequency": "a"},
    "LRUPTTTTDEQ156S": {"units": "lin", "frequency": "q"},
    "NMRSAXDCDEQ": {"units": "lin", "frequency": "q"},
    "DEUEXPORTQDSNAQ": {"units": "lin", "frequency": "q"},
    "DEURECD": {"units": "lin", "frequency": "m"},
    "CLVMNACSCAB1GQDE": {"units": "lin", "frequency": "q"},
    "DEURGDPC": {"units": "lin", "frequency": "a"},
    "INTGSBDEM193N": {"units": "lin", "frequency": "m"},
}

READABLE_NAMES = {
    "DEEPUINDXM": "EPU_GER",
    "DEUPROINDMISMEI": "IP_GER",
    "FPCPITOTLZGDEU": "INF_YoY_GER",
    "LRUPTTTTDEQ156S": "UNEMP_GER",
    "NMRSAXDCDEQ": "IM_GER",
    "DEUEXPORTQDSNAQ": "EX_GER",
    "DEURECD": "RECESS_GER",
    "CLVMNACSCAB1GQDE": "GDP_GER",      # Unites are in millions, need to transform to billions
    "DEURGDPC": "GDPC_GER",
    "INTGSBDEM193N": "10YS_GER",
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

        # Convert GDP from millions to billions
        if series_id == "CLVMNACSCAB1GQDE":
            df[series_id] = df[series_id] / 100

        return df[["date", series_id]]
    except Exception as e:
        print(f"[FRED] Error fetching {series_id}: {e}")
        return None

def fetch_worldbank_exchange_rate():
    print("Fetching World Bank: Exchange Rate (PA.NUS.FCRF)")
    url = "https://api.worldbank.org/v2/country/DE/indicator/PA.NUS.FCRF?format=json&per_page=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[1]
        df = pd.DataFrame([
            {"year": item["date"], "EXR_GER": item["value"]}
            for item in data if item["value"] is not None
        ])
        df["date"] = pd.to_datetime(df["year"], format="%Y").dt.to_period("Y").dt.to_timestamp()
        return df.drop(columns="year")
    except Exception as e:
        print(f"[World Bank] Error fetching exchange rate: {e}")
        return None

def collect_germany_data():
    combined_df = None

    # FRED data
    for series_id, options in FRED_SERIES.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            combined_df = df if combined_df is None else pd.merge(combined_df, df, on="date", how="outer")

    # Rename columns
    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)

    # World Bank: Exchange rate
    wb_df = fetch_worldbank_exchange_rate()
    if wb_df is not None:
        combined_df = pd.merge(combined_df, wb_df, on="date", how="outer")

    # Add local inflation file
    if combined_df is not None:
        if FILE_PATH and os.path.exists(FILE_PATH):
            print(f"Reading local inflation file: {FILE_PATH}")
            inflation_df = pd.read_csv(FILE_PATH, parse_dates=["date"])

            # Rename inflation column to match expected name
            country_code = "GER"
            inflation_col = [col for col in inflation_df.columns if col.lower() != "date"]
            if inflation_col:
                inflation_df.rename(columns={inflation_col[0]: f"INF_{country_code}"}, inplace=True)

            combined_df = pd.merge(combined_df, inflation_df, on="date", how="outer")

        combined_df = combined_df.sort_values("date")

    return combined_df


def save_to_csv(df, prefix="germany_combined_fred_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"../data/raw/{prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    return filename

def main():
    print("Starting Germany data collection...\n")
    df = collect_germany_data()

    if df is not None:
        filename = save_to_csv(df)
        print(df.tail(10))
        print(f"Total rows: {len(df)}")
        print(df.columns)
    else:
        print("\nNo data was collected.")

if __name__ == "__main__":
    main()
