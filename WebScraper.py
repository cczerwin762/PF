import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import datetime
from Helper import *
import re

class WebScraper:
    def __init__(self,url,attr,filter):
        self.url = url
        self.attr = attr
        self.filter = filter
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def scrapeToList(self, list):
        match self.attr:
            case 'href':
                for tag in self.soup.find_all(href=re.compile(self.filter)):
                    list.append(tag.text)
            case _:
                print('invalid attribute')

    def scrapeToFile(self, fileName):
        list = []
        self.scrapeToList(list)
        match fileName[-3:]:
            case '.txt':
                ParseListToTxt()
            case '.csv':
                ParseListToCsv()
            case _:
                print('invalid file extension')


        