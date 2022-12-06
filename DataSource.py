import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from multiprocessing import Process, Queue
import logging

class DataSource:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        
    def process(cls, queue, source = None):
        #orderbook for btcusd
        resp = requests.get("https://api.cryptowat.ch/markets/binance/btcusdt/orderbook?limit=1000")
        orderbook = resp.json()['result']
        print (orderbook)

        resp2 = requests.get("https://api.cryptowat.ch/markets/kraken/btcusdt/trades?limit=1000")
        trades = resp2.json()['result']
        print (trades)

        #when i have websocket or feed
        source = cls() if source is None else source
        while True:
            data = source.get_data()
            if data is not None:
                queue.put(data)
                if data == 'POISON':
                    break

        #backtester