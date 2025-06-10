import pandas as pd

# Load the full combined dataset
file = "../data/yield_data_full.csv"
df = pd.read_csv(file, parse_dates=True, index_col=0)
df.index.name = "date"

# Updated dictionary with column names
yield_pairs = {
    "US": ("US_10Y", "US_2Y"),
    "Canada": ("Canada_10Y", "Canada_2Y"),
    "Germany": ("Germany_10Y", "Germany_2Y"),
    "Mexico": ("Mexico_10Y", "Mexico_2Y"),
    "China": ("China_10Y", "China_2Y"),
    "Japan": ("Japan_10Y", "Japan_2Y")  #
}

# Resample to monthly averages to align mixed frequencies
df_monthly = df.resample("ME").mean()

# Compute 10Y - 2Y spreads
spread_df = pd.DataFrame(index=df_monthly.index)

for country, (y10, y2) in yield_pairs.items():
    if y10 in df_monthly.columns and y2 in df_monthly.columns:
        spread_df[f"{country}_Spread"] = df_monthly[y10] - df_monthly[y2]

output_file = "../data/yield_spreads_by_country_monthly.csv"
spread_df.to_csv(output_file)
print(f"Saved {output_file}")
print(spread_df.dropna(how='all').head())
