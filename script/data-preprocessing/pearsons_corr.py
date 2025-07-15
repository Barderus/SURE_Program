import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Load your dataset
df = pd.read_excel("../../data/summary_tables/panel_dataset_normalized - Copy.xlsx")

# Targets and exclusions
target_vars = ['RECESS', 'RECESS_OVER', 'RECESS_PERIOD']
excluded_cols = [
                    'Country', 'date', 'Country_CHI', 'Country_GER', 'Country_JAP',
                    'Country_MEX', 'Country_USA'
                ] + target_vars

# Numeric feature columns only
feature_cols = [col for col in df.select_dtypes(include='number').columns if col not in excluded_cols]

# Output path
output_path = "../../data/summary_tables/pearson_corr_sparse_by_country.xlsx"
sheets_written = 0

# Compute correlations safely, pair-by-pair
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    for country in df["Country"].unique():
        df_country = df[df["Country"] == country]
        rows = []

        for feature in feature_cols:
            for target in target_vars:
                x = df_country[feature]
                y = df_country[target]
                mask = x.notna() & y.notna()
                if mask.sum() < 10:
                    corr = np.nan
                else:
                    corr, _ = pearsonr(x[mask], y[mask])
                rows.append({"Feature": feature, "Target": target, "Correlation": corr})

        corr_df = pd.DataFrame(rows)

        if corr_df["Correlation"].notna().sum() > 0:
            # Sort by Target first, then descending correlation
            corr_df = corr_df.sort_values(by=["Target", "Correlation"], ascending=[True, False])

            # Save to Excel sheet
            corr_df.to_excel(writer, sheet_name=country[:31], index=False)

            sheets_written += 1

if sheets_written == 0:
    print("\nNo valid correlations could be calculated. Try relaxing the row threshold or inspecting missingness.")
else:
    print(f"\nSparse-safe Pearson correlation results saved to: {output_path}")
