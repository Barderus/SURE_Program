# Required Macroeconomics variables per country

## Main indicators for the US:
| Description                                                                                 | Series ID                 | READABLE_NAMES Entry         | Short Code Suggestion | Source              |
|---------------------------------------------------------------------------------------------|----------------------------|------------------------------|------------------------|---------------------|
| Economic Policy Uncertainty Index for the United States                                     | `USEPUINDXD`              | `US_EPU_Index`               | `EPU_USA`              | FRED                |
| Industrial Production: Total Index                                                          | `INDPRO`                  | `Industrial_Production`      | `IP_USA`               | FRED                |
| 10Y - 2Y Treasury Yield Spread**                                                            | `T10Y2Y`                  | `Yield_Spread`               | `YS_USA`               | FRED                |
| Consumer Price Inflation                                                                    | `FPCPITOTLZGUSA`          | `Inflation`                  | `INF_USA`              | FRED                |
| Unemployment Rate                                                                           | `UNRATE`                  | `Unemployment_Rate`          | `UNEMP_USA`            | FRED                |
| Real Net Exports of Goods and Services                                                      | `NETEXC`                  | `Real_Net_Exports`           | `EX_USA`               | FRED                |
| Trade Balance (Goods and Services)                                                          | `BOPGSTB`                 | `Trade_Balance`              | `TB_USA`               | FRED                |
| Recession Indicators *(DISCONTINUED)*                                                       | `USARECDM`                | `Recession_Indicator`        | `RECESS_USA`           | FRED                |
| Real Gross Domestic Product                                                                 | `GDPC1`                   | `Real_GDP`                   | `GDP_USA`              | FRED                |
| Real GDP per capita                                                                         | `A939RX0Q048SBEA`         | `Real_GDP_Per_Capita`        | `GDPC_USA`             | FRED                |
| Federal Funds Effective Rate                                                                | `FEDFUNDS`                | `Federal_Funds_Rate`         | `FFR_USA`              | FRED                |
| Consumer Confidence Index                                                                   | `CSCICP03.USA.M`          | *(custom - via OECD API)*    | `CCI_USA`              | OECD                |

Link sources:
- Consumer confidence index: `https://db.nomics.world/OECD/MEI_CLI/CSCICP03.USA.M?tab=chart`
---

## Main indicators for Japan:

| Description                                          | Series ID                   | READABLE_NAMES Entry         | Short Code Suggestion | Source               |
|------------------------------------------------------|------------------------------|------------------------------|------------------------|----------------------|
| Economic Policy Uncertainty Index for Japan          | `JPNEPUINDXM`               | `Japan_EPU_Index`            | `EPU_JAP`              | FRED                 |
| Industrial Production (Excl. Construction) for Japan | `JPNPROINDAISMEI`           | `Industrial_Production`      | `IP_JAP`               | FRED                 |
| 10-Year Government Bond Yield                        | `INTGSBJPM193N`             | `10Y_Bond_Yield`             | `10YS_JAP`             | FRED                 |
| 2-Year Government Bond Yield                         | *(MOF Japan Website)*       | *(custom)*                   | `2YS_JAP`              | MOF Japan            |
| 10Y - 2Y Yield Spread                                | *(calculated)*              | `yield_spread`               | `YS_JAP`               | Calculated           |
| Inflation, consumer prices (annual %)                | `FPCPITOTLZGJPN`            | `Inflation`                  | `INF_JAP`              | FRED                 |
| Unemployment Rate (Ages 15 to 64) for Japan          | `LRUN64TTJPA156S`           | `Unemployment_Rate`          | `UNEMP_JAP`            | FRED                 |
| Real Net Exports of Goods and Services               | `JPNRGDPNGS`                | `Real_Net_Exports`           | `EX_JAP`               | FRED                 |
| OECD-based Recession Indicators *(DISCONTINUED)*     | `JPNRECDP`                  | `Recession_Indicator`        | `RECESS_JAP`           | FRED                 |
| Real Gross Domestic Product for Japan                | `JPNRGDPEXP`                | `Real_GDP`                   | `GDP_JAP`              | FRED                 |
| Real GDP per Capita *(DISCONTINUED)*                 | `JPNRGDPC`                  | `Real_GDP_Per_Capita`        | `GDPC_JAP`             | FRED                 |
| Exchange Rate: Japanese Yen to USD                   | `DEXJPUS`                   | `YEN_to_USD_Exchange`        | `EXR_JAP`              | FRED                 |
| Consumer Confidence Index                            | `CSCICP03.JPN.M`            | *(custom - via OECD API)*    | `CCI_JAP`              | OECD                 |

