import pandas as pd

file_path = "../data/summary_tables/GDP_BASED_RECESSION.xlsx"
xls = pd.ExcelFile(file_path)
df = xls.parse('Sheet1')

# Ensure date is datetime and data is sorted
df['date'] = pd.to_datetime(df['date'])
df.sort_values(by=['Country', 'date'], inplace=True)

# Function to compute recession indicator
def compute_recession_indicator(group, column_name, indicator_name):
    gdp_growth = group[column_name].reset_index(drop=True)
    indicator = [0] * len(gdp_growth)

    for i in range(1, len(gdp_growth)):
        if pd.notna(gdp_growth[i]) and pd.notna(gdp_growth[i-1]):
            if gdp_growth[i] < 0 and gdp_growth[i-1] < 0:
                indicator[i] = 1
                indicator[i-1] = 1

    group[indicator_name] = indicator
    return group

# Apply the rule to both GDP growth columns
df = (
    df.groupby('Country', group_keys=False)
    .apply(lambda g: compute_recession_indicator(g, 'GDPG_PERIOD (%)', 'recess_ind_period'))
    .groupby('Country', group_keys=False)
    .apply(lambda g: compute_recession_indicator(g, 'GDPG_OVER (%)', 'recess_ind_over'))
)
#Save the result
df.to_excel("../data/summary_tables/GDP_Recession_Flagged.xlsx", index=False)
