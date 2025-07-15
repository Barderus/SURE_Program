import pandas as pd
import numpy as np
from statsmodels.tools.tools import add_constant
from statsmodels.api import OLS

# Load your dataset
df = pd.read_excel("../../data/summary_tables/panel_dataset_normalized - Copy.xlsx")

# Columns to include
included_cols = [
    "EPU (Index)", "EPU_CCI", "YS (%)", "YS_CCI", "GDP (Billion USD)",
    "IM_M (Billions USD)", "EX_M (Billions USD)", "IP (Index)",
    "CCI (Index)", "UNEMP (%)", "EXR (TO USD)", "EPU_YS", "INF (%)", "EPU_UNEMP"
]

# Keep only numeric and available columns
numeric_cols = [col for col in included_cols if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]

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

# Loop over countries
for country in df["Country"].unique():
    print(f"\n====== VIF for {country} ======")
    vif_df = compute_vif_country(df[df["Country"] == country])
    if vif_df.empty:
        print("Not enough data for VIF calculation.")
    else:
        print(vif_df.sort_values(by="VIF", ascending=False).to_string(index=False))

# Output file
output_path = "../../data/summary_tables/vif_selected_features_by_country.xlsx"

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    for country in df["Country"].unique():
        vif_df = compute_vif_country(df[df["Country"] == country])
        if vif_df.empty:
            continue
        vif_df.sort_values(by="VIF", ascending=True).to_excel(writer, sheet_name=country[:31], index=False)

print(f"VIF results saved to: {output_path}")