#------------- imports -------------#
import yagmail
import datetime
import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as si
import numpy as np
import sys
import time

import matplotlib.pyplot as plt


#------------- communication protocol info -------------#
FROM_EMAIL = "stonkoclonk@gmail.com"
FROM_PASS = "9d2bk8PNseQtQsAs"
yag = yagmail.SMTP(FROM_EMAIL, FROM_PASS)

RECIPIENTS_EMAILS = [
    "3239079063@vtext.com",
    # "liamb7144@gmail.com"
]


#------------- market information -------------#
MARKET_OPEN_PST = "06:30:00"
MARKET_CLOSE_PST = "13:00:00"
AFTERMARKET_OPEN_PST = "13:00:01"
AFTERMARKET_CLOSE_PST = "16:00:00"

MARKET_STATUS = "OPEN" ## options: OPEN, CLOSED, AFTER, HOLIDAY


#------------- alpaca information -------------#
api_key = 'AKPID22IGN3D2RHONGGY'
api_secret = 'rIXkKio71riZrAxTz6EjZ0zsW9GyMsyAN4ZkX94q'
base_url = 'https://api.alpaca.markets'
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')


def get_current_price(symbol):

    return round(si.get_live_price(symbol), 3)


def get_open_positions():

    position_tickers = []

    positions = api.list_positions()
    for position in positions:
        position_tickers.append(position.symbol)


    return position_tickers

def get_current_portfolio_value():

    return float(api.get_account().portfolio_value)

def get_current_time():
    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")

    return current_time


def send_message(contents, subject='SENTRY', attachments=[]):

    contents.append("Current time: {0}".format(get_current_time()))

    for recipient in RECIPIENTS_EMAILS:
        yag.send(recipient, subject, contents)


def send_sell_alert(ticker, prices):

    contents = []
    current_price = get_current_price(ticker)
    contents.append(f"SELL ALERT: {ticker}")
    contents.append(f"{ticker}: {current_price}")
    contents.append(f"Current price is {round(current_price/max(prices), 3)*100}% of maximum ({round(max(prices),3)})")
    contents.append(f"Link: https://finance.yahoo.com/quote/{ticker}")

    send_message(contents, subject='SELL')

# send_sell_alert("GME", 100*np.sin(np.linspace(0, 8, 100)))
# sys.exit(1)

#------------- STARTUP -------------#

send_message(["==============="])

send_message(["Welcome to the >>Sentry Stock Market Live-Monitoring Protocol<<"]) ## send startup message to all recipients

send_message(["Market status:", MARKET_STATUS]) ## send market status

startup_tickers = get_open_positions()
send_message([f"Current open positions: {startup_tickers}"]) ## show which positions are open

current_prices = [f"{ticker}: {get_current_price(ticker)}" for ticker in startup_tickers]

send_message(["Current prices", current_prices]) ## show current prices for each position

send_message(["Portfolio value", str(get_current_portfolio_value())]) ## show current portfolio value


asset_day_behavior = {}
for ticker in startup_tickers:
    asset_day_behavior[ticker] = {'t':[], 'p':[]} ## time and price


try:

    while True:


        #------------- GET POSITIONS -------------#

        tickers = get_open_positions()
        print("Tickers to monitor: ", tickers)


        # ------------- MARKET OPEN BEHAVIOR -------------#



        # ------------- MARKET CLOSE BEHAVIOR -------------#



        # ------------- HOURLY BEHAVIOR -------------#



        #------------- FREQUENT BEHAVIOR -------------#
        DELAY = 10 ## seconds

        # if MARKET == "OPEN":
        time.sleep(DELAY)

        print("Checking on stocks.")

        for ticker in tickers:

            ## append current price to dataset ##
            current_price = get_current_price(ticker)
            asset_day_behavior[ticker]['p'].append(current_price)

            ## grab maximum for day so far ##
            max_price = np.max(asset_day_behavior[ticker]['p'])

            ## is current price less than 3% of max? ##
            if current_price < 1.01*max_price:
                print("Sending sell alert.")
                send_sell_alert(ticker, asset_day_behavior[ticker]['p'])








        #------------- UNIT TESTING BEHAVIOR -------------#

except KeyboardInterrupt:
    print("Loop exited manually.")

print(asset_day_behavior)