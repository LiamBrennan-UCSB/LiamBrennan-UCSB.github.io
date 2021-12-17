import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import matplotlib.pyplot as plt
import scipy.stats


def probability_curve_generator(ticker):

    ## download data from last six months ##
    data = yf.download(ticker,'2021-05-02','2021-11-02') 

    ## extract closing data ##
    closing_data = data.Close

    LENGTH = len(closing_data)

    days_ago = []
    probs = []
    for i in reversed(range(20, LENGTH-1, 1)):
        
        days_ago.append(-i)

        ## grab timespan ##
        timespan = closing_data[-i:-1]

        ## roll and subtract ##
        deltas = timespan - np.roll(timespan, 1)

        ## chop off first erraneous point ##
        deltas = deltas[1:]

        ## get truths ##
        above_zero = deltas > 0


        ## calculate probability ##
        probs.append(above_zero.sum()/len(above_zero))



    z = np.polyfit(days_ago, probs, 1)
    p = np.poly1d(z)


    print("Slope: ", z[-1])
    print("X^2: ", scipy.stats.chisquare(p(days_ago), probs)[0])
    print("Predicted probability for next 5 days:", p(5))

    return z[-1], scipy.stats.chisquare(p(days_ago), probs)[0], p(5)



## get list of tickers ##
## scrape list of best stocks under $5 ##
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
    'AppleWebKit/537.11 (KHTML, like Gecko) '
    'Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

url = "https://stocksunder5.org/nyse-stocks-under-5/"
req = urllib.request.Request(url=url, headers=header)
page = urllib.request.urlopen(req).read()
table = pd.read_html(page)

symbols = table[5].Symbol
symbols = [symbol.split()[0] for symbol in symbols]
print(symbols)


output = []
for symbol in symbols:

    slope, chi, pred = probability_curve_generator(symbol)
    if slope < 0: continue
    if chi < 0.2: continue
    if pred < 0.5: continue
    output.append(f"{symbol}, {slope}, {chi}, {pred}\n")

with open("output-dec-16.csv", "w") as op_f:
    op_f.write("Symbol, Slope, Chi-square, Prediction\n")
    for line in output:
        op_f.write(line)