Link sources:
- Yield Spread: `INTGSBJPM193N`, 2Y: https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/index.htm
- Consumer Confidence Index: https://db.nomics.world/OECD/MEI_CLI/CSCICP03.JPN.M?tab=chart
---

## Main indicators for the Germany:
| Description                                            | Series ID        | READABLE_NAMES Entry      | Short Code Suggestion | Source              |
|--------------------------------------------------------|------------------|---------------------------|-----------------------|---------------------|
| Economic Policy Uncertainty Index for Germany          | `DEEPUINDXM`     | `Germany_EPU_Index`       | `EPU_GER`             | FRED                |
| Index of Industrial Production for Germany             | `A018ADDEA338NNBR` | `Industrial_Production`   | `IP_GER`              | FRED                |
| 10-Year Yield Spread                                   | `INTGSBDEM193N`  | `10Y_Bond_Yield`          | `10YS_GER`            | FRED                |
| 2-Year Government Bond Yield                           | *(ECB API)*      | 2Y_Yield_Spread           | `2YS_GER`             | ECB                 |
| 10-Year - 2-Year Yield Spread                          | *custom*         | Yield_Spread              | `YS_GER`              | ECB                 |
| Inflation, consumer prices for Germany                 | `FPCPITOTLZGDEU` | `Inflation`               | `INF_GER`             | FRED                |
| Unemployment to Population Rate: All Ages: All Persons | `LRUPTTTTDEQ156S` | `Unemployment_Rate`       | `UNEMP_GER`           | FRED                |
| Imports of Goods and Services in Germany               | `DEUIMPORTQDSNAQ` | `Real_Imports`            | `IM_GER`              | FRED                |
| Exports of Goods and Services in Germany               | `DEUEXPORTQDSNAQ` | `Real_Exports`            | `EX_GER`              | FRED                |
| OECD-based Recession Indicator *(DISCONTINUED)*        | `DEURECD`        | `Recession_Indicator`     | `RECESS_GER`          | FRED                |
| Real Gross Domestic Product for Germany                | `CLVMNACSCAB1GQDE` | `Real_GDP`                | `GDP_GER`             | FRED                |
| Real GDP per capita                                    | `DEURGDPC`       | `Real_GDP_Per_Capita`     | `GDPC_GER`            | FRED                |
| Exchange Rate (Local currency per 1 USD)               | `PA.NUS.FCRF`    | *(custom)*                | `EXR_GER`             | World Bank          |
| Exchange Rate (market + estimated)                     | `XRNCUSDEA618NRUG` | `Market_Exchange_Rate`    | `EXR_GER`             | FRED                |
| Consumer Confidence Index                              | `CSCICP03.DEU.M` | *(custom - via OECD API)* | `CCI_GER`             | OECD                |

Link sources:
- Yield Spread: 10Y: `INTGSBDEM193N`- 2Y: https://data.ecb.europa.eu/ API
- Exchange Rate (Local currency per 1 USD): `https://data.worldbank.org/indicator/PA.NUS.FCRF?locations=de`
- Consumer Confidence Index: `https://db.nomics.world/OECD/MEI_CLI/CSCICP03.DEU.M?tab=chart`
---

