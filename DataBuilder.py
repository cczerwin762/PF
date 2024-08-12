# import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
#from Helper import *
import re
#Stage - Scrape data from Urls in urls.csv
df = pd.DataFrame()
result = pd.read_csv('Urls.csv')
tickers = []
for i in range(0,len(result)):
    url = result['url'][i]
    attr = result['attr'][i]
    filt = result['filter'][i]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    match attr:
        case 'href':
            for tag in soup.find_all(href=re.compile("/symbols/NASDAQ")):
                tickers.append(tag.text)
        case _:
            print('invalid attribute')

print(tickers)


#Stage - Pick out tickers
#movers = [] #top movers for the day
#

#Stage - Analyze each ticker

#Next step set threshold and determine/ buy no buy

#Look at Stocks already purchased and determine buy/ no buy/ sell