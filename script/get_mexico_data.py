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
    #"INTGSBMXM193N": {"units": "lin", "frequency": "m"},
    #"IRLTST01MXM156N": {"units": "lin", "frequency": "m"},
    "LRHUTTTTMXM156S": {"units": "lin", "frequency": "m"},
    "NXRSAXDCMXQ": {"units": "lin", "frequency": "q"},
    "XTIMVA01MXM667S":{"units": "lin", "frequency": "m"},
    "NMRSAXDCMXQ": {"units": "lin", "frequency": "q"},
    "MEXRECDM": {"units": "lin", "frequency": "d"}, # Convert to monthly
    "NGDPRSAXDCMXQ": {"units": "lin", "frequency": "q"},
    "CSCICP02MXM460S": {"units": "lin", "frequency": "m"},
    "DEXMXUS": {"units": "lin", "frequency": "d"},
    "LFWA64TTMXQ647N": {"units": "lin", "frequency": "q"},
    "MEXPRINTO02IXOBSAM": {"units": "lin", "frequency": "m"},
}

# --- Readable Names ---
READABLE_NAMES = {
    #"INTGSBMXM193N": "1OYS_MEX",
    #"IRLTST01MXM156N": "2YS_MEX",
    "LRHUTTTTMXM156S": "UNEMP_MEX",
    "XTEXVA01MXM667S":"EX_M_MEX",
    "NXRSAXDCMXQ": "EX_MEX",
    "XTIMVA01MXM667S": "IM_M_MEX",
    "NMRSAXDCMXQ": "IM_MEX",
    "MEXRECDM": "RECESS_MEX",
    "NGDPRSAXDCMXQ": "GDP_MEX",     # In Millions, need to convert to Billions
    "CSCICP02MXM460S": "CCI_MEX",
    "DEXMXUS": "EXR_MEX",
    "LFWA64TTMXQ647N": "POP_15-64_MEX",
    "MEXPRINTO02IXOBSAM": "IP_MEX"
}

MANUAL_DATA = {
    "../data/manual-data/INF_MEX.csv",
    "../data/manual-data/EPU_MEX.csv",
    "../data/manual-data/IP_MEX.csv",
}

MILLION_TO_BILLION = {"NGDPRSAXDCMXQ"}
TO_BILLIONS = {"XTIMVA01MXM667S", "XTEXVA01MXM667S"}
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

        # Convert from billions to millions
        if series_id in MILLION_TO_BILLION:
            df[series_id] /= 1_000

        if series_id in TO_BILLIONS:
            df[series_id] /= 1_000_000_000

        # Convert daily data to monthly
        if options["frequency"] == "d":
            df = df.resample("MS", on="date").mean(numeric_only=True).reset_index()

        return df[["date", series_id]]
    except Exception as e:
        print(f"[FRED] Error fetching {series_id}: {e}")
        return None

def load_manual_data():
    manual_dfs = []
    for path in MANUAL_DATA:
        if os.path.exists(path):
            print(f"Reading manual file: {path}")
            df = pd.read_csv(path)

            # Ensure date is properly parsed
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
            else:
                print(f"[Warning] No 'date' column in {path}")
                continue

            # Rename value column
            value_cols = [col for col in df.columns if col.lower() != "date"]
            if value_cols:
                value_col = value_cols[0]
                df.rename(columns={value_col: value_col.upper()}, inplace=True)
                manual_dfs.append(df[["date", value_col.upper()]])
            else:
                print(f"[Warning] No value column found in {path}")
        else:
            print(f"[Warning] File not found: {path}")
    return manual_dfs


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

        # Load and merge manual datasets
        for manual_df in load_manual_data():
            combined_df = pd.merge(combined_df, manual_df, on="date", how="outer")


        # Sort final output
        combined_df = combined_df.sort_values("date")

    return combined_df

# --- Save ---
def save_to_csv(df, prefix="mexico_combined_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"../data/combined_data/{prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    return filename

def main():
    print("Starting Mexico data collection...\n")
    df = collect_mexico_data()
    if df is not None:
        df.drop(columns=["INFLATION"], inplace=True)
        #filename = save_to_csv(df)
        print(df.tail(10))
        print(f"Total rows: {len(df)}")
        print(df.columns)
    else:
        print("\nNo FRED data was collected.")

if __name__ == "__main__":
    main()
