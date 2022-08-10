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
import bybit_buy_sell as bbs
import asyncio

#------------- grab command line arguments -------------#
parser = argparse.ArgumentParser()
parser.add_argument('--coin', '-c', help="the coin you want to buy", type=str)
parser.add_argument('--spend', '-s', help="the amount of cash you want to use to buy the coin", type= float, default=None)
parser.add_argument('--gain', '-g', help="percent to wait to gain before selling", type=float, default=0.01)
parser.add_argument('--loss', '-l', help="percent to wait to lose before selling", type=float, default=-0.01)
args = parser.parse_args()


async def execute():
    COIN = str(args.coin)
    SPEND = float(args.spend)
    GAIN = float(args.gain)
    LOSS = float(args.loss)

    print("I am C3PO, human-cyborg relations.")


    #------------- log into alpaca -------------#
    alpaca_api_key = 'AKO5B5A1S2E3DSGPKUTZ'
    alpaca_api_secret = 'v7tg8zmIN4gtRr5DtD4s77JSw495m2tHxUGec7Ga'

    api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, api_version='v2')
    account = api.get_account()
    # print(account)


    #------------- grab coin price -------------#
    header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.11 (KHTML, like Gecko) '
        'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}



    link = "https://www.marketwatch.com/investing/cryptocurrency/{0}/charts"
    def get_price(coin):
        req = urllib.request.Request(url=link.format(coin+"USD"), headers=header)
        html = str(urllib.request.urlopen(req).read())
        with open("t.txt", "w") as f:
            f.write(html)

        # splitstr_phrase ='''<span class="V53LMb" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" focusable="false" class=" NMm5M"><path d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"/></svg></span>'''
        splitstr_phrase ='''"price"'''
        price = float(html.split(splitstr_phrase)[1].split('''"p''')[0][2:-2].replace(',', ''))

        return price

    coin_price, COIN = await bbs.get_price(COIN, return_symbol=True)
    print("Current price of coin: $", coin_price)

    old_buy_price = coin_price


    #------------- buy coin using cash specified -------------#
    if SPEND is None:
        SPEND = float(account.non_marginable_buying_power)

    async def buy(coins=1):

        await bbs.buy(COIN, coins)

        


    quantity = float(SPEND / coin_price)
    old_quantity = quantity
    print(quantity)
    await buy(quantity)

    buy_time = time.time()
    print ("[{0}][buy_time: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), buy_time))

    time.sleep(15)

    #------------- get buy price -------------#
    BUY_PRICE, quantity = await bbs.get_order(COIN)

    print ("[{0}][BUY_PRICE: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), BUY_PRICE))


    current_price = await bbs.get_price(COIN)

    if abs((current_price-BUY_PRICE)/BUY_PRICE) > 0.05:

        print("Problems server side for Bybit. Using old price and old quantity.")

        BUY_PRICE = old_buy_price*1.003
        quantity = old_quantity

        print("NEW BUY PRICE")
        print ("[{0}][BUY_PRICE: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), BUY_PRICE))


    #------------- sell coin after pricepoint reached -------------#

    async def sell(coins=1):


        t0 = time.time()
        await bbs.sell(COIN, coins)
        print(f"Sale completed in {time.time()-t0} seconds.")




    #------------- set up binance -------------#

    DEFAULT_GAIN = GAIN

    while 1:
        time.sleep(4)
        try:
            current_price = await bbs.get_price(COIN, p='ask_price')
            current_price = float(current_price)


            print ("[{0}][current_price: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), current_price))

            print(f"Percent above: {(current_price-BUY_PRICE)/BUY_PRICE}")

            # if current_price > (1.+GAIN) * BUY_PRICE or current_price < (1.+LOSS) * BUY_PRICE or time.time() - buy_time > 21600:
            if current_price > (1.+GAIN)*BUY_PRICE:

                LOSS = GAIN - 0.001
                # if LOSS < DEFAULT_GAIN:
                #     LOSS = -0.005
                GAIN += 0.002


                print(f"New gain is {GAIN}.")
                print(f"New loss is {LOSS}.")

            if current_price < (1.+LOSS) * BUY_PRICE:
                
                quantity = await bbs.get_allowable_sell_amount(COIN, quantity, current_price)

                await sell(quantity)
                print(f"Time to sell: {(time.time() - buy_time) / 60.} minutes.")

                os.system("killall python3")
                os.system("killall python")
        except requests.exceptions.ConnectionError:
            print("I think there's a problem with the internet. Gonna try to wait it out.")
            time.sleep(60)

        time.sleep(1)

    await exchange.close()

asyncio.run(execute())
