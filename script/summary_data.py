import pandas as pd
import os

df = pd.read_excel("../data/summary_tables/panel_dataset_country_col.xlsx")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Drop 'date' column, but keep 'Country'
df_numeric = df.drop(columns=["date"])
# Output path
output_path = "../data/summary_tables/variable_summary.xlsx"

# Start writing Excel
with pd.ExcelWriter(output_path) as writer:
    for var in df_numeric.columns:
        if var == "Country":
            continue

        # Summary stats grouped by country
        grouped = df_numeric.groupby("Country")[var].describe(percentiles=[0.25, 0.5, 0.75])
        grouped = grouped.rename(columns={"50%": "median"})
        grouped["Variable"] = var
        grouped = grouped.reset_index()[["Country", "Variable", "count", "mean", "median", "std", "min", "25%", "75%", "max"]]

        # Save to a sheet with variable name
        sheet_name = var.strip()[:31]
        grouped.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Saved variable-wise summary to {output_path}")
