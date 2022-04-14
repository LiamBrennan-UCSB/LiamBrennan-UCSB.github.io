import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import matplotlib.pyplot as plt
import scipy.stats
import datetime

from yahoo_fin import stock_info as si

def get_current_price(symbol):

    return si.get_live_price(symbol)

    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

t0 = time.time()

START_DATE = '2005-01-01'
END_DATE = '2022-01-01'

TODAY = True

_DATA_DIR = './offline_data/'

## get list of symbols ##
with open("all_symbols_under5.txt", "r") as sym_f:
    lines = sym_f.readlines()
symbols = [line.strip('\n') for line in lines]
symbols.append('GME')
print(symbols)

## download data and save to file ##
for s, symbol in enumerate(symbols[symbols.index('AAU'):]):

    # if s%80 == 0:
    #     print("Sleeping to trick Yahoo.")
    #     time.sleep(10)

    print(f"Downloading {symbol}.")
    ## download ##
    data = yf.download(symbol, start=START_DATE, end=END_DATE, threads= False)
    closing_data = data.Close

    print(closing_data)

    try:
        print(closing_data['2021-06-22'])
    except KeyError:
        continue

    print(f"Saving {symbol}.")
    
    with open(f"{_DATA_DIR}/{symbol}.txt", "w") as d_fil:
        for key in closing_data.keys():
            string = f"{key.year}-{str(key.month).zfill(2)}-{str(key.day).zfill(2)}, {closing_data[key]}\n"
            d_fil.write(string)

        if TODAY:
            current_price = get_current_price(symbol)
        #     # stock = yf.Ticker("ABEV3.SA")
        #     # data1= stock.info
        #     # current_price = np.mean([data1['bid'], data1['ask']])
            string = f"{key.year}-{str(key.month).zfill(2)}-{str(key.day+1).zfill(2)}, {current_price}\n"
            d_fil.write(string)

print(f"Download completed in {time.time()-t0} seconds.")