import alpaca_trade_api as tradeapi
import os
import pandas as pd
import time
import datetime

t0 = time.time()

####### PAPER TRADING #######
api_key = 'PKXQ2EJUCK102RZDHN0B'
api_secret = 'ch1dQIEE8OGU1Nhw6KgglJ1yv7nCQKO5UrvPbbTM'
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(key_id= api_key, secret_key=api_secret, base_url=base_url)

#------------- run all scripts -------------#
os.system("rm performance_files.txt")
os.system("touch performance_files.txt")
for percent in [1]:
    os.system(f"python run_all_scripts.py 180 {percent}")


#------------- parse stonks and share numbers -------------#
with open("performance_files.txt", "r") as pf:

    lines = pf.readlines()

_fpaths = [line.strip() for line in lines]

ticker_share_dict = {}
for _fpath in _fpaths:

    csv = pd.read_csv(_fpath)
    
    for t_idx, ticker in enumerate(csv.ticker):
        if ticker.strip() not in list(ticker_share_dict.keys()): ticker_share_dict[ticker.strip()] = []
        ticker_share_dict[ticker.strip()].append(int(csv.num_shares[t_idx]))


#------------- sell shares -------------#
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=3)
YESTERDAY = YESTERDAY.replace(hour=1, minute=00, second=00)

## grab shares bought yesterday ##
orders = api.list_orders('all', after=YESTERDAY)
buy_orders = [order for order in orders if order.side=='buy']
buy_orders_tickers = [order.symbol for order in buy_orders]
buy_orders_qty = [order.filled_qty for order in buy_orders]

print(buy_orders_tickers)


for t_idx, ticker in enumerate(buy_orders_tickers):

    qty = buy_orders_qty[t_idx]

    print(f"Selling {qty} shares of {ticker}.")

    
    try:
        api.submit_order(
            symbol=ticker, # Replace with the ticker of the stock you want to buy
            qty=qty,
            side='sell',
            type='market', 
            time_in_force='gtc' # Good 'til cancelled
            )
    except:
        print(r"Couldn't sell {qty} shares of {ticker}.")

#------------- buy shares -------------#

account = api.get_account()
for ticker in list(ticker_share_dict.keys()): 

    if float(account.cash) < 9.99: 
        print("Not enough money left.")
        break

    print(f"Cash left: ${account.cash}")

    if ticker in buy_orders_tickers: 
        continue

    qty = max(ticker_share_dict[ticker])



    print(f"Buying {qty} shares of {ticker}.")

    api.submit_order(
        symbol=ticker, # Replace with the ticker of the stock you want to buy
        qty=qty,
        side='buy',
        type='market', 
        time_in_force='gtc' # Good 'til cancelled
    )    


print(f"Trading bot took {(time.time()-t0)/60.} minutes.")