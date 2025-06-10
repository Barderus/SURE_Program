import os
import pandas as pd
import requests
import tradingeconomics as te
from dotenv import load_dotenv
import yfinance as yf


# Load API keys from .env
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")
TE_API_KEY = os.getenv("TE_API_KEY")

# Login to TradingEconomics
te.login(TE_API_KEY)

# ---------- FRED 10Y Yield Series ----------
fred_series = {
    "US_10Y": "DGS10",
    "Canada_10Y": "IRLTLT01CAM156N",
    "Germany_10Y": "IRLTLT01DEM156N",
    "Japan_10Y": "IRLTLT01JPM156N",
    "Mexico_10Y": "IRLTLT01MXM156N",
    "US_2Y": "DGS2"
}

def fetch_fred(label, series_id, start="1990-01-01"):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if "observations" not in data:
        raise ValueError(f"No data for {label} ({series_id})")
    df = pd.DataFrame(data["observations"])
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.set_index("date")["value"].rename(label)

# ---------- TradingEconomics 2Y Yield (Mexico only) ----------
def fetch_te_2y_http(label, symbol):
    url = f"https://api.tradingeconomics.com/markets/historical/{symbol}"
    params = {
        "c": TE_API_KEY,
        "d1": "1990-01-01",
        "format": "json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if not data or "Close" not in data[0]:
        raise ValueError(f"No usable data for {label}")
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date")["Close"].rename(label)

# ---------- Canada 2Y from Bank of Canada ----------
def fetch_canada_2y():
    url = "https://www.bankofcanada.ca/valet/observations/V122538/json"
    response = requests.get(url)
    data = response.json()
    obs = data["observations"]
    rows = [(pd.to_datetime(x["d"]), float(x["V122538"]["v"])) for x in obs if "v" in x["V122538"]]
    df = pd.DataFrame(rows, columns=["date", "value"]).set_index("date")
    return df["value"].rename("Canada_2Y")

# ---------- Germany 2Y from ECB ----------
def fetch_germany_2y():
    url = "https://sdw.ecb.europa.eu/quickviewexport.do?SERIES_KEY=FM.M.U2.EUR.4F.BB.U2_2Y.YLD&fileType=csv"
    df = pd.read_csv(url, skiprows=5)
    df = df[df["OBS_VALUE"] != "."]
    df["TIME_PERIOD"] = pd.to_datetime(df["TIME_PERIOD"])
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"])
    return df.set_index("TIME_PERIOD")["OBS_VALUE"].rename("Germany_2Y")

def fetch_china_yield_yf(label, symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(start="1990-01-01")
    series = hist["Close"].rename(label)
    series.index = pd.to_datetime(series.index)
    return series

china2 = fetch_china_yield_yf("China_2Y", "^CNY2Y")
china10 = fetch_china_yield_yf("China_10Y", "^CNY10Y")



# ---------- Japan 2Y ----------
def fetch_japan_2y_yf():
    ticker = yf.Ticker("^JPTY2Y")  # Yahoo Finance symbol for Japan 2Y yield
    hist = ticker.history(start="1990-01-01")
    series = hist["Close"].rename("Japan_2Y")
    series.index = pd.to_datetime(series.index)
    return series


# ---------- Main Collection ----------
series = []

# Fetch FRED data
for label, sid in fred_series.items():
    try:
        print(f"Fetching FRED: {label}")
        series.append(fetch_fred(label, sid))
    except Exception as e:
        print(f"FRED error for {label}: {e}")

# Fetch TE Mexico 2Y
try:
    print("Fetching TE: Mexico_2Y")
    series.append(fetch_te_2y_http("Mexico_2Y", "MEX:government-bond-2-year-yield"))
except Exception as e:
    print(f"TE error for Mexico_2Y: {e}")

# Fetch Canada 2Y
try:
    print("Fetching Bank of Canada: Canada_2Y")
    series.append(fetch_canada_2y())
except Exception as e:
    print(f"Canada 2Y error: {e}")

# Fetch Germany 2Y
try:
    print("Fetching ECB: Germany_2Y")
    series.append(fetch_germany_2y())
except Exception as e:
    print(f"Germany 2Y error: {e}")

# ---------- Combine and Save ----------
df_all = pd.concat(series, axis=1).sort_index()

output_path = "../data/yield_data_full.csv"
df_all.to_csv(output_path)
print(f"Saved to {output_path}")
print(df_all.tail())
print(df_all.columns)
