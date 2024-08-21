import yfinance as yf
import pandas as pd
stock = yf.Ticker('SIRI')
dict = stock.info
tempDf = pd.DataFrame.from_dict(dict,orient='index')
tempDf = tempDf.reset_index()
pd.set_option("display.max_rows", None)

print(tempDf)