## Main indicators for China:
| Description                                                           | Series ID          | READABLE_NAMES Entry       | Short Code Suggestion | Source        |
|-----------------------------------------------------------------------|--------------------|----------------------------|-----------------------|---------------|
| Economic Policy Uncertainty Index for China                           | `CHIEPUINDXM`      | `China_EPU_Index`          | `EPU_CHI`             | FRED          |
| Production: Industry: Total Industry Excluding Construction for China | `CHNPRINTO01IXPYM` | `Industrial_Production`    | `IP_CHI`              | FRED          |
| 10Y - Yield Spread                                                    | `INTDSRCNM193N`    | `10Y_Yield_Spread`         | `10YS_CHI`            | FRED          |
| 2-Year Government Bond Yield                                          | `Investing.com`     | `2Y-Yield_Spread`          | `2YS_CHI`             | Investing.com |
| 10-Year - 2-Year Yield Spread                                         | *Custom*           | *Yield_Spread*             | `YS_CHI`              | Calculated    |
| Inflation, consumer prices for China                                  | `FPCPITOTLZGCHN`   | `Inflation`                | `INF_CHI`             | FRED          |
| Unemployment Rate for China                                           | *(World Bank)*     | *(custom)*                 | `UNEMP_CHI`           | World Bank    |
| Real Imports of Goods and Services for China                          | `NMRXDCCNA`        | `Real_Imports`             | `IM_CHI`              | FRED          |
| Real Exports of Goods and Services for China                          | `NXRXDCCNA`        | `Real_Exports`             | `EX_CHI`              | FRED          |
| International Trade: Net Trade Value (Goods) Total                    | `CHNXTNTVA01STSAQ` | `Net_Trade_Value`          | `TB_CHI`              | FRED          |
| OECD-based Recession Indicator *(DISCONTINUED)*                       | `CHNRECDM`         | `Recession_Indicator`      | `RECESS_CHI`          | FRED          |
| Real Gross Domestic Product for China                                 | `NGDPRXDCCNA`      | `Real_GDP`                 | `GDP_CHI`             | FRED          |
| Real GDP per capita                                                   | `NY.GDP.PCAP.CD`   | *(custom)*                 | `GDPC_CHI`            | World Bank    |
| USD to CNY Exchange Rate, End of Period                               | `CCUSSP02CNM650N`  | `USD_to_CNY_End_of_Period` | `EXR_CHI`             | FRED / OECD   |
| Consumer Confidence Index                                             | `CSCICP03.CHN.M`   | *(custom - via OECD API)*  | `CCI_CHI`             | OECD          |

Link sources:
- 2Y Bond Spread: https://www.investing.com/rates-bonds/china-2-year-bond-yield-historical-data
- Yield Spread: 10Y:`INTDSRCNM193N`- 2Y: `https://yield.chinabond.com.cn/cbweb-pbc-web/pbc/showHistory?locale=en_US`
- Unemployment Rate for China: `https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=CN`
- Real GDP per capita: `https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?locations=CN`
- Consumer Confidence Index: https://db.nomics.world/OECD/MEI_CLI/CSCICP03.CHN.M?tab=chart
---

##  Main Indicators for Canada
| Description                                                            | Series ID           | READABLE_NAMES Entry      | Short Code Suggestion | Source           |
|------------------------------------------------------------------------|---------------------|---------------------------|------------------------|------------------|
| Economic Policy Uncertainty Index for Canada                           | `CANEPUINDXM`       | `Canada_EPU_Index`        | `EPU_CAN`              | FRED             |
| Production: Industry: Total Industry Excluding Construction for Canada | `CANPRINTO01MLSAM`  | `Industrial_Production`   | `IP_CAN`               | FRED             |
| 10-Year Government Bond Yield                                          | `IRLTLT01CAQ156N`   | `10Y_Bond_Yield`          | `10YS_CAN`             | FRED             |
| 2-Year Government Bond Yield                                           | *(Bank of Canada)*  | `2Y_Bond_Yield`           | `2YS_CAN`              | Bank of Canada   |
| 10-Year - 2-Year Government Bond Spread                                | *(Custom)*          | `yield_spread`            | `YS_CAN`               | Calculated       |
| Inflation, consumer prices for Canada                                  | `FPCPITOTLZGCAN`    | `CPI_Inflation`           | `INF_CAN`              | FRED             |
| Unemployment Rate for Canada                                           | *(World Bank)*      | `Unemployment_rate`       | `UNEMP_CAN`            | World Bank       |
| Real Exports of Goods and Services for Canada                          | `NXRSAXDCCAQ`       | `Real_Exports`            | `EX_CAN`               | FRED             |
| Imports of Goods and Services in Canada                                | `CANIMPORTQDSNAQ`   | `Real_Imports`            | `IM_CAN`               | FRED             |
| OECD-based Recession Indicators for Canada *(DISCONTINUED)*            | `CANRECDM`          | `Recession_Indicator`     | `RECESS_CAN`           | FRED             |
| Real Gross Domestic Product for Canada                                 | `NGDPRSAXDCCAQ`     | `Real_GDP`                | `GDP_CAN`              | FRED             |
| Real GDP per capita *(DISCONTINUED)*                                   | `CANRGDPC`          | `Real_GDP_Per_Capita`     | `GDPC_CAN`             | FRED             |
| Interest Rates: Government Bonds (10-Year)                             | `INTGSBCAM193N`     | `Gov_Bonds`               | `GBR_CAN`              | FRED             |
| Interest Rates: Central Bank Rates (Overnight)                         | `IRSTCB01CAM156N`   | `Central_Bank_Rate`       | `CBR_CAN`              | FRED             |
| Canadian Dollar to U.S. Dollar Spot Exchange Rate                      | `DEXCAUS`           | `CAD_to_USD_Exchange`     | `EXR_CAN`              | FRED             |
| Consumer Confidence Index *(DISCONTINUED)*                             | `CSCICP03CAM665S`   | `CCI`                     | `CCI_CAN`              | FRED             |

