import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from multiprocessing import Process, Queue
import logging

def __init__(self):
    self._logger = logging.getLogger(__name__)
    
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

    #backtester