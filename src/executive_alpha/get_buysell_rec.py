#------------- imports -------------#
import alpaca_trade_api as tradeapi
import sys
import numpy as np
import time
import requests
import matplotlib.pyplot as plt
import argparse
import urllib
import datetime
import os

import alpha 

import alpaca_trade_api as tradeapi

previous_order_value = 30
print ("[{0}][previous_order_value: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), previous_order_value))

coins = [
"BAT",
# "BTC",
# "BCH",
"LINK",
# "DAI",
"DOGE" ,
# "ETH",
"LTC",
"MATIC",
"SOL",
"TRX",
"UNI",
]


with open("Coins.txt", "r") as cf:
    lines = cf.readlines()

coins = [line.replace("\n", "") for line in lines]
print(coins)



header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
    'AppleWebKit/537.11 (KHTML, like Gecko) '
    'Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


def get_recommendation(coin):

    recommendation = alpha.executive_alpha(coin)

    if recommendation is False:

        return False

    else:
        return recommendation



def main():

    COIN_TO_BUY = None
    rec = None

    for c, coin in enumerate(coins):

        if c%30 == 0:
            time.sleep(30)
        print(f"Coin: {coin}")
        try:
            recommendation = get_recommendation(coin.split('USD')[0])
        except:
            time.sleep(30)
        print(f"Recommendation for {coin}: {recommendation}")
        
        
        if recommendation['buy']:
            COIN_TO_BUY = coin
            rec = recommendation

            break

    if COIN_TO_BUY is not None:
        print(f"Buying {COIN_TO_BUY}")
        os.system(f"python c3po.py -c {COIN_TO_BUY} -s {previous_order_value} -g {rec['stop-profit']} -l {rec['stop-loss']}")





if __name__ == '__main__':
    main()