# import yfinance as yf
import requests

url = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives?by=volume&top=10"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)