import alpaca_trade_api as tradeapi

# authentication and connection details
api_key = 'AKKIXOLDZT3LUO5RJ74Q'
api_secret = 'iYOIwLXhIIHQwa6UsVQV2PcYjLoWJNGxWNWoWhCu'
base_url = 'https://api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()
print(account)

api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY) # For real trading, don't enter a base_url

api.submit_order(
  symbol='SPY', # Replace with the ticker of the stock you want to buy
  qty=1,
  side='buy',
  type='market', 
  time_in_force='gtc' # Good 'til cancelled
)