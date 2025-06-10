#  Progress Summary

##  Countries included
- Canada
- China
- Germany
- Japan
- Mexico
- US
##  What’s been done

## Fetching data
- Created scripts to fetch macroeconomic indicators for a specific country and outputs a time-indexed .csv file.
  - `get_canada_data.py`
  - `get_china_data.py`
  - `get_germany_data.py`
  - `get_japan_data.py`
  - `get_us_data.py`
  - `get_mexico_data.py`


## Main data sources:
  - [FRED](https://fred.stlouisfed.org/) – Federal Reserve Economic Data
  - [OECD](https://data.oecd.org/) – Organisation for Economic Co-operation and Development
  - [World Bank](https://data.worldbank.org/)
  - [Bank of Canada Valet API](https://www.bankofcanada.ca/valet/)
  - [People’s Bank of China](http://www.pbc.gov.cn/)
  - [Bank of Japan](https://www.boj.or.jp/en/statistics/)
  - [TradingEconomics API](https://developer.tradingeconomics.com/)

- Other files
  - calculate_yield_spread.py loads the 2-year and 10-year government bond yields and calculate the yield spread (10Y - 2Y)
  - merge_rename.py loads all the necessary .csv files and merge them on the date column using outer joins.
    - Also applies a consistent column naming scheme to avoid any conflicts.

## Final output file
  - The final output file `merged_cleaned.csv` contains all the macroeconomic indicators for the requested countries.
## Next steps
- Run some EDA and look at trends over time  
- Build visualizations  
- Start feature engineering for modeling later on