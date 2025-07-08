import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

from script.get_mexico_data import MILLION_TO_BILLION, MANUAL_DATA

# --- Configuration ---

load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
WB_CANADA_UNEMPLOYMENT = "SL.UEM.TOTL.ZS"
FILE_PATH = "../data/raw/inflation/Canada_Inflation_Data.csv"


FRED_SERIES = {
    "IRLTLT01CAQ156N": {"units": "lin", "frequency": "q"},
    "LRUNTTTTCAM156S": {"units":"lin", "frequency":"m"},
    "XTEXVA01CAM667S": {"units": "lin", "frequency": "m"},
    "NXRSAXDCCAQ": {"units":"lin", "frequency":"q"},
    "XTIMVA01CAM667S": {"units": "lin", "frequency": "m"},
    "NMRSAXDCCAQ": {"units":"lin", "frequency":"q"},
    "DEXCAUS": {"units": "lin", "frequency": "d"}, # Convert to monthly
    "LFWA64TTCAM647S": {"units": "lin", "frequency": "m"},
    "CANRECDM": {"units": "lin", "frequency": "m"},
}

READABLE_NAMES = {
    "IRLTLT01CAQ156N": "10YS_CAN",
    "LRUNTTTTCAM156S": "UNEMP_CAN",
    "XTEXVA01CAM667S": "EX_M_CAN",
    "NXRSAXDCCAQ": "EX_CAN",
    "XTIMVA01CAM667S": "IM_M_CAN",
    "NMRSAXDCCAQ": "IM_CAN",
    "DEXCAUS": "EXR_CAN",
    "LFWA64TTCAM647S": "POP_15-64_CAN",
    "CANRECDM": "RECESS_CAN",
}

MANUAL_DATA = {
    "../data/manual-data/INF_CAN.csv",
    "../data/manual-data/GDP_CAN.csv",
    "../data/manual-data/GDP_Q_CAN.csv",
    "../data/manual-data/GDPC_CAN.csv",
}

MILLION_TO_BILLION = {""}

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

        RAW_TO_BILLION = ["XTEXVA01CAM667S", "XTIMVA01CAM667S"]

        # Convert values based on series_id
        if series_id in MILLION_TO_BILLION:
            df[series_id] /= 1_000  # from millions to billions

        elif series_id in RAW_TO_BILLION:
            df[series_id] /= 1_000_000_000  # from raw to billions

        df = df[["date", series_id]]

        return df
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


def collect_canada_data():
    combined_df = None

    # FRED data
    for series_id, options in FRED_SERIES.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            combined_df = df if combined_df is None else pd.merge(combined_df, df, on="date", how="outer")

    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)

        # Add local inflation file
        if FILE_PATH and os.path.exists(FILE_PATH):
            print(f"Reading local inflation file: {FILE_PATH}")
            inflation_df = pd.read_csv(FILE_PATH, parse_dates=["date"])

            # Rename inflation column to match expected name
            country_code = "CAN"
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
def save_to_csv(df, prefix="canada_combined_fred_data"):
    timestamp = datetime.now().strftime("%m-%d-%Y")
    filename = f"../data/combined_data/{prefix}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")
    return filename

def main():
    print("Starting Canada data collection...\n")
    df = collect_canada_data()

    if df is not None:
        df.drop(columns=["INFLATION"], inplace=True)
        filename = save_to_csv(df)
        print(df.tail(10))
        print(f"Total rows: {len(df)}")
        print(df.columns)
    else:
        print("\nNo FRED data was collected.")

if __name__ == "__main__":
    main()
