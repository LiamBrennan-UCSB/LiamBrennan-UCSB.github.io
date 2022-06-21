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
alpaca_api_key = 'AKO5B5A1S2E3DSGPKUTZ'
alpaca_api_secret = 'v7tg8zmIN4gtRr5DtD4s77JSw495m2tHxUGec7Ga'

api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, api_version='v2')
account = api.get_account()
print(account)

if float(account.cash) < 100:
    print("Too little cash!")
    sys.exit(0)

try:
    previous_order_value = float(api.get_activities()[0].price)*float(api.get_activities()[0].qty)
except AttributeError:
    previous_order_value = 100 
if previous_order_value < 100.:
    previous_order_value = 100.

print ("[{0}][previous_order_value: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), previous_order_value))

coins = [
"BATUSD",
# "BTCUSD",
# "BCHUSD",
"LINKUSD",
# "DAIUSD",
"DOGEUSD" ,
# "ETHUSD",
"LTCUSD",
"MKRUSD",
"MATICUSD",
"SOLUSD",
"TRXUSD",
"UNIUSD",
]



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

    for coin in coins:
        print(f"Coin: {coin}")
        recommendation = get_recommendation(coin.split('USD')[0])
        print(f"Recommendation for {coin}: {recommendation}")
        
        
        if recommendation['buy']:
            COIN_TO_BUY = coin
            rec = recommendation

            break

    if COIN_TO_BUY is not None:
        print(f"Buying {COIN_TO_BUY}")
        print(f"python -c {COIN_TO_BUY} -s {100} -g 0.01")
        os.system(f"python c3po.py -c {COIN_TO_BUY} -s {previous_order_value} -g {rec['stop-profit']} -l {rec['stop-loss']}")





if __name__ == '__main__':
    main()