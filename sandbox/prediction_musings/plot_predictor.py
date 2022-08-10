import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import matplotlib.pyplot as plt
import scipy.stats
import datetime

from yahoo_fin import stock_info as si
import access_offline_data as access



TICKER = 'BBIG'
START_DATE = '2020-01-01'
SIMULATED_START = '2021-09-27'
END_DATE = '2021-10-04'
TEST_DATE_MINUS_1 = '2021-10-04'
TEST_DATE = '2021-10-05'

NUM_DAYS_MEAN = 5


## get list of symbols ##
with open("all_symbols_under5.txt", "r") as sym_f:
    lines = sym_f.readlines()
symbols = [line.strip('\n') for line in lines]



r_s = []
good_tickers = []
for TICKER in symbols:
    try:
        data = access.access_range(TICKER, START_DATE, END_DATE)
    except FileNotFoundError:
        continue
    mean_perdiffs = []
    deltas = []
    for d, date in enumerate(list(data.keys())[0:-NUM_DAYS_MEAN-1]):

        data_subset = [float(data[k]) for k in list(data.keys())[d:d+NUM_DAYS_MEAN]]
        next_day_change = float(data[list(data.keys())[d+NUM_DAYS_MEAN+1]]) - float(data[list(data.keys())[d+NUM_DAYS_MEAN]])
        diffs = np.diff(data_subset) / data_subset[1:] 

        mean_perdiffs.append(np.sum(diffs))
        deltas.append(next_day_change)


    # fit = np.polyfit(mean_perdiffs, deltas, 1)
    # print(fit)
    # pfit = np.poly1d(fit)
    if len(deltas) < 5:
        continue
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(mean_perdiffs, deltas)

    # print(slope, r_value)

    r_s.append(r_value)

    if abs(r_value) > 0.10: 
        print("Found good one.")
        plt.title(TICKER)
        plt.plot(mean_perdiffs, slope*np.array(mean_perdiffs)+intercept)
        # plt.plot(mean_perdiffs, pfit(mean_perdiffs))
        plt.scatter(mean_perdiffs, deltas)
        plt.xlabel(f"mean percent diffs for previous {NUM_DAYS_MEAN} days")
        plt.ylabel("Change the next day")
        plt.ylim(-1, 1)
        plt.show()

        add = input("Use? (y/n)\n")
        if add.lower() in ['n', 'no']:
            continue
        else:
            good_tickers.append((TICKER, slope, intercept))


plt.hist(r_s)
plt.show()



## for every good stock; predict the next day ##
for package in good_tickers:

    ticker, slope, intercept = package

    data = access.access_range(ticker, SIMULATED_START, END_DATE)

    data_subset = [float(data[k]) for k in list(data.keys())]
    diffs = np.diff(data_subset) / data_subset[1:]     

    prediction = slope*np.sum(diffs) + intercept

    if prediction < 0:
        continue

    next_day = access.access(ticker, TEST_DATE)
    day_before = access.access(TICKER, TEST_DATE_MINUS_1)

    actual = (next_day - day_before) / day_before

    # print(f"Prediction: {prediction}; actual: {actual}")

    predicted_sign = np.sign(prediction)
    actual_sign = np.sign(actual)

    print(f"Predicted sign, actual sign: {predicted_sign}, {actual_sign}")




