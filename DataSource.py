import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from multiprocessing import Process, Queue
import logging
from pandas_datareader import DataReader
import datetime as dt
import domain

def __init__(self):
    self._logger = logging.getLogger(__name__)
    self.set_source(source = source, tickers=tickers, start=start, end=end)
    
def get_data():
    #orderbook for btcusd
    resp = requests.get("https://api.cryptowat.ch/markets/binance/btcusdt/orderbook?limit=1000")
    orderbook = resp.json()['result']
    print (orderbook)

    #trades
    resp2 = requests.get("https://api.cryptowat.ch/markets/kraken/btcusdt/trades?limit=1000")
    trades = resp2.json()['result']
    print (trades)

    #get price for each / timeframe?
    return [[3, 3], [4,4]]

def process(cls, queue, source = None):

    #when i have websocket or feed
    source = cls() if source is None else source
    while True:
        data = source.get_data()
        if data is not None:
            queue.put(data)
            if data == 'POISON':
                break

def set_source(self, source, tickers, start, end):
        prices = pd.DataFrame()
        counter = 0.
        for ticker in tickers:
            try:
                self._logger.info('Loading ticker %s' % (counter / len(tickers)))
                prices[ticker] = DataReader(ticker, source, start, end).loc[:, 'Close']
            except Exception as e:
                self._logger.error(e)
                pass
            counter+=1

        events = []
        for row in prices.iterrows():
            timestamp=row[0]
            series = row[1]
            vals = series.values
            indx = series.index
            for k in np.random.choice(len(vals),replace=False, size=len(vals)): # Shuffle!
                if np.isfinite(vals[k]):
                    events.append((timestamp, indx[k], vals[k]))

        self._source = events

        self._logger.info('Loaded data!')

def get_data(self):
    try:
        return self._source.pop(0)
    except IndexError as e:
        return 'POISON'