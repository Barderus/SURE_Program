import os
import logging
import pandas as pd
import requests
import tradingeconomics as te
from dotenv import load_dotenv
import urllib3

# --- Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")
TE_API_KEY = os.getenv("TE_API_KEY")

if not FRED_API_KEY or not TE_API_KEY:
    logging.warning("API keys for FRED or TradingEconomics not found in .env file.")
else:
    te.login(TE_API_KEY)


# --- Fetching Functions ---

def fetch_fred(label: str, series_id: str, start: str = "1990-01-01") -> pd.Series | None:
    logging.info(f"Fetching FRED: {label} ({series_id})")
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "observations" not in data or not data["observations"]:
            logging.warning(f"No observations data for {label}")
            return None
        df = pd.DataFrame(data["observations"])
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        return df.set_index("date")["value"].rename(label)
    except Exception as e:
        logging.error(f"Error fetching FRED {label}: {e}")
        return None

def fetch_te_http(label: str, symbol: str, start: str = "1990-01-01") -> pd.Series | None:
    logging.info(f"Fetching TE: {label} ({symbol})")
    url = f"https://api.tradingeconomics.com/markets/historical/{symbol}"
    params = {"c": TE_API_KEY, "d1": start, "format": "json"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data or "Close" not in data[0]:
            logging.warning(f"No usable data for {label} from TE.")
            return None
        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])
        return df.set_index("Date")["Close"].rename(label)
    except Exception as e:
        logging.error(f"Error fetching TE {label}: {e}")
        return None

def fetch_canada_2y() -> pd.Series | None:
    logging.info("Fetching Bank of Canada: Canada_2Y")
    url = "https://www.bankofcanada.ca/valet/observations/V122538/json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        obs = data["observations"]
        rows = [(pd.to_datetime(x["d"]), float(x["V122538"]["v"])) for x in obs if "v" in x.get("V122538", {})]
        if not rows:
            logging.warning("No observations found for Canada 2Y.")
            return None
        df = pd.DataFrame(rows, columns=["date", "value"]).set_index("date")
        return df["value"].rename("Canada_2Y")
    except Exception as e:
        logging.error(f"Error fetching Canada_2Y: {e}")
        return None


# --- Main Logic ---

def main():
    logging.info("Starting yield data collection process.")

    data_sources = [
        {"function": fetch_fred, "params": {"label": "US_10Y", "series_id": "DGS10"}},
        {"function": fetch_fred, "params": {"label": "US_2Y", "series_id": "DGS2"}},
        {"function": fetch_fred, "params": {"label": "Canada_10Y", "series_id": "IRLTLT01CAM156N"}},
        {"function": fetch_fred, "params": {"label": "Germany_10Y", "series_id": "IRLTLT01DEM156N"}},
        {"function": fetch_fred, "params": {"label": "Japan_10Y", "series_id": "IRLTLT01JPM156N"}},
        {"function": fetch_fred, "params": {"label": "Mexico_10Y", "series_id": "IRLTLT01MXM156N"}},
        {"function": fetch_te_http, "params": {"label": "Mexico_2Y", "symbol": "GMXN2YR"}},
        {"function": fetch_canada_2y, "params": {}},
    ]

    all_series = []
    for source in data_sources:
        try:
            series = source["function"](**source["params"])
            label = source["params"].get("label", "Canada_2Y")
            if series is not None:
                all_series.append(series)
            else:
                logging.warning(f"No data returned for {label}.")
        except Exception as e:
            logging.error(f"Critical error for {source['params']}: {e}")

    if not all_series:
        logging.error("No data collected. Exiting.")
        return

    logging.info("Combining all data series.")
    df_all = pd.concat(all_series, axis=1).sort_index()

    # --- Merge External 2Y Spread CSVs ---
    spread_dir = "../data/"
    spread_files = {
        'China_2Y': os.path.join(spread_dir, 'China-2Y.csv'),
        'Japan_2Y': os.path.join(spread_dir, 'Japan-2Y.csv'),
        'Germany_2Y': os.path.join(spread_dir, 'Germany-2y.csv')
    }

    for label, path in spread_files.items():
        if os.path.exists(path):
            try:
                df_spread = pd.read_csv(path)
                df_spread["date"] = pd.to_datetime(df_spread["date"])
                df_spread.set_index("date", inplace=True)
                df_spread.rename(columns={"price": label}, inplace=True)
                df_spread = df_spread[[label]]
                df_all = pd.merge(df_all, df_spread, left_index=True, right_index=True, how="left")
                logging.info(f"Merged spread file: {label}")
            except Exception as e:
                logging.error(f"Error merging {label} from {path}: {e}")
        else:
            logging.warning(f"Spread file not found: {path}")

    df_all = df_all.ffill()

    # --- Output ---
    output_path = "../data/yield_data_full.csv"
    df_all.to_csv(output_path)
    logging.info(f"Data saved to {output_path}")

    print("\n--- Data Collection Summary ---")
    print("Columns collected:")
    print(df_all.columns.tolist())
    print("\nLatest 5 rows:")
    print(df_all.tail())
    print("-----------------------------\n")


if __name__ == "__main__":
    main()
