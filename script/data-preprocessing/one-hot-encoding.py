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

def encode_country_dummies(df, country_col='Country', baseline='CAN'):
    """
    Performs one-hot encoding for Country, using 'baseline' as the reference (dropped) category.
    """
    dummies = pd.get_dummies(df[country_col], prefix='Country')
    dummy_col_to_drop = f"Country_{baseline}"

    if dummy_col_to_drop in dummies.columns:
        dummies = dummies.drop(columns=['Country_CAN'])
        dummies = dummies.astype(int)
    else:
        raise ValueError(f"Baseline '{baseline}' not found in country column.")

    return pd.concat([df, dummies], axis=1)

if __name__ == "__main__":
    input_path = "../../data/summary_tables/panel_dataset_country_col.xlsx"
    df = pd.read_excel(input_path)

    # Normalize column names
    df.columns = [normalize_column(col) for col in df.columns]

    # Add country dummies, using Canada as baseline
    df_encoded = encode_country_dummies(df, country_col='Country', baseline='CAN')

    # Clean unnamed/empty columns
    df_encoded = df_encoded.loc[:, ~df_encoded.columns.str.contains("^Unnamed")]

    # Save final output
    output_path = "../../data/summary_tables/panel_dataset_feat_eng.xlsx"
    df_encoded.to_excel(output_path, index=False)
    print(f"Saved: {output_path}")
