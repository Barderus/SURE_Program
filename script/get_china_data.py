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
    "CHIEPUINDXM": {"units": "lin", "frequency": "m"},
    "CHNPRINTO01IXPYM": {"units": "lin", "frequency": "m"},
    "FPCPITOTLZGCHN": {"units": "lin", "frequency": "a"},
    "NMRXDCCNA": {"units": "lin", "frequency": "a"},
    "NXRXDCCNA": {"units": "lin", "frequency": "a"},
    "CHNXTNTVA01STSAQ": {"units": "lin", "frequency": "q"},
    "CHNRECDM": {"units": "lin", "frequency": "m"},
    #"NGDPRXDCCNA": {"units": "lin", "frequency": "a"},
    "INTDSRCNM193N": {"units": "lin", "frequency": "m"},
    "CCUSSP02CNM650N": {"units": "lin", "frequency": "m"},
}

# Human-readable column names
READABLE_NAMES = {
    "CHIEPUINDXM": "EPU_CHI",
    "CHNPRINTO01IXPYM": "IP_CHI",
    "FPCPITOTLZGCHN": "INF_CHI",
    "NMRXDCCNA": "IM_CHI",
    "NXRXDCCNA": "EX_CHI",
    "CHNXTNTVA01STSAQ": "TB_CHI",
    "CHNRECDM": "RECESS_CHI",
    #"NGDPRXDCCNA": "GDP_CHI",
    "INTDSRCNM193N": "10YS_CHI",
    "CCUSSP02CNM650N": "EXR_CHI",
}

# World Bank series configuration
WORLD_BANK_SERIES = {
    "SL.UEM.TOTL.ZS": "UNEMP_CHI",
    "NY.GDP.PCAP.CD": "GDPC_CHI",
    "NY.GDP.MKTP.KD": "GDP_CHI"
}

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
        return df[["date", series_id]]
    except Exception as e:
        print(f"[FRED] Error fetching {series_id}: {e}")
        return None

def fetch_worldbank_series(indicator, column_name):
    print(f"Fetching World Bank series: {indicator}")
    url = f"https://api.worldbank.org/v2/country/CN/indicator/{indicator}?format=json&per_page=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[1]
        df = pd.DataFrame([
            {"year": item["date"], column_name: item["value"]}
            for item in data if item["value"] is not None
        ])

        # Scale GDP to billions if needed
        if indicator == "NY.GDP.MKTP.KD":
            df[column_name] = df[column_name] / 1e9  # Convert to billions

        df["date"] = pd.to_datetime(df["year"], format="%Y")
        df["date"] = df["date"].dt.to_period("Y")
        df["date"] = df["date"].dt.to_timestamp()

        return df.drop(columns="year")
    except Exception as e:
        print(f"[World Bank] Error fetching {indicator}: {e}")
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

    # Fetch World Bank data
    for indicator, col_name in WORLD_BANK_SERIES.items():
        wb_df = fetch_worldbank_series(indicator, col_name)
        if wb_df is not None and combined_df is not None:
            combined_df = pd.merge(combined_df, wb_df, on="date", how="outer")
        elif wb_df is not None:
            combined_df = wb_df

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
