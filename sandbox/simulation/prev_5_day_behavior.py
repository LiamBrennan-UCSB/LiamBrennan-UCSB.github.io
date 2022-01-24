import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import matplotlib.pyplot as plt
import scipy.stats
import datetime
import random
import os

import access_offline_data as access


def recommend_stock(ticker, date):

    ## download data from last six months ##
    start_date = datetime.datetime.strptime(date, '%Y-%m-%d')-datetime.timedelta(days=10)
    start_date = f"{start_date.year}-{str(start_date.month).zfill(2)}-{str(start_date.day).zfill(2)}"

    print("DATES:", start_date, date)

    # date = datetime.datetime.strptime(date, '%Y-%m-%d')-datetime.timedelta(days=1)
    # date = f"{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"
    # print(start_date)
    # data = yf.download(ticker, start_date ,date) 

    # ## extract closing data ##
    # closing_data = data.Close

    print ("[{0}][start_date: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), start_date))
    print ("[{0}][date: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), date))

    closing_data = access.access_range(ticker, start_date, date, return_list=True)[-6:-1]

    LENGTH = len(closing_data)
    # print("LENGTH", LENGTH)
    # print(closing_data)
    # if LENGTH <= 2: return -1000000
    print ("[{0}][LENGTH: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), LENGTH))

    deltas = []
    for d, day in enumerate(closing_data[1:]):

        deltas.append(day - closing_data[d])

    print("DELTA ", np.mean(deltas))
    return np.mean(deltas)
    if np.mean(deltas) > 0.0:
        return True

    return -100000


def get_recommended_symbols(date):

    with open("all_symbols_under5.txt", "r") as sym_f:
        lines = sym_f.readlines()
    symbols = [line.strip('\n') for line in lines]

    rec_symbols = []
    deltas = []
    for symbol in symbols:
        print(symbol)

        try:
            deltas.append(recommend_stock(symbol, date))
        except TypeError:
            print("Not using this symbol.")
            deltas.append(-1e10)
            continue

        except FileNotFoundError:
            print("Not using this symbol.")
            deltas.append(-1e10)
            continue

        except:
            continue

        
    indices = np.array(deltas).argsort()[-10:][::-1]
    print(np.array(deltas)[indices])
    if np.sum(np.array(deltas)[indices]) < 0: return []
    rec_symbols = [symbols[idx] for idx in indices]
    return rec_symbols


def main():

    print(get_recommended_symbols('2021-1-7'))

if __name__ == '__main__':
    main()