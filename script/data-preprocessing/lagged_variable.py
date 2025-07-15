import pandas as pd
import re

def normalize_column(name):
    """
    Normalize column names:
    - Strip leading/trailing whitespace
    - Collapse multiple spaces
    - Remove extra spaces inside parentheses
    """
    name = re.sub(r"\s+", " ", name.strip())
    name = re.sub(r"\(\s+", "(", name)
    name = re.sub(r"\s+\)", ")", name)
    return name

def create_lagged_features(df, group_col, date_col, target_cols, lags):
    """
    Creates lagged features for target columns over specified periods,
    grouped by a grouping variable (e.g., country).
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values(by=[group_col, date_col], inplace=True)

    for col in target_cols:
        for lag in lags:
            lag_col = f"{col}_LAG{lag}"
            df[lag_col] = df.groupby(group_col)[col].shift(lag)

    return df

if __name__ == "__main__":
    input_path = "../../data/summary_tables/panel_dataset_feat_eng.xlsx"
    df = pd.read_excel(input_path)

    # Normalize column names
    df.columns = [normalize_column(col) for col in df.columns]

    # Select base variables to lag
    target_cols = [
        'CCI (Index)',
        'EPU (Index)',
        'EXR (TO USD)',
        'EX_M (Billions USD)',
        'IM_M (Billions USD)',
        'IP (Index)',
        'INF (%)',
        'UNEMP (%)',
        'YS (%)',
        'GDP (Billion USD)',
        'EX (Billions USD)',
        'IM (Billions USD)',
        'POP_15-64 (People)',
        'GDPC (USD)',
        'GDPG_OVER (%)',
        'GDPG_PERIOD (%)',
        'POP (People)',
        #'CPI (Index)',
        #'BCI (Index)',
        #'BCI_CENT (%)'
    ]

    # Define lag periods
    lags = [1, 3, 6, 12]

    # Generate lagged features
    df_with_lags = create_lagged_features(
        df,
        group_col="Country",
        date_col="date",
        target_cols=target_cols,
        lags=lags
    )

    # Clean unnamed and empty columns
    df_with_lags = df_with_lags.loc[:, ~df_with_lags.columns.str.contains("^Unnamed")]
    df_with_lags = df_with_lags.dropna(axis=1, how="all")

    # Save result
    output_path = "../../data/summary_tables/panel_dataset_feat_eng.xlsx"
    df_with_lags.to_excel(output_path, index=False)
    print(f"Saved: {output_path}")
