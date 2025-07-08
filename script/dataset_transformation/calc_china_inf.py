import pandas as pd

# Load the downloaded CPI data from FRED
# Make sure your CSV file is named correctly or adjust the path
df = pd.read_csv("../../data/CHNCPIALLMINMEI.csv")

# Rename columns for clarity
df.columns = ["date", "CPI_Index"]

# Convert date column to datetime format
df["date"] = pd.to_datetime(df["date"])

# Convert CPI values to numeric, handling missing values
df["CPI_Index"] = pd.to_numeric(df["CPI_Index"], errors="coerce")

# Sort by date in case it's not ordered
df = df.sort_values("date")

# Calculate Year-over-Year (YoY) Inflation %
df["YoY_Inflation"] = df["CPI_Index"].pct_change(periods=12) * 100

# Calculate Month-over-Month (MoM) Inflation %
df["MoM_Inflation"] = df["CPI_Index"].pct_change(periods=1) * 100

# Drop rows where inflation can't be calculated
df = df.dropna(subset=["YoY_Inflation", "MoM_Inflation"])

# Save to a new CSV if needed
df.to_csv("china_inflation_rates.csv", index=False)

# Preview the result
print(df.tail())
