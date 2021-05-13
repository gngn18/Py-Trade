#necessary imports 
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

# you will need to add the data yourself (ie. a csv file containing your stock data)
# I used an API wiht a data cloud service to get my data so I have removed my KEY 


#modifying the data so it will be in the format and the amount that I want
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


#using pandas to create two exponential moving averages 
df['ema20'] = df['TWAP'].ewm(alpha=0.2, adjust=False).mean()
df['ema40'] = df['TWAP'].ewm(alpha=0.4, adjust=False).mean()
#print(df.head(40))
# apparently the EMA 40, under TWAP conditions, is closer to the actual close price than the EMA 20 is... explore this 






'''
#plotting the two moving averages and the close value of stock
fig = plt.figure()
ax1 = fig.add_subplot()
ax1.plot(df.loc[df.pos == 1.0].index, df.ema40[df.pos == 1.0], '^', markersize=10, color='m')
ax1.plot(df.loc[df.pos == -1.0].index, df.ema40[df.pos == -1.0], 'v', markersize=10, color='k')
df['close'].plot(ax=ax1)
df['TWAP'].plot(ax=ax1)
df['ema20'].plot(ax=ax1, label='ema20')
df['ema40'].plot(ax=ax1, label='ema40') 
plt.legend(loc='upper left')
plt.show()
'''