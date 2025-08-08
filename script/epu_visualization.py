import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = "US_Policy_Uncertainty_Data (1).xlsx"
df = pd.read_excel(file_path)

# Clean the data
df = df.dropna(subset=["Month", "EPU"])
df["Year"] = df["Year"].astype(int)
df["Month"] = df["Month"].astype(int)

# Create datetime column
df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))

# Filter to include data from 1995 onward
df_filtered = df[df["Year"] >= 1995]

# Plot the filtered EPU Index
plt.figure(figsize=(12, 6))
plt.plot(df_filtered["Date"], df_filtered["EPU"], label="US EPU Index (1995+)", color="tab:red")
plt.title("US Economic Policy Uncertainty (EPU) Since 1995")
plt.xlabel("Date")
plt.ylabel("EPU Index")
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.show()
