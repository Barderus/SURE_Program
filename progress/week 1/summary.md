#  Progress Summary

##  What’s been done

- Went through the FRED website and found the relevant `series_id` for each country.
- Used the FRED API to fetch time series data like GDP, inflation, interest rates, industrial production, and exchange rates.
- Pulled in World Bank data where needed (mainly for unemployment rates and GDP per capita).
- Saved each country’s data as a timestamped CSV inside `data/raw/`.
- Merged everything by date into one master CSV file inside `data/processed/

##  Countries included

- Canada  
- China  
- Germany  
- Japan  
- Mexico  
- US 

## Next steps

- Gather Consumer Confidence Index
- Run some EDA and look at trends over time  
- Build visualizations  
- Start feature engineering for modeling later on