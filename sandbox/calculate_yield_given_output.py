import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta

## matplotlib settings ##
import matplotlib.pyplot as plt
plt.style.use('classic')
import matplotlib as mpl
import matplotlib.font_manager as font_manager
mpl.rcParams['font.family']='serif'
cmfont = font_manager.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')
mpl.rcParams['font.serif']=cmfont.get_name()
mpl.rcParams['mathtext.fontset']='cm'
mpl.rcParams['axes.unicode_minus']=False
colors = ['green', 'orange', 'cyan', 'darkred']
plt.rcParams.update({'font.size': 14}) 




import pandas_datareader as pdr

import yfinance as yf
from yahoo_fin import stock_info as si

TODAY = datetime.today().strftime('%Y-%m-%d')
YESTERDAY = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')

output_file = "five_dollar_stock_prediction_11-03-2021.csv"

output_csv = pd.read_csv(output_file, header=None)

tickers_6mo, ignore_or_look_6mo = output_csv[0], output_csv[2]
previous_day_close, current_price = [], []

ignore = {}
look = {}

for idx, ticker in enumerate(tickers_6mo): 

    print(ticker)
    info = pdr.get_data_yahoo(symbols=ticker.split()[0].strip(":"), start=datetime(2021, 3, 1), end=YESTERDAY)
    print(info.Close[-1])
    # print(si.get_live_price(ticker.split()[0].strip(":")))
    previous_day_close.append(info.Close[-1])
    current_price.append(si.get_live_price(ticker.split()[0].strip(":")))

    i_o_l = ignore_or_look_6mo[idx].split()[0].strip()

    if i_o_l == 'IGNORE': 
        ignore[ticker.split()[0].strip(":")] = {'previous_close':info.Close[-1], 'current_price':si.get_live_price(ticker.split()[0].strip(":"))}

    elif i_o_l == 'LOOK':
        look[ticker.split()[0].strip(":")] = {'previous_close':info.Close[-1], 'current_price':si.get_live_price(ticker.split()[0].strip(":"))}
    else:
        print("Check your sanitizing!")

    print(i_o_l.split()[0].strip())


for ticker in list(look.keys()):

    plt.scatter(look[ticker]["previous_close"], 100*(look[ticker]["current_price"] - look[ticker]["previous_close"])/look[ticker]["previous_close"], c='green', s=80)

plt.axvline(0)
plt.axhline(0)

plt.xlim(-8, 8)
plt.ylim(-8, 8)

plt.xlabel("Previous close")
plt.ylabel("Percent change")
plt.title("Tag: LOOK")
plt.show()


for ticker in list(ignore.keys()):

    plt.scatter(ignore[ticker]["previous_close"], 100*(ignore[ticker]["current_price"] - ignore[ticker]["previous_close"])/ignore[ticker]["previous_close"], c='red', s=80)

plt.axvline(0)
plt.axhline(0)

plt.xlim(-8, 8)
plt.ylim(-8, 8)
plt.xlabel("Previous close")
plt.ylabel("Percent change")
plt.title("Tag: IGNORE")
plt.show()
