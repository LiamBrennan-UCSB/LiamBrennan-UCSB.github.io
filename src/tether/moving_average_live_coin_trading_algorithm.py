from binance.websockets import BinanceSocketManager
from binance.client import Client
import alpaca_trade_api as tradeapi
import sys
import numpy as np
import time

binance_api_key ="DvuDXaDBmVwrr7SxSbUME21PoYfBLwfxx2LfeIRlgxebtbTw3gw3jaM0veMzEJTU"
binance_api_secret ="MMcpYWesOC4v5q7E91ot8SQjo3qYMCXzSw5sfMQ2T1b6srUWOpiNKDRTBH75Fnw7"
client = Client(binance_api_key, binance_api_secret)

alpaca_api_key = 'AKCYO5AWGOLPSUT509MG'
alpaca_api_secret = 'fxTTP9MQiEKBYt94tKe0ieUGbR53YVqy2zsSevXK'

api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, api_version='v2')
account = api.get_account()
print(account)

CASH_FRAC = 0.5
COINS_OWNED = 0


api = tradeapi.REST(key_id= alpaca_api_key, secret_key=alpaca_api_secret) # For real trading, don't enter a base_url

def buy(coins=1, price=None):
    global COINS_OWNED

    if coins == None:
        coins = int(CASH_FRAC * np.floor(float(account.cash)) / price)-1


    api.submit_order(
      symbol='DOGEUSD', # Replace with the ticker of the stock you want to buy
      qty=coins,
      side='buy',
      type='market', 
      time_in_force='gtc', # Good 'til cancelled
    )

    COINS_OWNED = coins

def sell(coins=1, price=None):


    t0 = time.time()
    api.submit_order(
      symbol='DOGEUSD', # Replace with the ticker of the stock you want to buy
      qty=coins,
      side='sell',
      type='market', 
      time_in_force='gtc', # Good 'til cancelled
    )
    print(f"Sale completed in {time.time()-t0} seconds.")



## keep track of the moving average here ##
## acts as a buffer, is erased at the beginning of each BUY cycle ##
history = []

## flags to check if its time to buy/sell ##
BUY = True
SELL = False
BUY_PRICE = 0.00

## counter to go before 

def process_message(msg):
    global BUY, SELL, history, COINS_OWNED, BUY_PRICE


    print("Current Price: {}".format(msg['p']))
    if len(history) < 300:
        history.append(float(msg['p']))
    if len(history) >= 300:
        history.append(float(msg['p']))
        del history[0]

        print(f"HIST AVG {np.mean(history)}")
        if np.mean(history[-50:-1]) < np.mean(history) and BUY:
            print("BUYING")
            BUY_PRICE = float(msg['p'])
            buy(coins=None, price=float(msg['p']))
            BUY = False
            SELL = True

        elif SELL and np.mean(history[-10:-1]) > BUY_PRICE and float(msg['p']) > 1.05*BUY_PRICE:

            print("SELLING")
            sell(coins=COINS_OWNED, price=float(msg['p']))
            BUY = True
            SELL = False
            COINS_OWNED = 0
            history = []



bm = BinanceSocketManager(client)
conn_key = bm.start_trade_socket('DOGEUSDT', process_message)

bm.start()