# import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from Helper import *
import re
# # url = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives?by=volume&top=10"

# # headers = {"accept": "application/json"}

# # response = requests.get(url, headers=headers)

# # print(response.text)

#Stage - Scrape data from yfinance or above/ both
url = "https://www.wsj.com/market-data/stocks/us/movers"
url2 = "https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


#Stage - Pick out tickers
movers = [] #top movers for the day
for tag in soup.find_all(href=re.compile("/symbols/NASDAQ")):
    print(tag.text)
# for tag in soup.find_all(attrs={"data-test":"quoteLink"}):
#     print(tag.name)
#     print('tag')
#Stage - Analyze each ticker

#Next step set threshold and determine/ buy no buy

#Look at Stocks already purchased and determine buy/ no buy/ sell