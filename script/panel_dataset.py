import pandas as pd

# Assume df is already merged and cleaned
df = pd.read_csv("../data/processed/master_file_1995_onward.csv.", parse_dates=["date"])

print(df.columns)
# Keep only columns with country suffixes and 'date'
id_vars = ["date"]
value_vars = [col for col in df.columns if col != "date"]

# Melt wide to long
long_df = df.melt(id_vars="date", value_vars=value_vars, var_name="variable", value_name="value")

# Extract country and variable name
# Handles EX_M_USA → Variable: EX_M, Country: USA
long_df["Country"] = long_df["variable"].str.extract(r'_([A-Z]{3})$')
long_df["Variable"] = long_df["variable"].str.replace(r'_([A-Z]{3})$', '', regex=True)


# Pivot back to wide by country-date
panel_df = long_df.pivot_table(index=["Country", "date"], columns="Variable", values="value").reset_index()

# Optional: sort
panel_df = panel_df.sort_values(["Country", "date"]).reset_index(drop=True)
panel_df["date"] = pd.to_datetime(panel_df["date"]).dt.strftime("%Y-%m")

# Save
panel_df.to_excel("../data/summary_tables/panel_dataset_country_col.xlsx", index=False)
