from binance.websockets import BinanceSocketManager
from binance.client import Client
import alpaca_trade_api as tradeapi
import sys
import numpy as np
import time
import requests
import pick_possible_coin_alpaca as pcp

import matplotlib.pyplot as plt

coins = [
"AAVEUSD",
"BATUSD",
"BTCUSD",
"BCHUSD",
"LINKUSD",
"DAIUSD",
"DOGEUSD" ,
"ETHUSD",
"GRTUSD",
"LTCUSD",
"MKRUSD",
"MATICUSD",
"PAXGUSD" ,
"SHIBUSD" ,
"SOLUSD",
"SUSHIUSD" ,
"USDTUSD" ,
"TRXUSD",
"UNIUSD",
"WBTCUSD",
"YFIUSD" 
]



binance_api_key ="DvuDXaDBmVwrr7SxSbUME21PoYfBLwfxx2LfeIRlgxebtbTw3gw3jaM0veMzEJTU"
binance_api_secret ="MMcpYWesOC4v5q7E91ot8SQjo3qYMCXzSw5sfMQ2T1b6srUWOpiNKDRTBH75Fnw7"
client = Client(binance_api_key, binance_api_secret)

alpaca_api_key = 'AKCYO5AWGOLPSUT509MG'
alpaca_api_secret = 'fxTTP9MQiEKBYt94tKe0ieUGbR53YVqy2zsSevXK'

api = tradeapi.REST(alpaca_api_key, alpaca_api_secret, api_version='v2')
account = api.get_account()
print(account)

CASH_FRAC = 0.1
COINS_OWNED = 0

COIN = None

api = tradeapi.REST(key_id= alpaca_api_key, secret_key=alpaca_api_secret) # For real trading, don't enter a base_url

def buy(coins=1, price=None):
    global COINS_OWNED

    if coins == None:
        coins = int(CASH_FRAC * np.floor(float(account.non_marginable_buying_power)) / price) - 1
        print(f"Buying {coins}")


    api.submit_order(
      symbol=COIN, # Replace with the ticker of the stock you want to buy
      qty=coins,
      side='buy',
      type='market', 
      time_in_force='gtc', # Good 'til cancelled
    )

    COINS_OWNED = coins

def sell(coins=1, price=None):


    t0 = time.time()
    api.submit_order(
      symbol=COIN, # Replace with the ticker of the stock you want to buy
      qty=coins,
      side='sell',
      type='market', 
      time_in_force='gtc', # Good 'til cancelled
    )
    print(f"Sale completed in {time.time()-t0} seconds.")



def change_coin():

    global COIN

    COIN = None

    while 1:
        changes, ranked_changes = pcp.return_changes()

        for c, crypto in enumerate(ranked_changes):

            if changes[c] > 0.25:

                price = pcp.get_price(crypto)
                if price < 10 and price > 0.05:
                    print(f"Picked coin: {crypto}")
                    print(f"Change today: {changes[c]}")
                    COIN = crypto
                    break

        if COIN is not None:
            break

        else:
            print("None of the coins satisfied me. I'll sleep for 5 minutes and check again.")
            time.sleep(300)



def buy_or_sell_or_hold(series, show=False):

    '''
    THREE MARKERS

    - Derivative: is the price about to CHANGE DIRECTION? Derivative goes to zero.
    - Curvature: if the curvature is >0 (U) BUY. If curvature <0 (n) SELl. 
    - ~~Slope before/after d=0: if the slope is different before and after derivative this confirms price change. perform action.~~
    '''

    DECISION = 'HOLD'
    vertex_in_range = False

    print(series)
    fit = np.polyfit(range(len(series)), series, 2)
    f = np.poly1d(fit)

    a, b, c = fit
    print(a, b, c)

    ## where is teh vertex? (0 derivative point)
    vertex = -b/(2*a)
    if vertex > 0.92*len(series) and vertex < 0.98*len(series):

        vertex_in_range = True

    else:
        return 'HOLD', vertex, f

    ## what is the curvature?
    curvature = np.sign(a)
    if curvature > 0:
        DECISION = 'BUY'
    elif curvature < 0:
        DECISION = 'SELL'
    else:
        'HOLD', vertex, f 

    if show:
        plt.clf()
        plt.plot(series)

        plt.plot(range(len(series)), f(range(len(series)),))
        plt.axvline(vertex)
        plt.savefig("./test.jpg")

        # plt.show()



    return DECISION, vertex, f


## keep track of the moving average here ##
## acts as a buffer, is erased at the beginning of each BUY cycle ##
history = []

## flags to check if its time to buy/sell ##
BUY = True
SELL = False
BUY_PRICE = -1
START_TIME = None
def process_message(msg):
    global BUY, SELL, history, COINS_OWNED, BUY_PRICE, START_TIME

    if START_TIME is None:
        START_TIME = time.time()


    elapsed_time = abs(time.time() - START_TIME)

    print("Current Price: {}".format(msg['p']))
    if elapsed_time < 3600:
        history.append(float(msg['p']))
    elif elapsed_time >= 3600:
        history.append(float(msg['p']))
        del history[0]

        if SELL:
            try:
                BUY_PRICE = float(api.get_activities()[0].price)
            except requests.exceptions.HTTPError:
                print("Something weird happened--I couldn't connect to Alpaca to get activities.")


        DECISION, vertex, f = buy_or_sell_or_hold(history, show=False)
        if DECISION == 'BUY' and BUY and np.mean(history[-3:-1]) < 1.25*np.min(history):
            buy(coins=None, price=float(msg['p']))
            BUY = False
            SELL = True
            BUY_PRICE = float(api.get_activities()[0].price)
        elif DECISION == 'SELL' and SELL and np.mean(history[-3:-1]) > 1.0075*BUY_PRICE:
            sell(COINS_OWNED)
            SELL = False
            BUY = True
            change_coin()
        elif SELL and np.mean(history[-5:-1]) > 1.01*BUY_PRICE:
            sell(COINS_OWNED)
            SELL = False
            BUY = True
            change_coin()
        elif SELL and np.mean(history[-5:-1]) < 0.95*BUY_PRICE:
            print("Emergency sell--price went 5% below BUY.")
            sell(COINS_OWNED)
            SELL = False
            BUY = True
            change_coin()
        else:
            print("Doing nothing")
        plt.clf()
        plt.plot(history)

        plt.plot(range(len(history)), f(range(len(history)),))
        plt.axvline(vertex)
        if BUY_PRICE > 0:
            plt.axhline(BUY_PRICE)
        plt.title(f"{DECISION}, buy price: {BUY_PRICE}")
        plt.savefig("./test.jpg")




change_coin()


bm = BinanceSocketManager(client)
conn_key = bm.start_trade_socket(COIN+'T', process_message)

bm.start()


# x = np.linspace(0, 10, 300) + np.random.random(size=300)
# y = (x-1)**2.

# buy_or_sell_or_hold(y)