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


TICKER_WITH_MARKET_DATA = 'ACER'
YEARS = [2015, 2020]
_DATA_DIR = './offline_data/'


def get_start_end_date(month, year):

    ## get start date ##
    start_date = str(year)+'-'+str(month).zfill(2)
    for day in range(30):

        start_date_with_day = start_date + '-' + str(day).zfill(2)

        try:
            access.access(TICKER_WITH_MARKET_DATA, start_date_with_day)
        except KeyError:
            continue

        start_date = start_date_with_day
        break

    ## get end date ##
    end_date = str(year)+'-'+str(month).zfill(2)
    for day in range(30, 0, -1):

        end_date_with_day = end_date + '-' + str(day).zfill(2)

        try:
            access.access(TICKER_WITH_MARKET_DATA, end_date_with_day)
        except KeyError:
            continue

        end_date = end_date_with_day
        break

    return start_date, end_date


def get_change_over_month(ticker, month):

    ## get start year ##
    with open(f'{_DATA_DIR}/{ticker}.txt', "r") as o_f:
        line = o_f.readline()
    
    earliest_year = int(line.split()[0].split('-')[0]) + 1

    percent_diffs = []
    for year in range(earliest_year, YEARS[-1]+1):

        if year < YEARS[0]: continue
        print(year)

        start_date, end_date = get_start_end_date(month, year)

        start_price = float(access.access(ticker, start_date))
        end_price = float(access.access(ticker, end_date))

        percent_diffs.append((end_price-start_price)/start_price)

    # print(percent_diffs)
    if len(percent_diffs) < 2:
        return -10000, -10000

    print(percent_diffs)
    return np.median(percent_diffs), np.std(percent_diffs)



def main():

    ## unit testing ##

    get_start_end_date(1, 2005)
    for i in range(1, 12):
        print(get_change_over_month('ACER', i))


if __name__ == '__main__':
    main()