import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import datetime
from Helper import *
import re
from WebScraper import *
'''
Scripts to help with setup, testing, and stuff. I will comment these out as I go
'''
url = 'https://stockanalysis.com/stocks/sector/technology/'
attr = 'href'
filter = '/stocks/'

ws = WebScraper(url,attr,filter)
ticks = []
ws.scrapeToList(ticks)
print('Script start')
print(ticks)
#clean these tickers and helper file



