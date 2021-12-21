import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as si

# authentication and connection details LIVE
api_key = 'PKFNFY03E1757WU6LTB5'
api_secret = 'v4nOmTn0iXaufa75juRTHMizKLGsjijIA2xEZX4i'
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()
print(account)


TICKERS = ['BGI', 'SINO', 'HYMC', 'CNEY', 'HMY', 'PLG', 'BKCC']
total_money = 10000

for ticker in TICKERS:

  current_price = si.get_live_price(ticker)
  money_fraction = total_money / len(TICKERS)

  qty = int(0.98*(money_fraction / current _price))

  api.submit_order(
    symbol=ticker, # Replace with the ticker of the stock you want to buy
    qty=qty,
    side='buy',
    type='market', 
    time_in_force='gtc' # Good 'til cancelled
  )