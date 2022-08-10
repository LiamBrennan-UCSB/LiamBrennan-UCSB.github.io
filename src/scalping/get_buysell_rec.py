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
import asyncio
import bybit_buy_sell as bbs
import scrape_tradingview as st

import alpaca_trade_api as tradeapi

if len(sys.argv) > 1:
    part = sys.argv[1]



def get_recommendation(coin):

    recommendation = alpha.executive_alpha(coin)

    if recommendation is False:

        return False

    else:
        return recommendation



async def main():

    previous_order_value = await bbs.get_previous_order_value()
    if previous_order_value < 40:
        previous_order_value = 40
    print ("[{0}][previous_order_value: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), previous_order_value))


    COIN_TO_BUY, _ = st.scan_market()

    if COIN_TO_BUY is not None:

        print(f"Buying {COIN_TO_BUY}")
        os.system(f"python c3po.py -c {COIN_TO_BUY} -s {previous_order_value} -g {0.005} -l {-0.06}")

    elif COIN_TO_BUY is None:
        time.sleep(900)
        await main()

    print("No coin selected, not buying.")



if __name__ == '__main__':
    asyncio.run(main())