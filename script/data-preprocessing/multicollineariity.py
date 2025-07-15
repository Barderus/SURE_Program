import pandas as pd
import numpy as np
from statsmodels.tools.tools import add_constant
from statsmodels.api import OLS

# Load your dataset
df = pd.read_excel("../../data/summary_tables/panel_dataset_feat_eng.xlsx")

# Columns to exclude (non-features or dummies)
excluded_cols = [
    'Country', 'date', 'RECESS', 'RECESS_PERIOD', 'RECESS_OVER',
    'Country_CHI', 'Country_GER', 'Country_JAP', 'Country_MEX', 'Country_USA'
]

# Get numeric feature columns
numeric_cols = [col for col in df.select_dtypes(include='number').columns if col not in excluded_cols]

# Function to compute VIF per country
def compute_vif_country(df_country, min_non_missing=0.50):
    valid_features = df_country[numeric_cols].columns[
        df_country[numeric_cols].notna().mean() >= min_non_missing
        ].tolist()

    df_clean = df_country[valid_features].dropna()

    if df_clean.shape[0] < 10 or len(valid_features) < 2:
        return pd.DataFrame(columns=["Feature", "VIF"])

    X = add_constant(df_clean)
    vif_data = []
    for i in range(X.shape[1]):
        try:
            vif = 1 / (1 - OLS(X.iloc[:, i], X.drop(X.columns[i], axis=1)).fit().rsquared)
        except Exception:
            vif = np.nan
        vif_data.append((X.columns[i], vif))

    return pd.DataFrame(vif_data, columns=["Feature", "VIF"])

# Output file paths
output_all = "../../data/summary_tables/vif_all_features_by_country.xlsx"
output_filtered = "../../data/summary_tables/vif_filtered_under10_by_country.xlsx"
output_filtered_panel = "../../data/summary_tables/VIF_panel_dataset.xlsx"

# Accumulator for all filtered results and valid feature names
filtered_all_countries = []
selected_features_set = set()

# Console display and file output
with pd.ExcelWriter(output_all, engine='openpyxl') as writer_all:
    for country in df["Country"].unique():
        print(f"\n====== VIF for {country} ======")
        vif_df = compute_vif_country(df[df["Country"] == country])
        if vif_df.empty:
            print("Not enough data for VIF calculation.")
            continue

        vif_sorted = vif_df.sort_values(by="VIF", ascending=True)
        print(vif_sorted.to_string(index=False))

        # Save full results to individual country sheet
        vif_sorted.to_excel(writer_all, sheet_name=country[:31], index=False)

        # Filter and format for combined output
        vif_filtered = vif_sorted[vif_sorted["VIF"] < 10].copy()
        if not vif_filtered.empty:
            vif_filtered.insert(0, "Country", country)
            vif_filtered.insert(2, "Value", np.nan)
            vif_filtered["VIF_dup"] = vif_filtered["VIF"]
            vif_filtered = vif_filtered[["Country", "Feature", "Value", "VIF", "VIF_dup"]]
            filtered_all_countries.append(vif_filtered)

            # Track selected features (excluding constant term)
            selected_features_set.update(vif_filtered["Feature"].unique())

# Save all filtered VIF results to a single worksheet
if filtered_all_countries:
    df_filtered_combined = pd.concat(filtered_all_countries, ignore_index=True)
    df_filtered_combined.to_excel(output_filtered, sheet_name="Filtered_VIF_Under10", index=False)
    print(f"\nFiltered VIFs (< 10) saved to: {output_filtered}")
else:
    print("\nNo VIFs under 10 found. No filtered file created.")

# Create and save the filtered panel dataset
# Include always the identifying + target columns
essential_cols = ['Country', 'date', 'RECESS', 'RECESS_PERIOD', 'RECESS_OVER']
# Add the selected VIF-safe features
final_selected_cols = essential_cols + sorted(list(selected_features_set - {'const'}))  # remove 'const' if present

if selected_features_set:
    df_filtered_panel = df[final_selected_cols]
    df_filtered_panel.to_excel(output_filtered_panel, index=False)
    print(f"\nFiltered panel dataset saved to: {output_filtered_panel}")
else:
    print("\nNo features passed VIF filtering. No panel dataset created.")
