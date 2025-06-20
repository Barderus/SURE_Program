from datetime import datetime
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# --- Setup ---
load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
FILE_PATH = "../data/raw/inflation/Mexico_Inflation_Data.csv"

# --- FRED Series ---
FRED_SERIES = {
    "WUIMEX": {"units": "lin", "frequency": "q"},
    "MEXPRINTO02IXOBSAM": {"units": "lin", "frequency": "m"},
    "FPCPITOTLZGMEX": {"units": "lin", "frequency": "a"},
    "NGDPRSAXDCMXQ": {"units": "lin", "frequency": "q"},
    "IRLTST01MXM156N": {"units": "lin", "frequency": "m"},
    "INTGSBMXM193N": {"units": "lin", "frequency": "m"},
    "FXRATEMXA618NUPN": {"units": "lin", "frequency": "a"},
    "LRHUTTTTMXM156S": {"units": "lin", "frequency": "m"},
    "NYGDPPCAPKDMEX": {"units": "lin", "frequency": "a"},
    "NMRSAXDCMXQ":{"units": "lin", "frequency": "q"},
    "NXRSAXDCMXQ":{"units": "lin", "frequency": "q"},
    "MEXRECD": {"units": "lin", "frequency": "d"}, # Convert to monthly
}

# --- Readable Names ---
READABLE_NAMES = {
    "WUIMEX": "EPU_MEX",
    "MEXPRINTO02IXOBSAM": "IP_MEX",
    "FPCPITOTLZGMEX": "INF_YoY_MEX",
    "NGDPRSAXDCMXQ": "GDP_MEX",     # In Millions, need to convert to Billions
    "INTGSBMXM193N": "1OYS_MEX",
    "IRLTST01MXM156N": "2YS_MEX",
    "FXRATEMXA618NUPN": "EXR_MEX",
    "NMRSAXDCMXQ": "IM_MEX",
    "NXRSAXDCMXQ":"EX_MEX",
    "LRHUTTTTMXM156S": "UNEMP_MEX",
    "NYGDPPCAPKDMEX": "GDPC_MEX",
    "MEXRECD": "RECESS_MEX"
}

# --- World Bank Series ---
WORLD_BANK_SERIES = {
    #"SL.UEM.TOTL.ZS": "UNEMP_MEX+",
    #"NY.GDP.PCAP.CD": "GDPC_MEX+"
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

        # Convert millions to billions for specific GDP series
        if series_id in ["CLVMNACSCAB1GQDE", "NGDPRSAXDCMXQ"]:
            df[series_id] = df[series_id] / 1000

        # Convert daily data to monthly
        if options["frequency"] == "d":
            df = df.resample("MS", on="date").mean(numeric_only=True).reset_index()

        # Always keep only the required columns
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

    # FRED data
    for series_id, options in FRED_SERIES.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            combined_df = df if combined_df is None else pd.merge(combined_df, df, on="date", how="outer")

    # Rename columns
    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)

        # Add local inflation file
        if FILE_PATH and os.path.exists(FILE_PATH):
            print(f"Reading local inflation file: {FILE_PATH}")
            inflation_df = pd.read_csv(FILE_PATH, parse_dates=["date"])

            # Rename inflation column to match expected name
            country_code = "MEX"
            inflation_col = [col for col in inflation_df.columns if col.lower() != "date"]
            if inflation_col:
                inflation_df.rename(columns={inflation_col[0]: f"INF_{country_code}"}, inplace=True)

            combined_df = pd.merge(combined_df, inflation_df, on="date", how="outer")

        # Sort final output
        combined_df = combined_df.sort_values("date")

    return combined_df


"""
# --- Merge World Bank data ---
def merge_world_bank_data(df):
    for wb_series, readable_name in WORLD_BANK_SERIES.items():
        wb_df = fetch_world_bank_series(wb_series, "MX")
        if wb_df is not None:
            df = pd.merge(df, wb_df.rename(columns={wb_series: readable_name}), on="date", how="outer")
    return df
"""
# --- Save ---
def save_to_csv(df, prefix="mexico_combined_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"../data/raw/{prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    return filename

def main():
    print("Starting Mexico data collection...\n")
    df = collect_mexico_data()
    if df is not None:
        #df = merge_world_bank_data(df)
        filename = save_to_csv(df)
        print(df.tail(10))
        print(f"Total rows: {len(df)}")
        print(df.columns)
    else:
        print("\nNo FRED data was collected.")

if __name__ == "__main__":
    main()
