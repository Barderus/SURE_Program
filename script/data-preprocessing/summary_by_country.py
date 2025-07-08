import pandas as pd
import os

df = pd.read_excel("../data/summary_tables/panel_dataset_country_col.xlsx")

# Drop unnamed/empty columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
output_dir = "../../data/summary_tables/"

os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "country_summary_tables.xlsx")

# Write each country's summary to a different sheet
with pd.ExcelWriter(output_path) as writer:
    countries = df["Country"].unique()
    for country in countries:
        country_df = df[df["Country"] == country].drop(columns=["Country", "date"])
        desc = country_df.describe(percentiles=[0.25, 0.5, 0.75]).round(2)
        desc.to_excel(writer, sheet_name=country[:31])
        print(f"Added {country} to worksheet")

print(f"ll summaries saved to {output_path}")
