import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import datetime
#from Helper import *
import re

#Stage - Open log file
f = open('./logs/DataBuilderLog_' + str(datetime.datetime.now()).replace(' ', '_').replace(':', '-') + '.txt','w')
f.write('DataBuilder.py log data for: ' + str(datetime.datetime.now()) + '\n')
#Stage - Scrape data from Urls in urls.csv
result = pd.read_csv('./help/urls.csv')
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
            f.write('invalid attribute')

#print(tickers)

#Stage - Remove duplicate tickers
if len(result)>1:
    #logic to remove duplicates
    f.write('Duplicates removed')

#Stage - Analyze each ticker

#--Valuation Method 1 - Peter Lynch
incomplete = [] #array to store indices of incomplete tickers to be removed later
EPSGrowth = []
DivYield = []
PE = []
FoS = []
for i in range(0,len(tickers)):
    f.write(tickers[i] + '\n')
    stock = yf.Ticker(tickers[i])
    dict = stock.info
    tempDf = pd.DataFrame.from_dict(dict,orient='index')
    tempDf = tempDf.reset_index()
    EPSG = 0
    DY = 0
    P = 1
    err = 'ESPG'
    try:
        EPSG = tempDf[0][tempDf['index'] == 'forwardEps'].values[0]
        err = 'DY'
        DY = tempDf[0][tempDf['index'] == 'fiveYearAvgDividendYield'].values[0]
        err = 'PE'
        P = tempDf[0][tempDf['index'] == 'forwardPE'].values[0]
    except:
        f.write(tickers[i] + ' had incomplete ' + err + ' data\n')
        incomplete.append(i)
    EPSGrowth.append(EPSG)
    DivYield.append(DY)
    PE.append(P)
    FoS.append((EPSG+DY)/P)
f.write('\n-----------------------------------------------------------\n')
f.write(str(len(incomplete)) + ' out of ' + str(len(tickers)) + ' tickers being deleted.')
for i in range(0,len(incomplete)):
    f.write("Removing: " + tickers[incomplete[i]-i]+ '\n')
    del tickers[incomplete[i]-i] # -i b/c index will continuously decrease by 1 as we move through the list
    del EPSGrowth[incomplete[i]-i]
    del DivYield[incomplete[i]-i]
    del PE[incomplete[i]-i]
    del FoS[incomplete[i]-i]
f.write('\n-----------------------------------------------------------\n')
d = {'Ticker': tickers, 'EPSGrowth' : EPSGrowth, 'DivYield':DivYield, 'P/E':PE,'FoS':FoS}
df = pd.DataFrame(data=d)
f.write(df.to_string())

#Next step set threshold and determine/ buy no buy

#Look at Stocks already purchased and determine buy/ no buy/ sell
f.close()