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


async def get_price(coin, return_symbol=False, p='last_price'):

    info = client.Market.Market_symbolInfo().result()

    keys = info[0]['result']
    symbols = []
    symbol = coin
    for key in keys:
        if key['symbol'] == coin: 
            # print(key)
            coin_price = key[p]
            symbol = coin

        elif key['symbol'] == coin+"USDT": 
            # print(key)
            coin_price = key[p]
            symbol = coin+"USDT"
        elif key['symbol'] == coin+"/USDT": 
            # print(key)
            coin_price = key[p]
            symbol = coin+"/USDT"
        elif key['symbol'] == coin[1:]+"/USDT":
            coin_price = key[p]
            symbol = coin[1:]+"/USDT"
        elif coin in key['symbol']:
            coin_price = key[p]
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


async def get_previous_order_value():

    trades = await exchange.fetchClosedOrders()
    order = trades[-1]

    print(order)

    price = float(order['info']['cummulativeQuoteQty'])

    await exchange.close()

    return price



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


async def print_info(coin):

    info = client.Market.Market_symbolInfo().result()

    keys = info[0]['result']
    symbols = []
    for key in keys:
        if key['symbol'] == coin: 
            print(key)
            print(f"24 hour high: {key['high_price_24h']}")
            print(f"Upper bound: {(float(key['low_price_24h']) + (float(key['high_price_24h']) + float(key['low_price_24h']))/2.)/2.}")
            print(f"CURRENT PRICE: {key['last_price']}")
            print(f"24 hour low: {key['low_price_24h']}")
            print(f"Change (1h): {float(key['price_1h_pcnt'])*100}%")
            print(f"Change (24h): {float(key['price_24h_pcnt'])*100}%")
            print("===="*10)
            print(f"Current price lower than upper bound? {float(key['last_price']) < (float(key['low_price_24h']) + (float(key['high_price_24h']) + float(key['low_price_24h']))/2.)/2.}")
            print(f"Hour change greater than 0.2%: {float(key['price_1h_pcnt']) > 0.002}")
            print(f"Day change greater than 1%: {float(key['price_24h_pcnt']) > 0.01}")
            coin_price = key['bid_price']
            coin_price = key['ask_price']
            break
        symbols.append(key['symbol'])


async def check_coin_lower_part_day(coin):

    coin = coin+'USDT'

    info = client.Market.Market_symbolInfo().result()
    keys = info[0]['result']
    symbols = []
    for key in keys:
        if key['symbol'] == coin: 
            price = float(key['last_price'])
            symbol = key['symbol'].split('USD')[0]

            high = float(key['high_price_24h'])
            low = float(key['low_price_24h'])

            pct24 = float(key['price_24h_pcnt'])
            pct1 = float(key['price_1h_pcnt'])

            # return price > (low + (high + low)/2.)/2.:
            return price < (high + low)/2.

async def main():

    # p, a = await get_order('ENSUSDT')
    # await exchange.close()
    # print(p, a)

    # await get_allowable_sell_amount('AGLDUSDT', 57.2603, 0.413)
    await print_info(sys.argv[1])

if __name__ == '__main__':
    asyncio.run(main())