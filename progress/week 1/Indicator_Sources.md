## Main indicators for the US:

| Description                                             | Series ID         | READABLE\_NAMES Entry     | Short Code Suggestion | Unit             | Frequency | Source |
| ------------------------------------------------------- | ----------------- | ------------------------- | --------------------- | ---------------- | --------- | ------ |
| Economic Policy Uncertainty Index for the United States | `USEPUINDXD`      | `US_EPU_Index`            | `EPU_USA`             | Index            | Monthly   | FRED   |
| Industrial Production: Total Index                      | `INDPRO`          | `Industrial_Production`   | `IP_USA`              | Index (2017=100) | Monthly   | FRED   |
| 10Y - 2Y Treasury Yield Spread\*\*                      | `T10Y2Y`          | `Yield_Spread`            | `YS_USA`              | %                | Monthly   | FRED   |
| Consumer Price Inflation                                | `FPCPITOTLZGUSA`  | `Inflation`               | `INF_USA`             | %                | Annual    | FRED   |
| Unemployment Rate                                       | `UNRATE`          | `Unemployment_Rate`       | `UNEMP_USA`           | %                | Monthly   | FRED   |
| Real Exports of Goods and Services                      | `EXPGSC1`         | `Real_Exports`            | `EX_USA`              | Billions USD     | Quarterly | FRED   |
| Real imports of goods and services                      | `IMPGSC1`         | `Real_Imports`            | `IMP_USA`             | Billions USD     | Quarterly | FRED   |
| Recession Indicators *(DISCONTINUED)*                   | `USARECDM`        | `Recession_Indicator`     | `RECESS_USA`          | Binary (0/1)     | Monthly   | FRED   |
| Real Gross Domestic Product                             | `GDPC1`           | `Real_GDP`                | `GDP_USA`             | Billions USD     | Quarterly | FRED   |
| Real GDP per capita                                     | `A939RX0Q048SBEA` | `Real_GDP_Per_Capita`     | `GDPC_USA`            | USD              | Quarterly | FRED   |
| Consumer Confidence Index                               | `CSCICP03.USA.M`  | *(custom - via OECD API)* | `CCI_USA`             | Index            | Monthly   | OECD   |

### Link sources:

* Consumer Confidence Index: [OECD](https://db.nomics.world/OECD/MEI_CLI/CSCICP03.USA.M?tab=chart)

---

## Main indicators for Japan:

| Description                                          | Series ID             | READABLE\_NAMES Entry     | Short Code Suggestion | Unit          | Frequency | Source     |
| ---------------------------------------------------- | --------------------- | ------------------------- | --------------------- | ------------- | --------- | ---------- |
| Economic Policy Uncertainty Index for Japan          | `JPNEPUINDXM`         | `Japan_EPU_Index`         | `EPU_JAP`             | Index         | Monthly   | FRED       |
| Industrial Production (Excl. Construction) for Japan | `JPNPROINDAISMEI`     | `Industrial_Production`   | `IP_JAP`              | Index         | Monthly   | FRED       |
| 10-Year Government Bond Yield                        | `INTGSBJPM193N`       | `10Y_Bond_Yield`          | `10YS_JAP`            | %             | Monthly   | FRED       |
| 2-Year Government Bond Yield                         | *(MOF Japan Website)* | *(custom)*                | `2YS_JAP`             | %             | Monthly   | MOF Japan  |
| 10Y - 2Y Yield Spread                                | *(calculated)*        | `yield_spread`            | `YS_JAP`              | %             | Monthly   | Calculated |
| Inflation, consumer prices (annual %)                | `FPCPITOTLZGJPN`      | `Inflation`               | `INF_JAP`             | %             | Annual    | FRED       |
| Unemployment Rate (Ages 15 to 64) for Japan          | `LRUN64TTJPA156S`     | `Unemployment_Rate`       | `UNEMP_JAP`           | %             | Monthly   | FRED       |
| Real Exports of Goods and Services                   | `JPNRGDPEGS`          | `Real_Exports`            | `EX_JAP`              | Billions JPY  | Quarterly | FRED       |
| Real Imports of Goods and Services for Japan         | `JPNRGDPIGS`          | `Real_Imports `           | `IMP_JAP`             | Billions JPY  | Quarterly | FRED       |
| OECD-based Recession Indicators *(DISCONTINUED)*     | `JPNRECDP`            | `Recession_Indicator`     | `RECESS_JAP`          | Binary (0/1)  | Monthly   | FRED       |
| Real Gross Domestic Product for Japan                | `JPNRGDPEXP`          | `Real_GDP`                | `GDP_JAP`             | Trillions JPY | Quarterly | FRED       |
| Real GDP per Capita *(DISCONTINUED)*                 | `JPNRGDPC`            | `Real_GDP_Per_Capita`     | `GDPC_JAP`            | JPY           | Annual    | FRED       |
| Exchange Rate: Japanese Yen to USD                   | `DEXJPUS`             | `YEN_to_USD_Exchange`     | `EXR_JAP`             | JPY/USD       | Daily     | FRED       |
| Consumer Confidence Index                            | `CSCICP03.JPN.M`      | *(custom - via OECD API)* | `CCI_JAP`             | Index         | Monthly   | OECD       |

### Link sources:

* Yield Spread: `INTGSBJPM193N`, 2Y: [MOF Japan](https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/index.htm)
* Consumer Confidence Index: [OECD](https://db.nomics.world/OECD/MEI_CLI/CSCICP03.JPN.M?tab=chart)

---

## Main indicators for Germany:

| Description                                            | Series ID          | READABLE\_NAMES Entry     | Short Code Suggestion | Unit         | Frequency | Source     |
| ------------------------------------------------------ | ------------------ | ------------------------- | --------------------- | ------------ | --------- | ---------- |
| Economic Policy Uncertainty Index for Germany          | `DEEPUINDXM`       | `Germany_EPU_Index`       | `EPU_GER`             | Index        | Monthly   | FRED       |
| Index of Industrial Production for Germany             | `DEUPROINDMISMEI`  | `Industrial_Production`   | `IP_GER`              | Index        | Monthly   | FRED       |
| 10-Year Yield Spread                                   | `INTGSBDEM193N`    | `10Y_Bond_Yield`          | `10YS_GER`            | %            | Monthly   | FRED       |
| 2-Year Government Bond Yield                           | *(ECB API)*        | `2Y_Yield_Spread`         | `2YS_GER`             | %            | Monthly   | ECB        |
| 10-Year - 2-Year Yield Spread                          | *(custom)*         | `Yield_Spread`            | `YS_GER`              | %            | Monthly   | ECB        |
| Inflation, consumer prices for Germany                 | `FPCPITOTLZGDEU`   | `Inflation`               | `INF_GER`             | %            | Annual    | FRED       |
| Unemployment to Population Rate: All Ages: All Persons | `LRUPTTTTDEQ156S`  | `Unemployment_Rate`       | `UNEMP_GER`           | %            | Quarterly | FRED       |
| Real Imports of Goods and Services in Germany          | `NMRSAXDCDEQ`      | `Real_Imports`            | `IM_GER`              | Billions EUR | Quarterly | FRED       |
| Exports of Goods and Services in Germany               | `DEUEXPORTQDSNAQ`  | `Real_Exports`            | `EX_GER`              | Billions EUR | Quarterly | FRED       |
| OECD-based Recession Indicator *(DISCONTINUED)*        | `DEURECD`          | `Recession_Indicator`     | `RECESS_GER`          | Binary (0/1) | Monthly   | FRED       |
| Real Gross Domestic Product for Germany                | `CLVMNACSCAB1GQDE` | `Real_GDP`                | `GDP_GER`             | Billions EUR | Quarterly | FRED       |
| Real GDP per capita                                    | `DEURGDPC`         | `Real_GDP_Per_Capita`     | `GDPC_GER`            | EUR          | Annual    | FRED       |
| Exchange Rate (Local currency per 1 USD)               | `PA.NUS.FCRF`      | *(custom)*                | `EXR_GER`             | Local/USD    | Annual    | World Bank |
| Exchange Rate (market + estimated)                     | `XRNCUSDEA618NRUG` | `Market_Exchange_Rate`    | `EXR_GER`             | Local/USD    | Monthly   | FRED       |
| Consumer Confidence Index                              | `CSCICP03.DEU.M`   | *(custom - via OECD API)* | `CCI_GER`             | Index        | Monthly   | OECD       |

### Link sources:

* Yield Spread: 10Y: `INTGSBDEM193N`, 2Y: [ECB Yield Data](https://data.ecb.europa.eu/data/datasets/YC/YC.B.U2.EUR.4F.G_N_A.SV_C_YM.SRS_10Y_2Y)
* Exchange Rate (Local currency per 1 USD): [World Bank](https://data.worldbank.org/indicator/PA.NUS.FCRF?locations=de)
* Consumer Confidence Index: [OECD](https://db.nomics.world/OECD/MEI_CLI/CSCICP03.DEU.M?tab=chart)

---
## Main indicators for China:

| Description                                                           | Series ID          | READABLE\_NAMES Entry      | Short Code Suggestion | Unit          | Frequency | Source        |
| --------------------------------------------------------------------- | ------------------ | -------------------------- | --------------------- | ------------- | --------- | ------------- |
| Economic Policy Uncertainty Index for China                           | `CHIEPUINDXM`      | `China_EPU_Index`          | `EPU_CHI`             | Index         | Monthly   | FRED          |
| Production: Industry: Total Industry Excluding Construction for China | `CHNPRINTO01IXPYM` | `Industrial_Production`    | `IP_CHI`              | Index         | Monthly   | FRED          |
| 10Y - Yield Spread                                                    | `INTDSRCNM193N`    | `10Y_Yield_Spread`         | `10YS_CHI`            | %             | Monthly   | FRED          |
| 2-Year Government Bond Yield                                          | `Investing.com`    | `2Y-Yield_Spread`          | `2YS_CHI`             | %             | Daily     | Investing.com |
| 10-Year - 2-Year Yield Spread                                         | *(Custom)*         | *Yield\_Spread*            | `YS_CHI`              | %             | Monthly   | Calculated    |
| Inflation, consumer prices for China                                  | `FPCPITOTLZGCHN`   | `Inflation`                | `INF_CHI`             | %             | Annual    | FRED          |
| Unemployment Rate for China                                           | *(World Bank)*     | *(custom)*                 | `UNEMP_CHI`           | %             | Annual    | World Bank    |
| Real Imports of Goods and Services for China                          | `NMRXDCCNA`        | `Real_Imports`             | `IM_CHI`              | Billions CNY  | Annual    | FRED          |
| Real Exports of Goods and Services for China                          | `NXRXDCCNA`        | `Real_Exports`             | `EX_CHI`              | Billions CNY  | Annual    | FRED          |
| International Trade: Net Trade Value (Goods) Total                    | `CHNXTNTVA01STSAQ` | `Net_Trade_Value`          | `TB_CHI`              | Billions CNY  | Quarterly | FRED          |
| OECD-based Recession Indicator *(DISCONTINUED)*                       | `CHNRECDM`         | `Recession_Indicator`      | `RECESS_CHI`          | Binary (0/1)  | Monthly   | FRED          |
| Real Gross Domestic Product for China                                 | `NGDPRXDCCNA`      | `Real_GDP`                 | `GDP_CHI`             | Trillions CNY | Annual    | FRED          |
| Real GDP per capita                                                   | `NY.GDP.PCAP.CD`   | *(custom)*                 | `GDPC_CHI`            | USD           | Annual    | World Bank    |
| USD to CNY Exchange Rate, End of Period                               | `CCUSSP02CNM650N`  | `USD_to_CNY_End_of_Period` | `EXR_CHI`             | CNY/USD       | Monthly   | FRED / OECD   |
| Consumer Confidence Index                                             | `CSCICP03.CHN.M`   | *(custom - via OECD API)*  | `CCI_CHI`             | Index         | Monthly   | OECD          |

### Link sources:

* Real Imports for China is Annually
* 2Y Bond Spread: [Investing.com](https://www.investing.com/rates-bonds/china-2-year-bond-yield-historical-data)
* Yield Spread: 10Y: `INTDSRCNM193N`, 2Y: [Chinabond](https://yield.chinabond.com.cn/cbweb-pbc-web/pbc/showHistory?locale=en_US)
* Unemployment Rate: [World Bank](https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=CN)
* Real GDP per capita: [World Bank](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?locations=CN)
* Consumer Confidence Index: [OECD](https://db.nomics.world/OECD/MEI_CLI/CSCICP03.CHN.M?tab=chart)
* New GDP: [World Bank](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD?locations=CN)

---
## Main indicators for Canada:

| Description                                                            | Series ID          | READABLE\_NAMES Entry   | Short Code Suggestion | Unit         | Frequency | Source         |
| ---------------------------------------------------------------------- | ------------------ | ----------------------- | --------------------- | ------------ | --------- | -------------- |
| Economic Policy Uncertainty Index for Canada                           | `CANEPUINDXM`      | `Canada_EPU_Index`      | `EPU_CAN`             | Index        | Monthly   | FRED           |
| Production: Industry: Total Industry Excluding Construction for Canada | `CANPROINDMISMEI`  | `Industrial_Production` | `IP_CAN`              | Index        | Monthly   | FRED           |
| 10-Year Government Bond Yield                                          | `IRLTLT01CAQ156N`  | `10Y_Bond_Yield`        | `10YS_CAN`            | %            | Monthly   | FRED           |
| 2-Year Government Bond Yield                                           | *(Bank of Canada)* | `2Y_Bond_Yield`         | `2YS_CAN`             | %            | Monthly   | Bank of Canada |
| 10-Year - 2-Year Government Bond Spread                                | *(Custom)*         | `yield_spread`          | `YS_CAN`              | %            | Monthly   | Calculated     |
| Inflation, consumer prices for Canada                                  | `FPCPITOTLZGCAN`   | `CPI_Inflation`         | `INF_CAN`             | %            | Annual    | FRED           |
| Unemployment Rate for Canada                                           | *(World Bank)*     | `Unemployment_rate`     | `UNEMP_CAN`           | %            | Annual    | World Bank     |
| Real Exports of Goods and Services for Canada                          | `NXRSAXDCCAQ`      | `Real_Exports`          | `EX_CAN`              | Billions CAD | Quarterly | FRED           |
| Real Imports of Goods and Services for Canada                          | `NMRSAXDCCAQ`      | `Real_Imports`          | `IM_CAN`              | Billions CAD | Quarterly | FRED           |
| OECD-based Recession Indicators for Canada *(DISCONTINUED)*            | `CANRECDM`         | `Recession_Indicator`   | `RECESS_CAN`          | Binary (0/1) | Monthly   | FRED           |
| Real Gross Domestic Product for Canada                                 | `NGDPRSAXDCCAQ`    | `Real_GDP`              | `GDP_CAN`             | Billions CAD | Quarterly | FRED           |
| Real GDP per capita *(DISCONTINUED)*                                   | `CANRGDPC`         | `Real_GDP_Per_Capita`   | `GDPC_CAN`            | CAD          | Annual    | FRED           |
| Interest Rates: Government Bonds (10-Year)                             | `INTGSBCAM193N`    | `Gov_Bonds`             | `GBR_CAN`             | %            | Monthly   | FRED           |
| Interest Rates: Central Bank Rates (Overnight)                         | `IRSTCB01CAM156N`  | `Central_Bank_Rate`     | `CBR_CAN`             | %            | Monthly   | FRED           |
| Canadian Dollar to U.S. Dollar Spot Exchange Rate                      | `DEXCAUS`          | `CAD_to_USD_Exchange`   | `EXR_CAN`             | CAD/USD      | Daily     | FRED           |
| Consumer Confidence Index *(DISCONTINUED)*                             | `CSCICP03CAM665S`  | `CCI`                   | `CCI_CAN`             | Index        | Monthly   | FRED           |

---
## Main indicators for Mexico:

| Description                                                            | Series ID            | READABLE\_NAMES Entry      | Short Code Suggestion | Unit         | Frequency | Source     |
| ---------------------------------------------------------------------- | -------------------- | -------------------------- | --------------------- | ------------ | --------- | ---------- |
| World Uncertainty Index for Mexico                                     | `WUIMEX`             | `Mexico_EPU`               | `EPU_MEX`             | Index        | Quarterly | FRED       |
| Production: Industry: Total Industry Including Construction for Mexico | `MEXPRINTO02IXOBSAM` | `Industrial_Production`    | `IP_MEX`              | Index        | Monthly   | FRED       |
| Yield Spread (10Y Gov Bonds)                                           | `INTGSBMXM193N`      | `10Y_Bonds_Rate`           | `1OYS_MEX`            | %            | Monthly   | FRED       |
| Yield Spread (2Y Gov Bonds)                                            | `IRLTST01MXM156N`    | `2Y_Bond_Rate`             | `2YS_MEX`             | %            | Monthly   | FRED       |
| 10-Year - 2-Year Government Bond Spread                                | *(Custom)*           | `yield_spread`             | `YS_MEX`              | %            | Monthly   | Calculated |
| Inflation, consumer prices for Mexico                                  | `FPCPITOTLZGMEX`     | `Inflation`                | `INF_MEX`             | %            | Annual    | FRED       |
| Unemployment Rate for Mexico                                           | *(World Bank)*       | *(custom)*                 | `UNEMP_MEX`           | %            | Annual    | World Bank |
| Recession Indicator                                                    | `MEXRECD`            | `recession_indicator`      | `RECESS_MEX`          | Binary (0/1) | Monthly   | FRED       |
| Real Gross Domestic Product for Mexico                                 | `NGDPRSAXDCMXQ`      | `Real_GDP`                 | `GDP_MEX`             | Billions MXN | Quarterly | FRED       |
| Real GDP per capita                                                    | `NY.GDP.PCAP.CD`     | *(custom)*                 | `GDPC_MEX`            | USD          | Annual    | World Bank |
| Real Exports of Goods and Services for Mexico                          | `NXRSAXDCMXQ`        | `Real_Exports`             | `EX_MEX`              | Billions MXN | Quarterly | FRED       |
| Real Imports of Goods and Services for Mexico                          | `NMRSAXDCMXQ`        | `Real_Imports`             | `IM_MEX`              | Billions MXN | Quarterly | FRED       |
| Exchange Rate to U.S. Dollar for Mexico                                | `FXRATEMXA618NUPN`   | `Exchange_Rate_USD`        | `EXR_MEX`             | MXN/USD      | Monthly   | FRED       |
| Consumer Confidence Index                                              | `CSCICP03.MEX.M`     | *(custom - via OECD API)*  | `CCI_MEX`             | Index        | Monthly   | OECD       |
| Additional Unemployment Rate                                           | `LRHUTTTTMXM156S`    | `Mexico_Unemployment_Rate` | `UNEMP_MEX`           | %            | Monthly   | FRED       |

### Source links:

* Unemployment Rate for Mexico: [World Bank](https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=MX&name_desc=false)
* Real GDP per capita: [World Bank](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?locations=MX)
* Consumer Confidence Index: [OECD](https://db.nomics.world/OECD/MEI_CLI/CSCICP03.MEX.M?tab=chart)
