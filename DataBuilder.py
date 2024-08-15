import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
#from Helper import *
import re

#Stage - Scrape data from Urls in urls.csv
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
            for tag in soup.find_all(href=re.compile(filt)):
                tickers.append(tag.text)
        case _:
            print('invalid attribute')

#print(tickers)

#Stage - Remove duplicate tickers
if len(result)>1:
    #logic to remove duplicates
    print('Duplicates removed')

#Stage - Analyze each ticker

#--Valuation Method 1 - Peter Lynch
incomplete = [] #array to store indices of incomplete tickers to be removed later
EPSGrowth = []
DivYield = []
PE = []
FoS = []
for i in range(0,len(tickers)):
    print(tickers[i] + '\n')
    stock = yf.Ticker(tickers[i])
    dict = stock.info
    tempDf = pd.DataFrame.from_dict(dict,orient='index')
    tempDf = tempDf.reset_index()
    EPSG = 0
    DY = 0
    P = 1
    try:
        EPSG = tempDf[0][tempDf['index'] == 'forwardEps'].values[0]
        DY = tempDf[0][tempDf['index'] == 'fiveYearAvgDividendYield'].values[0]
        P = tempDf[0][tempDf['index'] == 'forwardPE'].values[0]
    except:
        print(tickers[i] + ' had incomplete data\n')
        incomplete.append(i)
    EPSGrowth.append(EPSG)
    DivYield.append(DY)
    PE.append(P)
    FoS.append((EPSG+DY)/P)
print('\n-----------------------------------------------------------\n')
print(str(len(incomplete)) + ' out of ' + str(len(tickers)) + ' tickers being deleted.')
for i in range(0,len(incomplete)):
    print("Removing: " + tickers[incomplete[i]-i]+ '\n')
    del tickers[incomplete[i]-i] # -i b/c index will continuously decrease by 1 as we move through the list
    del EPSGrowth[incomplete[i]-i]
    del DivYield[incomplete[i]-i]
    del PE[incomplete[i]-i]
    del FoS[incomplete[i]-i]
print('\n-----------------------------------------------------------\n')
d = {'Ticker': tickers, 'EPSGrowth' : EPSGrowth, 'DivYield':DivYield, 'P/E':PE,'FoS':FoS}
df = pd.DataFrame(data=d)
print(df)
# microsoft = yf.Ticker('MSFT')
# dict =  microsoft.info
# dfi = pd.DataFrame.from_dict(dict,orient='index')
# dfi = dfi.reset_index()
# test = []
# test.append(dfi[0][dfi['index'] == 'forwardEps'].values[0])
# print(test)

#Next step set threshold and determine/ buy no buy

#Look at Stocks already purchased and determine buy/ no buy/ sell