---

## Main indicators for Mexico:
| Description                                                            | Series ID                  | READABLE_NAMES Entry       | Short Code Suggestion | Source     |
|------------------------------------------------------------------------|----------------------------|----------------------------|-----------------------|------------|
| World Uncertainty Index for Mexico                                     | `WUIMEX`                   | `Mexico_EPU`               | `EPU_MEX`             | FRED       |
| Production: Industry: Total Industry Including Construction for Mexico | `MEXPRINTO02IXOBSAM`       | `Industrial_Production`    | `IP_MEX`              | FRED       |
| Yield Spread (10Y Gov Bonds)                                           | `INTGSBMXM193N`            | `10Y_Bonds_Rate`           | `1OYS_MEX`            | FRED       |
| Yield Spread (2Y Gov Bonds)                                            | `IRLTST01MXM156N`          | `2Y_Bond_Rate`              | `2YS_MEX`             | FRED       |
| 10-Year - 2-Year Government Bond Spread                                | *(Custom)*                 | `yield_spread`             | `YS_MEX`              | Calculated |
| Inflation, consumer prices for Mexico                                  | `FPCPITOTLZGMEX`           | `Inflation`                | `INF_MEX`             | FRED       |
| Unemployment Rate for Mexico                                           | *(World Bank)*             | *(custom)*                 | `UNEMP_MEX`           | World Bank |
| Recession Indicator                                                    | `MEXRECD`                  | `recession_indicator`      | `RECESS_MEX`          | FRED       |
| Real Gross Domestic Product for Mexico                                 | `NGDPRSAXDCMXQ`            | `Real_GDP`                 | `GDP_MEX`             | FRED       |
| Real GDP per capita                                                    | `NY.GDP.PCAP.CD`           | *(custom)*                 | `GDPC_MEX`            | World Bank |
| Treasury Bills Rate                                                    | `INTGSTMXM193N`            | *(optional)*               | `TBR_MEX`             | FRED       |
| Exchange Rate to U.S. Dollar for Mexico                                | `FXRATEMXA618NUPN`         | `Exchange_Rate_USD`        | `EXR_MEX`             | FRED       |
| Consumer Confidence Index                                              | `CSCICP03.MEX.M`           | *(custom - via OECD API)*  | `CCI_MEX`             | OECD       |
| Additional Unemployment Rate                                           | `LRHUTTTTMXM156S`          | `Mexico_Unemployment_Rate` | `UNEMP_MEX`           | FRED       |
| Alternate Goods Exports metric                                         | `XTEXVA01MXM667S`          | `Goods_Exports`            | `EX_MEX`              | FRED       |

Source links:
- Unemployment Rate for Mexico: `https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=MX&name_desc=false`
- Real GDP per capita: `https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?locations=MX`
- Consumer Confidence Index: https://db.nomics.world/OECD/MEI_CLI/CSCICP03.MEX.M?tab=chart
