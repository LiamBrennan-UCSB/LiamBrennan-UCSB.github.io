import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import matplotlib.pyplot as plt
import scipy.stats
import datetime
import access_offline_data as access

import probability_curve_continuous as pcc
import prev_5_day_behavior as p5

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def warning(message):
        print (bcolors.WARNING + "[" + message + "]" + bcolors.ENDC)

    @staticmethod
    def success(message):
        print (bcolors.OKGREEN + "[" + message + "]" + bcolors.ENDC)

    @staticmethod
    def failure(message):
        print (bcolors.FAIL + "[" + message + "]" + bcolors.ENDC)




START_MONEY = 1000 ## dollars
START_DATE = '2021-07-01'
START_DATE_OBJ = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
DAYS = 200

CURRENT_EQUITY = START_MONEY

equity = [CURRENT_EQUITY]
dates = [START_DATE_OBJ]


def stock_picker(date):
    '''given date, pick stocks to invest in'''

    print(f"Picking stocks for date {date}.")

    # return pcc.get_recommended_symbols(date)
    return p5.get_recommended_symbols(date)


def calculate_delta_single_ticker(date, ticker, percent=True):
    '''return how much ticker changed between date and date+1'''

    print(f"Computing delta for {ticker} on {date}.")

    date_plus_1 = datetime.datetime.strptime(date, '%Y-%m-%d')+datetime.timedelta(days=2)
    date_plus_1 = f"{date_plus_1.year}-{str(date_plus_1.month).zfill(2)}-{str(date_plus_1.day).zfill(2)}"

    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = f"{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"

    # data = yf.download(ticker, date,date_plus_1) 
    # closing_data = data.Close

    closing_data = access.access_range(ticker, date, date_plus_1, return_list=True)

    try:
        start_price = closing_data[0]
        end_price = closing_data[1]
    except IndexError:
        print(closing_data)
        print("Weekend or holiday. Market closed. Skipping.")
        # input()
        return "SKIP"

    if percent:
        print((end_price-start_price)/start_price)
        return (end_price-start_price)/start_price


def calculate_delta_sum(date, tickers):
    '''given date and tickers calculate total change'''

    print("Computing deltas.")


    delta_percents = []
    for ticker in tickers:

        delta_percents.append(calculate_delta_single_ticker(date, ticker, percent=True))
        if delta_percents[-1] == 'SKIP':
            print(ticker)
            return 'SKIP'

    return 1.+np.mean(delta_percents)


def update_equity(delta, date=None):

    global CURRENT_EQUITY

    CURRENT_EQUITY *= delta
    bcolors.success(f"Current portfolio value: {CURRENT_EQUITY}")
    equity.append(CURRENT_EQUITY)
    if date is not None: 
        dates.append(date)


previous_day_stocks = []
stocks_picked_vs_dates = []
gains = 0
VOLATILE_WARNING = 0
TWO_DAY_VOLATILE_WARNING = 0
shutdown_activated = 0
for day in range(DAYS):

    if VOLATILE_WARNING > 0:
        VOLATILE_WARNING -= 1
        continue

    ## set current dat  e ##
    current_date = START_DATE_OBJ + datetime.timedelta(days=day)
    current_date = f"{current_date.year}-{str(current_date.month).zfill(2)}-{str(current_date.day).zfill(2)}"

    delta = calculate_delta_sum(current_date, ['GME'])
    if delta == 'SKIP':
        continue

    
    ## pick stocks ##
    stocks = stock_picker(current_date)
    stocks = [stock for stock in stocks if stock not in previous_day_stocks]
    print(current_date, stocks)
    # input()
    previous_day_stocks = stocks
    # print(stocks)

    print(len(stocks))

    if len(stocks) == 0: continue

    ## calculate change ##
    delta = calculate_delta_sum(current_date, stocks)
    print(delta)

    if delta == 'SKIP':
        continue

    if delta > 1.5:
        print(stocks)
        input()

    ## update equity ##
    update_equity(delta, date=datetime.datetime.strptime(current_date, '%Y-%m-%d'))
    stocks_picked_vs_dates.append([datetime.datetime.strptime(current_date, '%Y-%m-%d'), stocks])
    print(stocks)
    print(current_date)
    # input()


    # if CURRENT_EQUITY > 100000:
    #     print(current_date)
    #     print(stocks)
    #     print(previous_day_stocks)
    #     print(delta)
    #     input()
    # if delta < 0.95:
    #     shutdown_activated+=1
    #     VOLATILE_WARNING = 3

    # if delta < 0.97:
    #     TWO_DAY_VOLATILE_WARNING += 1
    #     if TWO_DAY_VOLATILE_WARNING == 2:
    #         VOLATILE_WARNING = 3
    #         TWO_DAY_VOLATILE_WARNING = 0

    # gains += (delta*CURRENT_EQUITY - CURRENT_EQUITY)
    # bcolors.success(f"Current gains: {gains}")

