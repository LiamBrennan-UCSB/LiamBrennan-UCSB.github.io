import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import matplotlib.pyplot as plt
import scipy.stats
import datetime

START_DATE = '2019-01-01'
END_DATE = '2021-12-15'

_DATA_DIR = './offline_data/'

## get list of symbols ##
with open("all_symbols_under5.txt", "r") as sym_f:
    lines = sym_f.readlines()
symbols = [line.strip('\n') for line in lines]
print(symbols)

## download data and save to file ##
for symbol in symbols:

    print(f"Downloading {symbol}.")
    ## download ##
    data = yf.download(symbol, start=START_DATE, end=END_DATE)
    closing_data = data.Close

    print(f"Saving {symbol}.")
    
    # with open(f"{_DATA_DIR}/{symbol}.txt", "w") as d_fil:
    #     for key in closing_data.keys():
    #         string = f"{key.year}-{str(key.month).zfill(2)}-{str(key.day).zfill(2)}, {closing_data[key]}\n"
    #         d_fil.write(string)

