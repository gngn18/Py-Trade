# Py-Trade
Technical Analysis and Smoothed Data + Statistics in an attempt to increase accuracy

data_getter takes and sorts JSON data from IEX Cloud API retrieved data, there is a muted block that transfers the JSON data into a pandas dataframe so it is easier to work with.
It continues on to remove the unecessary data and calculate the TWAP of the price in order to provide the user with more accurate prices, and less noise. The final TWAP 
price is more closely accurate to what execution price could be throughout the trading day.

Algorithm uses a DC algo from an SSRN research paper. Calculates percent changes above and below a specific threshold to identify extending trends. Stores strings and floats in a Pandas DataFrame, cannot plot the strings but can plot the floats (using arrows for BUY and SELL). Also it is calculating the changes based off of the TWAP prices to try and increase "purchasing accuracy" 
Working on adding more functions to be able to plot the data once it is called upon.
Added the full algo + quick low level vectorized backtest. Would outperform buy and hold, will be able to provide more data once I figure out how to calculate returns when you hold the position, not just a quick buy and sell.

Technicals: uses TALIB to create technical indicators and plot them as well as use a quick vectorized "backtester" very low level, just to see if something could be there. Ultimately want to have an event based system.
