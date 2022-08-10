import asyncio
import os
from random import randint
import sys
import time
from pprint import pprint
import numpy as np

import ccxt.async_support as ccxt  # noqa: E402


print('CCXT Version:', ccxt.__version__)

exchange = ccxt.bybit({
    'apiKey': 'u9WMNvH1ELEIvlRRJc',
    'secret': 'RtbMQ6q5WCSTIsQXX2E5XGA5zSx7MqUxs5kS',
})

exchange.options['defaultType'] = 'spot'; # very important set spot as default type



import bybit

client = bybit.bybit(test=False, api_key="u9WMNvH1ELEIvlRRJc", api_secret="RtbMQ6q5WCSTIsQXX2E5XGA5zSx7MqUxs5kS")


async def buy(coin, quantity):


    info = client.Market.Market_symbolInfo().result()

    keys = info[0]['result']
    symbols = []
    print(coin)
    for key in keys:

        if key['symbol'] == coin: 
            print(key)
            coin_price = key['ask_price']
            break
        symbols.append(key['symbol'])


    print("Current price ", coin_price)


    # create limit order
    try:
        symbol = coin.split('USD')[0]+'/USDT'
        t = 'limit'
        side = 'buy'
        amount = quantity
        price = float(coin_price)
        create_order = await exchange.create_order(symbol, t, side, amount, 1.01*price)
        print('Create order id:', create_order['id'])

    except:
        symbol = coin.split('USD')[0]+'USDT'
        t = 'limit'
        side = 'buy'
        amount = 0.9987*quantity
        price = float(coin_price)
        create_order = await exchange.create_order(symbol, t, side, amount, 1.003*price)
        print('Create order id:', create_order['id'])


async def sell(coin, quantity):
    info = client.Market.Market_symbolInfo().result()

    keys = info[0]['result']
    symbols = []
    for key in keys:
        if key['symbol'] == coin: 
            print(key)
            coin_price = key['bid_price']
            coin_price = key['ask_price']
            break
        symbols.append(key['symbol'])


    print("Current price ", coin_price)


    # create limit order
    try:
        try:
            symbol = coin.split('USD')[0]+'/USDT'
            t = 'limit'
            side = 'sell'
            amount = quantity
            price = float(coin_price)
            create_order = await exchange.create_order(symbol, t, side, amount, 0.996*price)
            print('Create order id:', create_order['id'])

        except:
            symbol = coin.split('USD')[0]+'USDT'
            t = 'limit'
            side = 'sell'
            amount = quantity
            price = float(coin_price)
            create_order = await exchange.create_order(symbol, t, side, amount, 0.996*price)
            print('Create order id:', create_order['id'])
    except:
        try:
            symbol = coin.split('USD')[0]+'/USDT'
            t = 'limit'
            side = 'sell'
            amount = quantity
            price = float(coin_price)
            create_order = await exchange.create_order(symbol, t, side, amount, 0.99*price)
            print('Create order id:', create_order['id'])

        except:
            symbol = coin.split('USD')[0]+'USDT'
            t = 'limit'
            side = 'sell'
            amount = quantity
            price = float(coin_price)
            create_order = await exchange.create_order(symbol, t, side, amount, 0.996*price)
            print('Create order id:', create_order['id'])


async def get_price(coin, return_symbol=False):

    info = client.Market.Market_symbolInfo().result()

    keys = info[0]['result']
    symbols = []
    symbol = coin
    for key in keys:
        if key['symbol'] == coin: 
            # print(key)
            coin_price = key['last_price']
            symbol = coin

        elif key['symbol'] == coin+"USDT": 
            # print(key)
            coin_price = key['last_price']
            symbol = coin+"USDT"
        elif key['symbol'] == coin+"/USDT": 
            # print(key)
            coin_price = key['last_price']
            symbol = coin+"/USDT"
        elif key['symbol'] == coin[1:]+"/USDT":
            coin_price = key['last_price']
            symbol = coin[1:]+"/USDT"
        elif coin in key['symbol']:
            coin_price = key['last_price']
            symbol = key['symbol']
        symbols.append(key['symbol'])

    if return_symbol:
        return float(coin_price), symbol
    return float(coin_price)


async def get_order(coin):

    trades = await exchange.fetchClosedOrders()
    order = trades[-1]

    print(order)

    price = float(order['info']['avgPrice'])
    amount = float(order['amount'])

    await exchange.close()

    return price, amount


async def get_allowable_sell_amount(coin, start_qty, price):

    ## test making fake order ##
    for factor in np.linspace(1.008, 0.95, 100):
        try:
            symbol = coin.split('USD')[0]+'USDT'
            t = 'limit'
            side = 'sell'
            create_order = await exchange.create_order(symbol, t, side, factor*start_qty, 10.*price)
            oi = create_order['id']
            print('Create order id:', oi)

            ## test cancelling order ##
            await exchange.cancelOrder(oi, symbol)

            print("It worked! You can sell this much: ", factor*start_qty)

            return factor*start_qty
        except:
            print("Didn't work :( trying a smaller sell amount.")



async def main():

    # p, a = await get_order('ENSUSDT')
    # await exchange.close()
    # print(p, a)

    await get_allowable_sell_amount('AGLDUSDT', 57.2603, 0.413)

if __name__ == '__main__':
    asyncio.run(main())