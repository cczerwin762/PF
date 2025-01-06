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
    missing = ''
    #Dividend Yield
    if not(tempDf[0][tempDf['index'] == 'dividendYield'].empty):
        DY = tempDf[0][tempDf['index'] == 'dividendYield'].values[0]*100
    #P/E Ratio
    if not(tempDf[0][tempDf['index'] == 'forwardPE'].empty):
        P = tempDf[0][tempDf['index'] == 'forwardPE'].values[0]
    elif missing == '': 
        missing = 'PE'
    #Earnings per share growth
    if missing == '' and not(tempDf[0][tempDf['index'] == 'earningsGrowth'].empty):
        EPSG = tempDf[0][tempDf['index'] == 'earningsGrowth'].values[0]*100
    elif missing == '' and not(tempDf[0][tempDf['index'] == 'pegRatio'].empty) :
        EPSG = P/(tempDf[0][tempDf['index'] == 'pegRatio'].values[0])
    elif missing == '': 
        missing = 'EPSG'

    if missing != '' :
        f.write(tickers[i] + ' had incomplete ' + missing + ' data\n')
        incomplete.append(i)
    EPSG = max(EPSG,0)
    EPSGrowth.append(EPSG)
    DivYield.append(DY)
    PE.append(P)
    FoS.append(max((EPSG+DY)/P,0))
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
plusFosDf = df[df['FoS'] > 0.05]
f.write(plusFosDf.sort_values(by=['FoS'],ascending=False).to_string())

#Valuation Method - 2 TensorFlow
'''
What will our input variables be - ticker + five crucial data points of a stock X(past data)
Y - Whether or not it was a good by - how will we quantify this? I guess we don't have to do a yes/no data point here we can just put the % change over the past year
would be smart to take into account how it paired against the industry average but this would complicate things/ we could do a model for one specific industry though
but maybe last year was just a bad year, so how will we know if the model predicts everything poorly based on biased year - ideally we'd do multiple years, but we will start with 1. 
Ticker, PE, PB, DE, FCF, PEG -> 1yr % change

'''

#Next step set threshold and determine/ buy no buy

#Look at Stocks already purchased and determine buy/ no buy/ sell
f.close()


#Next steps - find better way to pull web data for stocks that's more consistent than yfinance
# - AI valuation
# - Tableau presentation
# - Clean up this whole thing so it's more organized
# - finish the wallet functionality and buy sell functionality once the valuation's are good
