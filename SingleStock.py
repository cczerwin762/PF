import yfinance as yf
import pandas as pd
inp = input("Ticker: ")
stock = yf.Ticker(inp)
dict = stock.info
tempDf = pd.DataFrame.from_dict(dict,orient='index')
tempDf = tempDf.reset_index()
pd.set_option("display.max_rows", None)
print(tempDf.sort_values(by='index',ascending=True))
