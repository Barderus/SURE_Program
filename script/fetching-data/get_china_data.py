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
    "../data/manual-data/2YS_CHI_C.csv",
    "../data/manual-data/UNEMP_CHI.csv",
    "../data/manual-data/EX_IM_CHI.csv",
    "../data/manual-data/GDPC_CHI.csv",
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

        # Convert date to YYYY-MM string format
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m")

        # Convert values to numeric
        df[series_id] = pd.to_numeric(df["value"], errors="coerce")

        # Convert from millions to billions if needed
        if series_id in MILLION_TO_BILLION:
            df[series_id] /= 1_000

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

            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime("%Y-%m")
            else:
                print(f"[Warning] No 'date' column in {path}")
                continue

            value_cols = [col for col in df.columns if col.lower() != "date"]
            if value_cols:
                df.rename(columns={col: col.upper() for col in value_cols}, inplace=True)
                cleaned_df = df[["date"] + [col.upper() for col in value_cols]]
                manual_dfs.append(cleaned_df)
            else:
                print(f"[Warning] No value column found in {path}")
        else:
            print(f"[Warning] File not found: {path}")

    # Save all manual data into a single CSV file
    if manual_dfs:
        combined_manual = pd.concat(manual_dfs).drop_duplicates().sort_values("date")
        combined_manual.to_csv("../data/combined_data/CHI_manual_data.csv", index=False)
    else:
        print("[Error] No manual data loaded.")

    return manual_dfs  # So your for-loop in main() still works

def main():
    print("Starting data collection...\n")
    combined_df = None

    # Fetch FRED data
    for series_id, options in FRED_SERIES.items():
        df = fetch_fred_series(series_id, options)
        if df is not None:
            combined_df = df if combined_df is None else pd.merge(combined_df, df, on="date", how="outer")

    if combined_df is not None:
        combined_df.rename(columns=READABLE_NAMES, inplace=True)

        # Merge manual data
        for manual_df in load_manual_data():
            # Ensure date is datetime for merge compatibility
            manual_df["date"] = pd.to_datetime(manual_df["date"], errors="coerce")
            combined_df["date"] = pd.to_datetime(combined_df["date"], errors="coerce")
            #combined_df = pd.merge(combined_df, manual_df, on="date", how="outer")

        combined_df = combined_df.sort_values("date")

        # Save to CSV
        filename = f"../data/combined_data/china_combined_data_{datetime.now().strftime('%m-%d-%Y')}.csv"
        combined_df.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")
        print(combined_df.tail(10))
        print(f"Total rows: {len(combined_df)}")
        print(combined_df.columns)
    else:
        print("\nNo data was collected or merged.")


if __name__ == "__main__":
    main()
