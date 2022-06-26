# from pybit import spot
# from pybit import HTTP


# ws_spot = spot.WebSocket(
#     test=True,
#     api_key="ECjEx2pZKc7wB2WVDx",  # omit the api_key & secret to connect w/o authentication
#     api_secret="6plQszU2LBaiUpbHO6S2geBr0OF6Ab0g7n8r",
#     # to pass a custom domain in case of connectivity problems, you can use:
#     domain="bybit"  # the default is "bybit"
# )

# session = HTTP('https://api.bybit.com',  api_key="ECjEx2pZKc7wB2WVDx", api_secret="6plQszU2LBaiUpbHO6S2geBr0OF6Ab0g7n8r")

# session.place_active_order(
#     symbol="DOGEUSDT",
#     side="Buy",
#     order_type="Market",
#     qty=0.000004,
#     time_in_force="GoodTillCancel",
#     reduce_only=False,
#     close_on_trigger=False
# )


# print(client.Order.Order_new(side="Buy", symbol="DOTUSD", order_type="Limit", qty=  0.001, price=dot_price, time_in_force="GoodTillCancel").result())




import asyncio
import os
from random import randint
import sys
from pprint import pprint

import ccxt.async_support as ccxt  # noqa: E402


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
    if key['symbol'] == 'DOTUSD': 
        print(key)
        dot_price = key['last_price']
    symbols.append(key['symbol'])


print("Current price ", dot_price)

exchange.options['defaultType'] = 'spot'; # very important set spot as default type


# create limit order
symbol = 'DOT/USDT'
t = 'limit'
side = 'buy'
amount = 0.196*10
price = float(dot_price)
create_order = await exchange.create_order(symbol, t, side, amount, 1.1*price)
print('Create order id:', create_order['id'])


info = client.Market.Market_symbolInfo().result()

keys = info[0]['result']
symbols = []
for key in keys:
    print(key['symbol'])
    if key['symbol'] == 'DOTUSD': 
        print(key)
        dot_price = key['last_price']
    symbols.append(key['symbol'])


print("Current price ", dot_price)


# create limit order
symbol = 'DOT/USDT'
t = 'limit'
side = 'sell'
amount = 0.195*10
price = float(dot_price)
create_order = await exchange.create_order(symbol, t, side, amount, 0.99*price)
print('Create order id:', create_order['id'])
