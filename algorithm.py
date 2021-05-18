#the algorithm 
#going to use TWAP EMA prices to detect directional changes with greater accuracy that thru noisy data 
## needs ##
# OHLC Data 
# Transfer into TWAP 
# EMA calculations 
## smoothing facotor ## 
# Directional changes 
# Buy and Sell Signals 
# holding period 
# backtest 
# returns of long/short against buy/hold 

#package imports 
import pandas as pd 
import numpy as np 
from pandas_datareader import DataReader
import math 
import os 
import path 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style 
import time 
import datetime
import requests
import io 
import json
style.use('ggplot')





# data import and cleansing and sorting 
df = pd.read_csv('TWTR.csv', parse_dates=True, index_col=0)
df = pd.DataFrame(df)
df.set_index('date', inplace=True)
df.drop([
    'symbol', 
    'id', 
    'key', 
    'subkey', 
    'updated', 
    'changeOverTime', 
    'marketChangeOverTime',
    'uOpen',
    'uVolume',
    'fOpen',
    'fClose',
    'fHigh',
    'fLow',
    'fVolume',
    'label',
    'change',
    'changePercent',
    'uHigh',
    'uClose',
    'uLow'], inplace=True, axis=1)
#calculating and using better data 
# using filtered data TWAP
# remember cannot observe and act upon actual close data received, this will add misinformation to your backtest
df['OH Dist'] = (df['high'] - df['open'])
df['OL Dist'] = (df['open'] - df['low'])
df['HL Dist'] = (df['high'] - df['low'])
df['LC Dist'] = (df['close'] - df['low'])
df['HC Dist'] = (df['high'] - df['close'])
df['OHLC Dist'] = (df['OH Dist'] + df['HL Dist'] + df['LC Dist'])
df['OLHC Dist'] = (df['OL Dist'] + df['HL Dist'] + df['HC Dist'])
df['OH Mean'] = (df['open'] + df['high']) * 0.5 
df['OL Mean'] = (df['open'] + df['low']) * 0.5
df['HL Mean'] = (df['high'] + df['low']) * 0.5
df['LC Mean'] = (df['low'] + df['close']) * 0.5 
df['HC Mean'] = (df['high'] + df['close']) * 0.5 
df['OHLC TWAP'] = (((df['OH Dist'] / df['OHLC Dist']) * df['OH Mean']) + ((df['HL Dist'] / df['OHLC Dist']) * df['HL Mean']) + ((df['LC Dist'] / df['OHLC Dist']) * df['LC Mean']))
df['OLHC TWAP'] = (((df['OL Dist'] / df['OLHC Dist']) * df['OL Mean']) + ((df['HL Dist'] / df['OLHC Dist']) * df['HL Mean']) + ((df['HC Dist'] / df['OLHC Dist']) * df['HC Mean']))
df['TWAP'] = ((df['OHLC TWAP'] + df['OLHC TWAP']) * 0.5)
df.drop([
    'OH Dist',
    'OL Dist',
    'HL Dist',
    'LC Dist',
    'HC Dist',
    'OHLC Dist',
    'OLHC Dist',
    'OH Mean',
    'OL Mean',
    'HL Mean',
    'LC Mean',
    'HC Mean',
    'OHLC TWAP',
    'OLHC TWAP'], inplace=True, axis=1)


# calculation of directional changes 
def directional(data, d=0.1):
    
    #algorithm design 
    ''' 
    takes in data ---- 
    "if the event is an upturn event" - don't think I actually need to calculate this since technically it will be streamed continuously 
    and it will just be able to calculate this throughout time
    if price at time i is <= high price * (1 - threshold):
        "downturn"
        low price = current price (because it is lower)
        end time for downturn event
        start time for downward overshoot *** this is what we want, overshoot = trend = profit 
    elif high price < price at time i:
        high price = price at time i 
        start time for downturn event 
        end time for upward overshoot 
    end if 
    if price at time i <= low price * (1 + threshold):
        "upturn"
        price high = price at time i 
        end time for upturn event 
        start time for upward overshoot event 
    elif low price > price at time i:
        low price = price at time i 
        start time for an upturn event 
        end time for a downard overshoot 
    end if 
    '''
    #using a list for testing purposes, but a rather inefficient way to store the data because it has to be done at a specific event
    #storage = []

    data['sig'] = ""
    data['sign'] = ""
    high = data['high'][0]
    low = high

    for i in range(len(data)):
        if data['close'][i] <= high * (1 - d):
            high = data['close'][i]
            data['sig'][i] = data['TWAP'][i]
            data['sign'][i] = "sell"
        elif data['close'][i] <= low * (1 + d):
            low = data['close'][i]
            data['sig'][i] = data['TWAP'][i]
            data['sign'][i] = "buy"
        else:
            pass

    #data['sig'].plot()
    print(data)

directions = directional(df)
print(directions)


#plt.show()    
                
    








