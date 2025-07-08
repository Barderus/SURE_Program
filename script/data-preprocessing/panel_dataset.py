import pandas as pd

df = pd.read_csv("../../data/MERGE/master_file_merged.csv", parse_dates=["date"])

# Filter from 1995 onward
df = df[df["date"] >= "1995-01-01"]

# Melt wide to long format
value_vars = [col for col in df.columns if col != "date"]
long_df = df.melt(id_vars="date", value_vars=value_vars,
                  var_name="variable", value_name="value")

# Split variable and country suffix more safely
long_df["Country"] = long_df["variable"].str.extract(r'_(\w{3})$')
long_df["Variable"] = long_df["variable"].str.replace(r'_(\w{3})$', '', regex=True)


# Pivot to panel format: one row per (Country, date), columns = variables
panel_df = long_df.pivot_table(index=["Country", "date"],
                               columns="Variable", values="value").reset_index()

# Sort and format date
panel_df["date"] = pd.to_datetime(panel_df["date"]).dt.strftime("%Y-%m")
panel_df = panel_df.sort_values(["Country", "date"]).reset_index(drop=True)

# Save to Excel
output_path = "../../data/summary_tables/panel_dataset_country_col.xlsx"
panel_df.to_excel(output_path, index=False)
