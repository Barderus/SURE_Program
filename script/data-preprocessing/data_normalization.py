import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load your dataset
df = pd.read_excel("../../data/summary_tables/VIF_panel_dataset.xlsx")

# Ensure 'date' column is in YYYY-MM format
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.to_period('M').astype(str)

# Select numeric columns to normalize
columns_to_exclude = ['date', "RECESS", "RECESS_PERIOD", "RECESS_OVER",
                      "Country_CHI", "Country_GER", "Country_JAP", "Country_MEX", "Country_USA"]

numeric_cols = [col for col in df.select_dtypes(include='number').columns if col not in columns_to_exclude]

# Normalize numeric columns
scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Save the normalized dataset
df.to_excel("../../data/summary_tables/panel_dataset_normalized.xlsx", index=False)

print("Saved normalized dataset to 'panel_dataset_normalized.xlsx'")
