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

FRED_SERIES = {
    "DEEPUINDXM": {"units": "lin", "frequency": "m"},
    "A018ADDEA338NNBR": {"units": "lin", "frequency": "a"},
    "FPCPITOTLZGDEU": {"units": "lin", "frequency": "a"},
    "LRUPTTTTDEQ156S": {"units": "lin", "frequency": "q"},
    "DEUIMPORTQDSNAQ": {"units": "lin", "frequency": "q"},
    "DEUEXPORTQDSNAQ": {"units": "lin", "frequency": "q"},
    "DEURECD": {"units": "lin", "frequency": "m"},
    "CLVMNACSCAB1GQDE": {"units": "lin", "frequency": "q"},
    "DEURGDPC": {"units": "lin", "frequency": "a"},
    "INTDSRDEM193N": {"units": "lin", "frequency": "m"},
    "INTGSTDEM193N": {"units": "lin", "frequency": "m"},
    "INTGSBDEM193N": {"units": "lin", "frequency": "m"},
    "XRNCUSDEA618NRUG": {"units": "lin", "frequency": "a"},
    # Placeholder: Consumer Confidence Index
}

READABLE_NAMES = {
    "DEEPUINDXM": "Germany_EPU_Index",
    "A018ADDEA338NNBR": "Industrial_Production",
    "FPCPITOTLZGDEU": "CPI_Inflation",
    "LRUPTTTTDEQ156S": "Unemployment_Rate",
    "DEUIMPORTQDSNAQ": "Imports",
    "DEUEXPORTQDSNAQ": "Exports",
    "DEURECD": "Recession_Indicator",
    "CLVMNACSCAB1GQDE": "Real_GDP",
    "DEURGDPC": "Real_GDP_Per_Capita",
    "INTDSRDEM193N": "Discount_Rate",
    "INTGSTDEM193N": "T_Bills",
    "INTGSBDEM193N": "Gov_Bonds",
    "XRNCUSDEA618NRUG": "Exchange_Rate_FRED",
    # Placeholder: Consumer Confidence Index
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
            {"year": item["date"], "Exchange_Rate_WB": item["value"]}
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

    if combined_df is not None:
        combined_df = combined_df.sort_values("date")
    return combined_df

def save_to_csv(df, prefix="germany_combined_fred_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"{prefix}_{timestamp}.csv"
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
    else:
        print("\nNo data was collected.")

if __name__ == "__main__":
    main()
