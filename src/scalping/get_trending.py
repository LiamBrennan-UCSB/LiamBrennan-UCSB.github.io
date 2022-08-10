#------------- imports -------------#
import asyncio
import os
from random import randint
import sys
import time
from pprint import pprint
import numpy as np
import datetime 
from tqdm import tqdm

import ccxt.async_support as ccxt  # noqa: E402


print('CCXT Version:', ccxt.__version__)

exchange = ccxt.bybit({
    'apiKey': 'u9WMNvH1ELEIvlRRJc',
    'secret': 'RtbMQ6q5WCSTIsQXX2E5XGA5zSx7MqUxs5kS',
})

exchange.options['defaultType'] = 'spot'; # very important set spot as default type



import bybit

client = bybit.bybit(test=False, api_key="u9WMNvH1ELEIvlRRJc", api_secret="RtbMQ6q5WCSTIsQXX2E5XGA5zSx7MqUxs5kS")

# bad_coin_list = ['MTLUSDT', 'BANDUSDT']

with open(f"Coins_part0.txt", "r") as cf:
    lines = cf.readlines()

good_coin_list = [line.replace("\n", "") for line in lines]

# print(good_coin_list)


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


async def get_trending():

    info = client.Market.Market_symbolInfo().result()
    
    keys = info[0]['result']

    symbols, pct1s = [], []

    best_symbol, best_pct1 = None, -9999999
    best2_symbol, best2_pct1 = None, -9999999

    for key in tqdm(keys):

        # print(key)


        price = float(key['last_price'])
        symbol = key['symbol'].split('USD')[0]
        if has_numbers(symbol): continue
        if symbol not in good_coin_list: 
            continue

        # print(price, symbol)

        high = float(key['high_price_24h'])
        low = float(key['low_price_24h'])

        pct24 = float(key['price_24h_pcnt'])
        pct1 = float(key['price_1h_pcnt'])

        BUY = True

        if price > (low + (high + low)/2.)/2.:
        # if price > (high + low)/2.:
            # print("Buy price is too high.")
            BUY = True

        if pct1 < 0.002:
            # print("Price decreasing in last hour.")
            BUY = False

        if pct24 < 0.01:
            # print("Price didn't rise enough in the last day.")
            BUY = False

        if BUY:
            symbols.append(symbol)
            pct1s.append(pct1)

            if pct1 > best_pct1:
                print(f"New best symbol is {symbol} with {round(pct1*100, 3)}% increase.")
                best2_symbol = best_symbol
                best2_pct1 = best_pct1
                best_symbol = symbol
                best_pct1 = pct1

    if best2_symbol is not None:
        return best2_symbol, best2_pct1

    return best_symbol, best_pct1


async def main():
    best_symbol, best_pct1 = await get_trending()
    print ("[{0}][best_symbol: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), best_symbol))
    print ("[{0}][best_pct1: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), best_pct1))

    


if __name__ == '__main__':
    asyncio.run(main())