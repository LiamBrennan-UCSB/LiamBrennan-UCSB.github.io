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
import get_buy_sell_recommendation as gbsr

#------------- grab command line arguments -------------#
parser = argparse.ArgumentParser()
parser.add_argument('--coin', '-c', help="the coin you want to buy", type=str)
parser.add_argument('--spend', '-s', help="the amount of cash you want to use to buy the coin", type= float, default=None)
parser.add_argument('--gain', '-g', help="percent to wait to gain before selling", type=float, default=0.01)
args = parser.parse_args()

COIN = str(args.coin)
SPEND = float(args.spend)
GAIN = float(args.gain)

print("I am C3PO, human-cyborg relations.")


#------------- log into alpaca -------------#
alpaca_api_key = 'AKCYO5AWGOLPSUT509MG'
alpaca_api_secret = 'fxTTP9MQiEKBYt94tKe0ieUGbR53YVqy2zsSevXK'

api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, api_version='v2')
account = api.get_account()
print(account)


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
    req = urllib.request.Request(url=link.format(coin), headers=header)
    html = str(urllib.request.urlopen(req).read())
    with open("t.txt", "w") as f:
        f.write(html)

    # splitstr_phrase ='''<span class="V53LMb" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" focusable="false" class=" NMm5M"><path d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"/></svg></span>'''
    splitstr_phrase ='''"price"'''
    price = float(html.split(splitstr_phrase)[1].split('''"p''')[0][2:-2].replace(',', ''))

    return price

coin_price = get_price(COIN)
print("Current price of coin: $", coin_price)


#------------- buy coin using cash specified -------------#
if SPEND is None:
    SPEND = float(account.non_marginable_buying_power)

def buy(coins=1):

    api.submit_order(
      symbol=COIN, # Replace with the ticker of the stock you want to buy
      qty=coins,
      side='buy',
      type='market', 
      time_in_force='gtc', # Good 'til cancelled
    )

    


quantity = int(SPEND / coin_price)-1
print(quantity)
buy(quantity)

buy_time = time.time()
print ("[{0}][buy_time: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), buy_time))

time.sleep(5)

#------------- get buy price -------------#
while 1:
    try:
        BUY_PRICE = float(api.get_activities()[0].price)
        break
    except requests.exceptions.HTTPError:
        print("Something weird happened--I couldn't connect to Alpaca to get activities.")
        time.sleep(10)

print ("[{0}][BUY_PRICE: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), BUY_PRICE))
#------------- sell coin after pricepoint reached -------------#

def sell(coins=1):


    t0 = time.time()
    api.submit_order(
      symbol=COIN, # Replace with the ticker of the stock you want to buy
      qty=coins,
      side='sell',
      type='market', 
      time_in_force='gtc', # Good 'til cancelled
    )
    print(f"Sale completed in {time.time()-t0} seconds.")




#------------- set up binance -------------#

def process_message(msg):

    current_price = float(msg['p'])
    print ("[{0}][current_price: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), current_price))
    print(f"Percent above: {(current_price-BUY_PRICE)/BUY_PRICE}")

    if current_price > (1.+GAIN) * BUY_PRICE:
        sell(quantity)
        print(f"Time to sell: {(time.time() - buy_time) / 60.} minutes.")
        os.system("killall python3")
        os.system("killall python")
    elif current_price < BUY_PRICE * 0.993:
        recommendation = gbsr.get_recommendation(COIN)
        if recommendation == 'sell':
            sell(quantity)
            print(f"Time to sell: {(time.time() - buy_time) / 60.} minutes.")
            os.system("killall python3")
            os.system("killall python")
    elif current_price < BUY_PRICE * 0.982:
        print("Stop-loss activated. Selling.")
        sell(quantity)


binance_api_key ="DvuDXaDBmVwrr7SxSbUME21PoYfBLwfxx2LfeIRlgxebtbTw3gw3jaM0veMzEJTU"
binance_api_secret ="MMcpYWesOC4v5q7E91ot8SQjo3qYMCXzSw5sfMQ2T1b6srUWOpiNKDRTBH75Fnw7"
client = Client(binance_api_key, binance_api_secret)

bm = BinanceSocketManager(client)
conn_key = bm.start_trade_socket(COIN+'T', process_message)

bm.start()