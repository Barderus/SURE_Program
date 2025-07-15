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

def compute_moving_averages(df, group_col, date_col, target_cols, windows):
    """
    Computes simple moving averages for target columns over specified window sizes.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values(by=[group_col, date_col], inplace=True)

    for col in target_cols:
        for window in windows:
            ma_col = f"{col}_MA{window}"
            df[ma_col] = df.groupby(group_col)[col].transform(lambda x: x.rolling(window).mean())

    return df

if __name__ == "__main__":
    input_path = "../../data/summary_tables/panel_dataset_feat_eng.xlsx"
    df = pd.read_excel(input_path)

    # Normalize all column names (Remove white space, etc.)
    df.columns = [normalize_column(col) for col in df.columns]

    # Define variables to apply moving averages
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
        #'EX (Billions USD)',
        #'IM (Billions USD)',
        'POP_15-64 (People)',
        #'GDPC (USD)',
        #'GDPG_OVER (%)',
        #'GDPG_PERIOD (%)',
        #'POP (People)',
    ]

    # Compute 12-month moving averages
    df_with_ma = compute_moving_averages(
        df,
        group_col="Country",
        date_col="date",
        target_cols=target_cols,
        windows=[12]
    )

    # Drop unnamed columns and fully empty columns
    df_with_ma = df_with_ma.loc[:, ~df_with_ma.columns.str.contains("^Unnamed")]

# Save result
    output_path = "../../data/summary_tables/panel_dataset_feat_eng.xlsx"
    df_with_ma.to_excel(output_path, index=False)
    print(f"Saved: {output_path}")
    print(df_with_ma.columns)
