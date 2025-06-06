from datetime import datetime
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# --- Setup ---
load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# --- FRED Series ---
FRED_SERIES = {
    "WUIMEX": {"units": "lin", "frequency": "q"},
    "MEXPRINTO02IXOBSAM": {"units": "lin", "frequency": "m"},
    "FPCPITOTLZGMEX": {"units": "lin", "frequency": "a"},
    "XTEXVA01MXQ188S": {"units": "lin", "frequency": "q"},
    "NGDPRSAXDCMXQ": {"units": "lin", "frequency": "q"},
    "INTDSRMXM193N": {"units": "lin", "frequency": "m"},
    "INTGSTMXM193N": {"units": "lin", "frequency": "m"},
    "INTGSBMXM193N": {"units": "lin", "frequency": "m"},
    "FXRATEMXA618NUPN": {"units": "lin", "frequency": "a"},
    "XRNCUSMXA618NRUG": {"units": "lin", "frequency": "a"},
    # Placeholder: Consumer Confidence Index
}

# --- Readable Names ---
READABLE_NAMES = {
    "WUIMEX": "World_Uncertainty_Index",
    "MEXPRINTO02IXOBSAM": "Industrial_Production",
    "FPCPITOTLZGMEX": "Inflation",
    "XTEXVA01MXQ188S": "Exports_Value",
    "NGDPRSAXDCMXQ": "Real_GDP",
    "INTDSRMXM193N": "Discount_Rate",
    "INTGSTMXM193N": "Treasury_Bills_Rate",
    "INTGSBMXM193N": "Gov_Bonds_Rate",
    "FXRATEMXA618NUPN": "Exchange_Rate_USD",
    "XRNCUSMXA618NRUG": "Market_Exchange_Rate"
    # Placeholder: Consumer Confidence Index
}

# --- World Bank Series ---
WORLD_BANK_SERIES = {
    "SL.UEM.TOTL.ZS": "Unemployment_Rate",
    "NY.GDP.PCAP.CD": "GDP_Per_Capita"
}

# --- Fetch FRED Series ---
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

# --- Fetch World Bank Series ---
def fetch_world_bank_series(series_id, country_code):
    print(f"Fetching World Bank: {series_id}")
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{series_id}?format=json&per_page=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        if len(json_data) < 2 or not isinstance(json_data[1], list):
            print(f"[World Bank] No data returned for {series_id}")
            return None
        records = json_data[1]
        df = pd.DataFrame([
            {"date": pd.to_datetime(entry["date"]), series_id: entry["value"]}
            for entry in records if entry["value"] is not None
        ])
        return df.sort_values("date")
    except Exception as e:
        print(f"[World Bank] Error fetching {series_id}: {e}")
        return None

# --- Combine FRED data ---
def collect_mexico_data():
    combined_df = None
    for series_id, options in FRED_SERIES.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            combined_df = df if combined_df is None else pd.merge(combined_df, df, on="date", how="outer")
    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)
        combined_df = combined_df.sort_values("date")
    return combined_df

# --- Merge World Bank data ---
def merge_world_bank_data(df):
    for wb_series, readable_name in WORLD_BANK_SERIES.items():
        wb_df = fetch_world_bank_series(wb_series, "MX")
        if wb_df is not None:
            df = pd.merge(df, wb_df.rename(columns={wb_series: readable_name}), on="date", how="outer")
    return df

# --- Save ---
def save_to_csv(df, prefix="mexico_combined_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"{prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    return filename

# --- Main ---
def main():
    print("Starting Mexico data collection...\n")
    df = collect_mexico_data()
    if df is not None:
        df = merge_world_bank_data(df)
        filename = save_to_csv(df)
        print(df.tail(10))
        print(f"Total rows: {len(df)}")
    else:
        print("\nNo FRED data was collected.")

if __name__ == "__main__":
    main()
