import alpaca_trade_api as tradeapi

# authentication and connection details LIVE
api_key = 'AKKIXOLDZT3LUO5RJ74Q'
api_secret = 'iYOIwLXhIIHQwa6UsVQV2PcYjLoWJNGxWNWoWhCu'
base_url = 'https://api.alpaca.markets'

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()
print(account)

api = tradeapi.REST(key_id= api_key, secret_key=api_secret) # For real trading, don't enter a base_url

api.submit_order(
  symbol='BORR', # Replace with the ticker of the stock you want to buy
  qty=1,
  side='sell',
  type='market', 
  time_in_force='gtc' # Good 'til cancelled
)

## matplotlib settings ##
import matplotlib.pyplot as plt
plt.style.use('classic')
import matplotlib as mpl
import matplotlib.font_manager as font_manager
mpl.rcParams['font.family']='serif'
cmfont = font_manager.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')
mpl.rcParams['font.serif']=cmfont.get_name()
mpl.rcParams['mathtext.fontset']='cm'
mpl.rcParams['axes.unicode_minus']=False
colors = ['green', 'orange', 'cyan', 'darkred']
plt.rcParams.update({'font.size': 10}) 


