#using TA-Lib to create technical analysis / charts / patterns

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
import talib as ta
from talib import MA_Type
style.use('ggplot')

#data import -- work on making this a function or at least try and condense it
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

#trying our first TA-LIB technical 
upper, middle, lower = ta.BBANDS(df['close'], matype=MA_Type.T3)

df['pos'] = np.where(df['TWAP'] > middle, 1, -1) 
df['returns'] = np.log(df['TWAP'] / df['TWAP'].shift(1)) 
df['strat'] = df['pos'].shift(1) * df['returns']
df.dropna(inplace=True)
totals = np.exp(df[['returns', 'strat']].sum())
print(totals)


upper.plot(label='upper')
middle.plot(label='mid')
lower.plot(label='lower')
plt.plot(df['TWAP'])
plt.legend(loc='upper left')
df['pos'].plot(secondary_y='pos')
plt.show()