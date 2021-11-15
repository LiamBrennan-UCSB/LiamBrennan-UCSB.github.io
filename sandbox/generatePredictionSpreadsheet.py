import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import sys
import datetime
import csv

## load in ML algorithm ##
import sys
sys.path.insert(0, '../modules/apollo/src/core/')

import DataFormatterv1
import ClassificationNetv1
import IterativeApproximation

TODAY = datetime.datetime.now()
d = datetime.timedelta(days=0)
TODAY = TODAY - d
INTERVAL_DAYS = int(sys.argv[1])
PERCENT = float(sys.argv[2])

def predict_value(STOCK, interval_days=INTERVAL_DAYS):
    #------------- predict next day value -------------#
    ## download data from last six months ##
    d = datetime.timedelta(days=interval_days)
    start_date = TODAY - d
    data = yf.download(STOCK,datetime.date.strftime(start_date, "%Y-%m-%d"),datetime.date.strftime(TODAY, "%Y-%m-%d")) 

    ## extract closing data ##
    closing_data = data.Close

    training_data = []
    for d_idx, c_d in enumerate(closing_data):

        try:
            data_vec = [closing_data[d] for d in range(d_idx, d_idx+6)]
            

            training_data.append(data_vec)
        except IndexError:
            break

    ## save data for read-in ##
    a = np.asarray(training_data)
    np.savetxt("pred_data_cache.csv", a, delimiter=",")

    results = np.transpose(training_data)[-1]


    ## load in dataset ##
    dataset = DataFormatterv1.Format("./pred_data_cache.csv", names=['a', 'b', 'c', 'd', 'e', 'f'])

    list_of_columns = [
        list(dataset.a.tolist()),
        list(dataset.b.tolist()),
        list(dataset.c.tolist()),   
        list(dataset.d.tolist()),
        list(dataset.e.tolist()),
        list(dataset.f.tolist())
    ]

    predict = training_data[-1][0:-1]
    ## expected value 5.530000209808349609e+00
    (bounds, history) = IterativeApproximation.IterativeApproximation(dataset, predict, list_of_columns, start_v = np.mean(results), second_v=1.5*np.mean(results), num_iter=25, show_graph=False)

    return bounds, history



t0 = time.time()

#------------- load in recommendation csv -------------#
_fpath = f'five_dollar_stock_prediction_{datetime.date.strftime(TODAY, "%Y-%m-%d")}_{INTERVAL_DAYS}-{PERCENT}percent.csv'
recommendations = DataFormatterv1.Format(_fpath, names=["ticker+pred", "confidence", "recommendation"])


#------------- compile prediction dictionary -------------#
pre_dict = { ## key is ticker, assoc. w/ prev close, predict price, lower bound, upper bound, actual close, percent error, delta mu (money made or lost per share)
}
for idx, ticker_unformatted in enumerate(recommendations['ticker+pred']):

    recommendation = recommendations['recommendation'][idx]
    if recommendation.strip() == 'IGNORE' or recommendations.confidence[idx]<0.80:
        continue

    ticker = ticker_unformatted.split()[0].strip(':')

    ticker_dict = {'ticker':ticker}

    ticker_dict['confidence'] = recommendations['confidence'][idx]

    ## get previous close ##
    ticker_yahoo = yf.Ticker(ticker)
    todayData = ticker_yahoo.history(period='1d')
    last_quote = todayData['Close'][0]
    ticker_dict['prev_close'] = last_quote

    ## predict price ##
    bounds, history = predict_value(ticker)

    ticker_dict['prediction'] = np.mean(bounds)

    pre_dict[ticker] = ticker_dict

## save csv ##
keys = pre_dict[list(pre_dict.keys())[0]].keys()
with open(f'prediction_spreadsheet_{INTERVAL_DAYS}_{datetime.date.strftime(TODAY, "%Y-%m-%d")}_{PERCENT}.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows([pre_dict[key] for key in list(pre_dict.keys())])


print(f"Total time to complete: {time.time()-t0}")