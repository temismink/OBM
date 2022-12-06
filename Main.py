import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import requests

def main():
    resp = requests.get("https://api.cryptowat.ch/markets/binance/btcusdt/orderbook?limit=1")
    orderbook = resp.json()['result']
    print (orderbook)

if __name__ == '__main__':
    main()