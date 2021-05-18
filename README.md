# Py-Trade
Technical Analysis and Smoothed Data + Statistics in an attempt to increase accuracy

data_getter takes and sorts JSON data from IEX Cloud API retrieved data, there is a muted block that transfers the JSON data into a pandas dataframe so it is easier to work with.
It continues on to remove the unecessary data and calculate the TWAP of the price in order to provide the user with more accurate prices, and less noise. The final TWAP 
price is more closely accurate to what execution price could be throughout the trading day.

Algorithm uses a DC algo from an SSRN research paper. Calculates percent changes above and below a specific threshold to identify extending trends. 
