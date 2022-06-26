import asyncio
import os
from random import randint
import sys
from pprint import pprint



import ccxt.async_support as ccxt  # noqa: E402


coin = str(sys.argv[1])
quantity = float(sys.argv[2])


print('CCXT Version:', ccxt.__version__)

exchange = ccxt.bybit({
    'apiKey': 'ECjEx2pZKc7wB2WVDx',
    'secret': '6plQszU2LBaiUpbHO6S2geBr0OF6Ab0g7n8r',
})


import bybit

client = bybit.bybit(test=False, api_key="ECjEx2pZKc7wB2WVDx", api_secret="6plQszU2LBaiUpbHO6S2geBr0OF6Ab0g7n8r")

info = client.Market.Market_symbolInfo().result()

keys = info[0]['result']
symbols = []
for key in keys:
    print(key['symbol'])
    if key['symbol'] == coin: 
        print(key)
        coin_price = key['last_price']
    symbols.append(key['symbol'])


print("Current price ", coin_price)


# create limit order
symbol = coin.split('USD')[0]+'/USD'
t = 'limit'
side = 'buy'
amount = quantity
price = float(coin_price)
create_order = await exchange.create_order(symbol, t, side, amount, 1.1*price)
print('Create order id:', create_order['id'])
