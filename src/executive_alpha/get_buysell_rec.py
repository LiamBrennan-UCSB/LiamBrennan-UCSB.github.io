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
import random
import get_bitgur_rec
import good_buy_time as gbt
import asyncio
import alpha 

import alpaca_trade_api as tradeapi

if len(sys.argv) > 1:
    part = sys.argv[1]

previous_order_value = 50
print ("[{0}][previous_order_value: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), previous_order_value))

# coins = [
# "BAT",
# # "BTC",
# # "BCH",
# "LINK",
# # "DAI",
# "DOGE" ,
# # "ETH",
# "LTC",
# "MATIC",
# "SOL",
# "TRX",
# "UNI",
# ]


with open(f"Coins_part{part}.txt", "r") as cf:
    lines = cf.readlines()

coins = [line.replace("\n", "") for line in lines]
random.shuffle(coins)
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



async def main():

    COIN_TO_BUY = None
    best_coin_prob = -1e8
    rec = None

    while 1:
        bitgur_rec = get_bitgur_rec.get_rec()
        if bitgur_rec == 0:
            time.sleep(300)
            continue
        else:
            break


    for c, coin in enumerate(coins):

        print(f"Current coin to buy: {COIN_TO_BUY} with {best_coin_prob} probability.")
        if c%40 == 0 and c != 0:
            if COIN_TO_BUY is not None:
                break
            time.sleep(30)
        print(f"Coin: {coin}")
        print(f"Index: {c%40}/40")
        try:
            recommendation = get_recommendation(coin.split('USD')[0])
        except:
            time.sleep(30)
        print(f"Recommendation for {coin}: {recommendation}")
        
        
        if recommendation['buy']:
            prob = recommendation['prob']
            if best_coin_prob < prob:
                COIN_TO_BUY = coin
                best_coin_prob = prob
                rec = recommendation


    if COIN_TO_BUY is not None:

        print('1')

        ## wait for optimal time to buy ##
        tstart = time.time()
        while 1:

            print('2')
            elapsed_time = time.time() - tstart
            if elapsed_time > 7200:
                print("Didn't buy because coin never bottomed out.")
                sys.exit(1)
            else:
                buy = await gbt.check_buy_time(COIN_TO_BUY.split('USD')[0])

                if buy: 
                    break
                elif not buy:
                    time.sleep(60)
                    continue




        print(f"Buying {COIN_TO_BUY}")
        os.system(f"python c3po.py -c {COIN_TO_BUY} -s {previous_order_value} -g {rec['stop-profit']} -l {rec['stop-loss']}")






if __name__ == '__main__':
    asyncio.run(main())