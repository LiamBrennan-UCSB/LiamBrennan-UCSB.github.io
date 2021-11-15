import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import sys
import datetime
import csv
import copy 

TODAY = datetime.datetime.now() - datetime.timedelta(days=0)
INTERVAL_DAYS = int(sys.argv[1])
PREV_DATE = TODAY - datetime.timedelta(days=1)
PERCENT = float(sys.argv[2])

#------------- load csv -------------#
_fpath = f'prediction_spreadsheet_{INTERVAL_DAYS}_{datetime.date.strftime(TODAY, "%Y-%m-%d")}_{PERCENT}_gt87.csv'
print(_fpath)
predictions = pd.read_csv(_fpath, encoding='ISO-8859–1')

print(predictions)

actual_closing, percent_error, delta_mu, simulated_shares, num_shares, returns = [], [], [], [], [], []
for t_idx, ticker in enumerate(predictions.ticker):

    ## get today's closing ##
    ticker_yahoo = yf.Ticker(ticker)
    todayData = ticker_yahoo.history(period='1d')
    last_quote = todayData['Close'][0]
    actual_closing.append(last_quote)

    ## compute percent error ##
    percent_error.append(100.*abs(predictions.prediction[t_idx]-last_quote)/last_quote)

    ## compute delta_mu ##
    d_mu = last_quote - predictions.prev_close[t_idx]

    delta_mu.append(d_mu)

    ## compute simulated number of shares ##
    simulated_share_frac = predictions.confidence[t_idx] / np.sum(predictions.confidence)

    simulated_shares.append(simulated_share_frac)

    ## compute number of shares based on $100 ##
    money_to_spend = simulated_share_frac*5000.
    num_shares_to_buy = np.floor(money_to_spend/predictions.prev_close[t_idx])
    if num_shares_to_buy < 1:
        num_shares_to_buy = 0

    num_shares.append(num_shares_to_buy)


    ## compute returns ##
    returns.append(num_shares_to_buy*d_mu)


## add new columns ##
performance = copy.deepcopy(predictions)
performance['actual_closing'] = actual_closing
performance['percent_error'] = percent_error
performance['delta_mu'] = delta_mu
performance['simulated_shares'] = simulated_shares
performance['num_shares'] = num_shares
performance['returns'] = returns

## save csv ##
performance.to_csv(f"performance_spreadsheet{_fpath.split('spreadsheet')[-1]}")
with open("performance_files.txt", "a") as pf:
    pf.write(f"performance_spreadsheet{_fpath.split('spreadsheet')[-1]}\n")

