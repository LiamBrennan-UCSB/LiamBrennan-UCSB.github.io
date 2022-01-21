import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as si

# authentication and connection details PAPER
# api_key = 'PKJXO4HQPZI4UUFADXK4'
# api_secret = 'yeFtyDCi95H7lThIVu5pwS6xNA8FK04hCqbCjnmX'
# base_url = 'https://paper-api.alpaca.markets'

# authentication and connection details LIVE
api_key = 'AKPID22IGN3D2RHONGGY'
api_secret = 'rIXkKio71riZrAxTz6EjZ0zsW9GyMsyAN4ZkX94q'
base_url = 'https://api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()
print(account)


TICKERS = ['GMDA', 'RETO']

# total_money = 10100
total_money = 94

for ticker in TICKERS:

  current_price = si.get_live_price(ticker)
  money_fraction = total_money / len(TICKERS)

  qty = int(0.98*(money_fraction / current_price))

  api.submit_order(
    symbol=ticker, # Replace with the ticker of the stock you want to buy
    qty=qty,
    side='buy',
    type='market', 
    time_in_force='gtc' # Good 'til cancelled
  )