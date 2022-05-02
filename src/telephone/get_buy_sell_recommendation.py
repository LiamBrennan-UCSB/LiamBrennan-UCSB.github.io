#------------- imports -------------#
from binance.websockets import BinanceSocketManager
from binance.client import Client
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

import pick_possible_coin_alpaca as ppc

import alpaca_trade_api as tradeapi
alpaca_api_key = 'AKCYO5AWGOLPSUT509MG'
alpaca_api_secret = 'fxTTP9MQiEKBYt94tKe0ieUGbR53YVqy2zsSevXK'

api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, api_version='v2')
account = api.get_account()
print(account)

if float(account.cash) < 100:
    print("Too little cash!")
    sys.exit(0)

previous_order_value = float(api.get_activities()[0].price)*float(api.get_activities()[0].qty)
if previous_order_value < 100.:
    previous_order_value = 100.

print ("[{0}][previous_order_value: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), previous_order_value))

coins = [
"BATUSD",
"BTCUSD",
"BCHUSD",
"LINKUSD",
"DAIUSD",
"DOGEUSD" ,
"ETHUSD",
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

    url = "https://bitgur.com/coin/{0}".format(coin)

    req = urllib.request.Request(url=url, headers=header)
    html = str(urllib.request.urlopen(req).read())

    splitStrList = ['EMA5', 'EMA10', 'EMA20', 'EMA50', 'EMA100']

    buys, sells = 0, 0

    for splitStr in splitStrList:
        recommend = html.split(splitStr)[1][0:250]
        if 'sell' in recommend:
            recommend = 'sell'
            sells += 1
        elif 'buy' in recommend:
            recommend = 'buy'
            buys += 1
        else:
            print("Something weird happened. Skipping.")
            print(recommend)
        print(f"{splitStr}: {recommend}")

    url = "https://bitgur.com/coin/{0}/prediction".format(coin)

    req = urllib.request.Request(url=url, headers=header)
    html = str(urllib.request.urlopen(req).read())

    splitStr = "Next 24 hours brief prediction</h3>"

    try:
        raise_not = html.split(splitStr)[1][0:200]

        if "RAISE" in raise_not:
            raise_not = "raise"
        else:
            raise_not = "not"
    except IndexError:
        raise_not = "not"
    print(raise_not)

    if buys > sells+1 and raise_not == "raise":
        return "buy"
    else:
        return 'sell'



def main():

    COIN_TO_BUY = None

    for coin in coins:
        print(f"Coin: {coin}")
        recommendation = get_recommendation(coin.split('USD')[0])
        print(f"Recommendation for {coin}: {recommendation}")

        if recommendation == "buy":
            COIN_TO_BUY = coin

            break

    if COIN_TO_BUY is not None:
        print(f"Buying {COIN_TO_BUY}")
        print(f"python -c {COIN_TO_BUY} -s {100} -g 0.01")
        os.system(f"python c3po.py -c {COIN_TO_BUY} -s {previous_order_value} -g 0.01")





if __name__ == '__main__':
    main()