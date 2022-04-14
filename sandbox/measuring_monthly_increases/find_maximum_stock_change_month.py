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

import analyze_for_month as afm



MONTH = 4

## get list of symbols ##
with open("all_symbols_under5.txt", "r") as sym_f:
    lines = sym_f.readlines()
symbols = [line.strip('\n') for line in lines]


lines_to_write = []
for symbol in symbols[symbols.index('CYBN'):]:
    print("Working on ", symbol)
    try:
        median, std = afm.get_change_over_month(symbol, MONTH)
    except FileNotFoundError:
        continue

    lines_to_write.append(f"{symbol}, {median}, {std}\n")

with open("april_penny_analysis_6yearsplus.txt", "w") as apa:
    for line in lines_to_write:
        if '-10000' not in line:
            apa.write(line)


## plot results ##
data = pd.read_csv("april_penny_analysis_6yearsplus.txt", header=None)

for idx, d in enumerate(data[0]):


    print(data[0])
    plt.scatter(data[1][idx], data[2][idx])
    plt.annotate(d, (data[1][idx], data[2][idx]))

plt.xlabel("median")
plt.ylabel("std")
plt.show()