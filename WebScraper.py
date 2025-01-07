import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import datetime
#from Helper import *
import re

result = pd.read_csv('./help/urls.csv')
tickers = []

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