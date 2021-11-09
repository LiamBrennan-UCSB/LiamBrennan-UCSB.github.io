import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import sys
import datetime
import csv
import copy 

TODAY = datetime.datetime.now()
INTERVAL_DAYS = int(sys.argv[1])
PERCENT = int(sys.argv[2])

#------------- load csv -------------#
_fpath = f'prediction_spreadsheet_{INTERVAL_DAYS}_{datetime.date.strftime(TODAY, "%Y-%m-%d")}_{PERCENT}.csv'
predictions = pd.read_csv(_fpath)

print(predictions.ticker)

actual_closing, percent_error, delta_mu = [], [], []
for t_idx, ticker in enumerate(predictions.ticker):

    ## get today's closing ##
    ticker_yahoo = yf.Ticker(ticker)
    todayData = ticker_yahoo.history(period='1d')
    last_quote = todayData['Close'][0]
    actual_closing.append(last_quote)

    ## compute percent error ##
    percent_error.append(abs(predictions.prediction[t_idx]-last_quote)/last_quote)

    ## compute delta_mu ##
    delta_mu = last_quote - predictions.prev_close[t_idx]


## add new columns ##
performance = copy.deepcopy(predictions)
performance['actual_closing'] = actual_closing
performance['percent_error'] = percent_error
performance['delta_mu'] = delta_mu

## save csv ##
performance.to_csv(f"performance_spreadsheet{_fpath.split('spreadsheet')[-1]}")

