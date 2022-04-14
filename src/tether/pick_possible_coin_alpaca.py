import os
import pandas as pd
import urllib.request

import numpy as np


coins = [
"AAVEUSD",
"BATUSD",
"BTCUSD",
"BCHUSD",
"LINKUSD",
"DAIUSD",
"DOGEUSD" ,
"ETHUSD",
"GRTUSD",
"LTCUSD",
"MKRUSD",
"MATICUSD",
"PAXGUSD" ,
"SHIBUSD" ,
"SOLUSD",
"SUSHIUSD" ,
"USDTUSD" ,
"TRXUSD",
"UNIUSD",
"WBTCUSD",
"YFIUSD" 
]

header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
    'AppleWebKit/537.11 (KHTML, like Gecko) '
    'Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


# link = "https://www.google.com/finance/quote/{0}-USD"
link = "https://www.marketwatch.com/investing/cryptocurrency/{0}/charts"
# link = "https://www.coingecko.com/en/coins/{0}/usd"

def download_data(coin):

    req = urllib.request.Request(url=link.format(coin), headers=header)
    html = str(urllib.request.urlopen(req).read())
    with open("t.txt", "w") as f:
        f.write(html)


    splitstr_phrase ='''priceChangePercent'''


    percent_day = float(html.split(splitstr_phrase)[1].split("%")[0][3:])
    return percent_day


def get_price(coin):
    req = urllib.request.Request(url=link.format(coin), headers=header)
    html = str(urllib.request.urlopen(req).read())
    with open("t.txt", "w") as f:
        f.write(html)

    # splitstr_phrase ='''<span class="V53LMb" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" focusable="false" class=" NMm5M"><path d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"/></svg></span>'''
    splitstr_phrase ='''"price"'''
    price = float(html.split(splitstr_phrase)[1].split('''"p''')[0][2:-2])

    return price

def return_changes():
    changes = []
    for coin in coins:

        print(coin)
        percent_change = download_data(coin)

        print(percent_change)
        changes.append(percent_change)


    ranked_changes = np.array(coins)[np.argsort(changes)][::-1]
    changes = np.array(changes)[np.argsort(changes)][::-1]
    print(changes)
    print(ranked_changes)

    return changes, ranked_changes




if __name__ == '__main__':
    # print(get_price("AAVEUSD"))
    return_changes()
