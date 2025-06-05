import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("FRED_API_KEY")


base_url = "https://api.stlouisfed.org/fred/"

series_list = {
    "GDP": {"units": "lin", "frequency": "q"},                     # Nominal Gross Domestic Product
    "GDPC1": {"units": "lin", "frequency": "q"},                   # Real Gross Domestic Product (chained 2012 dollars)
    "A939RX0Q048SBEA": {"units": "lin", "frequency": "q"},         # Real GDP per capita
    "NGDPSAXDCUSQ": {"units": "lin", "frequency": "q"},            # Nominal GDP (national currency, quarterly)
    "GDI": {"units": "lin", "frequency": "q"},                     # Gross Domestic Income
    "NETEXP": {"units": "lin", "frequency": "q"},                  # Net Exports of Goods and Services
    "NETEXC": {"units": "lin", "frequency": "q"},                  # Real Net Exports of Goods and Services
    "EXPGS": {"units": "lin", "frequency": "q"},                   # Exports of Goods and Services
    "B230RC0Q173SBEA": {"units": "lin", "frequency": "q"},         # Population
    "W068RCQ027SBEA": {"units": "lin", "frequency": "q"},          # Government Total Expenditures
    "IMPGS": {"units": "lin", "frequency": "q"},                   # Imports of Goods and Services
    "GCE": {"units": "lin", "frequency": "q"},                     # Government Consumption Expenditures & Investment
    "W790RC1Q027SBEA": {"units": "lin", "frequency": "q"},         # Net Domestic Investment: Private, Domestic Business
    "W987RC1Q027SBEA": {"units": "lin", "frequency": "q"},         # Gross Private Domestic Investment: Domestic Business
    "FGEXPND": {"units": "lin", "frequency": "q"},                 # Federal Government Current Expenditures
    "GCEC1": {"units": "lin", "frequency": "q"},                   # Real Government Consumption Expenditures & Investment
    "M2V": {"units": "lin", "frequency": "q"},                     # Velocity of M2 Money Stock
    "FEDFUNDS": {"units": "lin", "frequency": "q"}                 # Federal Funds Effective Rate (converted to quarterly)
}


combined_df = None

for series_id, options in series_list.items():
    params = {
        "api_key": api_key,
        "file_type": "json",
        "series_id": series_id,
        "units": options["units"],
        "frequency": options["frequency"]
    }

    response = requests.get(base_url + "series/observations", params=params)

    # If status = ok, request the data
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["observations"])
        df["date"] = pd.to_datetime(df["date"])
        df[series_id] = pd.to_numeric(df["value"], errors="coerce")
        df = df[["date", series_id]]

        # Combine the dfs in a single df
        if combined_df is None:
            combined_df = df
        else:
            combined_df = pd.merge(combined_df, df, on="date", how="outer")
    else:
        print(f"Failed to retrieve data for {series_id}: {response.status_code}")

# Sort by date and save
combined_df = combined_df.sort_values("date")
combined_df.to_csv("us_combined_fred_data.csv", index=False)
print("Saved combined data to combined_fred_data.csv")

print(combined_df.tail(10))
print(len(combined_df))