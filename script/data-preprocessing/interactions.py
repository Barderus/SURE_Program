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

def create_interaction_terms(df):
    """
    Creates economic interaction terms between selected variables.
    """
    required_cols = ['EPU (Index)', 'YS (%)', 'CCI (Index)', 'UNEMP (%)']

    # Confirm columns exist
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Create interactions
    df['EPU_YS'] = df['EPU (Index)'] * df['YS (%)']
    df['EPU_CCI'] = df['EPU (Index)'] * df['CCI (Index)']
    df['YS_CCI'] = df['YS (%)'] * df['CCI (Index)']
    df['EPU_UNEMP'] = df['EPU (Index)'] * df['UNEMP (%)']

    return df

if __name__ == "__main__":
    input_path = "../../data/summary_tables/panel_dataset_feat_eng.xlsx"
    df = pd.read_excel(input_path)

    # Normalize columns
    df.columns = [normalize_column(col) for col in df.columns]

    # Create interaction terms
    df_with_interactions = create_interaction_terms(df)

    # Clean unnamed/empty columns
    df_with_interactions = df_with_interactions.loc[:, ~df_with_interactions.columns.str.contains("^Unnamed")]

    # Save result
    output_path = "../../data/summary_tables/panel_dataset_feat_eng.xlsx"
    df_with_interactions.to_excel(output_path, index=False)
    print(f"Saved: {output_path}")
