## Weekly  Update

This week, I explored our dataset more thoroughly. I began by reviewing all available variables to ensure their relevance, and removed those that were not immediately useful.

Next, I focused on aligning the starting date periods across all countries. After reviewing each variable individually, I decided to keep only the data from **1995 onward**. This allows us to maximize coverage across countries while minimizing data loss.

I prepared and shared the following key files with the team:
- `country_aligned_timeseries.csv`: aligned time series by country
- `panel_dataset.csv`: long-format panel data for analysis
- `data_summary.csv`: descriptive statistics including count, min, max, mean, and quantiles

Once the data was standardized across countries (e.g., unit consistency), I began generating **correlation matrices** and **heatmaps** to support future analytical work and identify early relationships between variables.