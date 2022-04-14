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

api = tradeapi.REST(key_id= alpaca_api_key, secret_key=alpaca_api_secret) # For real trading, don't enter a base_url


def buy(coins=1):
    api.submit_order(
      symbol='DOGEUSD', # Replace with the ticker of the stock you want to buy
      qty=coins,
      side='buy',
      type='market', 
      time_in_force='gtc' # Good 'til cancelled
    )

def sell(coins=1):
    t0 = time.time()
    api.submit_order(
      symbol='DOGEUSD', # Replace with the ticker of the stock you want to buy
      qty=coins,
      side='sell',
      type='market', 
      time_in_force='gtc' # Good 'til cancelled
    )
    print(f"Sale completed in {time.time()-t0} seconds.")


history = []
BUY = True

def process_message(msg):
    global BUY
    print("Current Price: {}".format(msg['p']))
    if len(history) < 150:
        history.append(float(msg['p']))
    else:
        print(f"HIST AVG {np.mean(history)}")
        if float(msg['p']) < np.mean(history) and BUY:
            print("BUYING")
            buy()
            BUY = False



bm = BinanceSocketManager(client)
conn_key = bm.start_trade_socket('DOGEUSDT', process_message)

bm.start()


## test alpaca buy ##
# authentication and connection details LIVE


