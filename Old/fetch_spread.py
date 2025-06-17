import os
import pandas as pd
import requests
from dotenv import load_dotenv


# Load API keys from .env
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

fred_series = {
    "10YS_CAN": "IRLTLT01CAM156N",
    "10YS_GER": "IRLTLT01DEM156N",
    "10Y_JAP": "IRLTLT01JPM156N",
    "10YS_MEX": "IRLTLT01MXM156N",
    "2YS_MEX": "IRLTST01MXM156N"
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
    return df[["date", "value"]].rename(columns={"value": label})

# ---------- Canada 2Y from Bank of Canada ----------
def fetch_canada_2y():
    url = "https://www.bankofcanada.ca/valet/observations/V122538/json"
    response = requests.get(url)
    data = response.json()
    obs = data["observations"]
    rows = [(pd.to_datetime(x["d"]), float(x["V122538"]["v"])) for x in obs if "v" in x["V122538"]]
    return pd.DataFrame(rows, columns=["date", "2YS_CAN"])

# ---------- Germany 2Y from ECB (local CSV) ----------
def fetch_germany_2y():
    file_path = "../data/raw/spread/Germany-2Y.csv"
    df = pd.read_csv(file_path)
    df = df[df["price"] != "."]
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = pd.to_numeric(df["price"])
    return df.rename(columns={"price": "2YS_GER"})[["date", "2YS_GER"]]

def fetch_germany_YS():
    file_path = "../data/raw/spread/GER_YS.csv"
    df = pd.read_csv(file_path)
    df = df[df["price"] != "."]
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = pd.to_numeric(df["price"])
    return df.rename(columns={"price": "YS_GER"})[["date", "YS_GER"]]

# ---------- China from local CSV ----------
def fetch_china_yield():
    df_2y = pd.read_csv("../data/raw/spread/China-2Y.csv", parse_dates=["date"])
    df_10y = pd.read_csv("../data/raw/spread/China-10YS.csv", parse_dates=["date"])
    df_2y = df_2y[["date", "price"]].rename(columns={"price": "2YS_CHI"})
    df_10y = df_10y[["date", "price"]].rename(columns={"price": "10YS_CHI"})
    return pd.merge(df_2y, df_10y, on="date", how="outer").sort_values("date")

# ---------- Japan from local CSV ----------
def fetch_japan_yield():
    df = pd.read_csv("../data/raw/spread/Japan-2Y.csv")
    df = df[df["price"] != "."]
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = pd.to_numeric(df["price"])
    return df.rename(columns={"price": "2YS_JAP"})[["date", "2YS_JAP"]]

# ---------- Main Fetch and Save ----------
def save_country_csv(country, df):
    path = f"../data/raw/{country}_yields.csv"
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

# Canada
can_10y = fetch_fred("10YS_CAN", fred_series["10YS_CAN"])
can_2y = fetch_canada_2y()
can_df = pd.merge(can_10y, can_2y, on="date", how="outer")
save_country_csv("CAN", can_df)

# Germany
ger_10y = fetch_fred("10YS_GER", fred_series["10YS_GER"])
ger_2y = fetch_germany_2y()
ger_ys = fetch_germany_YS()

# Ensure 'date' column is monthly
ger_10y["date"] = pd.to_datetime(ger_10y["date"]).dt.to_period("M").dt.to_timestamp()
ger_2y["date"] = pd.to_datetime(ger_2y["date"]).dt.to_period("M").dt.to_timestamp()
ger_ys["date"] = pd.to_datetime(ger_ys["date"]).dt.to_period("M").dt.to_timestamp()

# Rename for consistency
ger_10y = ger_10y.rename(columns={"value": "10YS_GER"})
ger_2y = ger_2y.rename(columns={"value": "2YS_GER"})
ger_ys = ger_ys.rename(columns={"value":"YS_GER"})

# Merge on monthly date
ger_df = pd.merge(ger_10y, ger_2y, on="date", how="outer").sort_values("date")

# Save to CSV
save_country_csv("GER", ger_ys)

# Mexico
mex_10y = fetch_fred("10YS_MEX", fred_series["10YS_MEX"])
mex_2y = fetch_fred("2YS_MEX", fred_series["2YS_MEX"])
mex_df = pd.merge(mex_10y, mex_2y, on="date", how="outer")
save_country_csv("MEX", mex_df)

# China
china_df = fetch_china_yield()
save_country_csv("CHI", china_df)

# Japan
jap_10y = fetch_fred("10YS_JAP", fred_series["10Y_JAP"])
jap_2y = fetch_japan_yield()
jap_df = pd.merge(jap_10y, jap_2y, on="date", how="outer")
save_country_csv("JAP", jap_df)