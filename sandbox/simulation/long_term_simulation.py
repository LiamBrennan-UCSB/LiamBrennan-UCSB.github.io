import numpy as np
import access_offline_data as access
import datetime
import prev_5_day_behavior as p5
import apollo_prediction as ml


import matplotlib.pyplot as plt

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def warning(message):
        print (bcolors.WARNING + "[" + message + "]" + bcolors.ENDC)

    @staticmethod
    def success(message):
        print (bcolors.OKGREEN + "[" + message + "]" + bcolors.ENDC)

    @staticmethod
    def failure(message):
        print (bcolors.FAIL + "[" + message + "]" + bcolors.ENDC)

START_MONEY = 10000 ## dollars
START_DATE = '2021-02-01'
START_DATE_OBJ = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
DAYS = 100

CURRENT_EQUITY = START_MONEY

equity = [CURRENT_EQUITY]
dates = [START_DATE_OBJ]

class Portfolio(object):

    def __init__(self, cash=0, start_date=START_DATE_OBJ, ticker=None):

        self.cash = cash
        self.shares = 0
        self.ticker = ticker
        self.start_date = START_DATE_OBJ
        self.current_date = self.start_date
        self.portfolio_value = 0
        self.initial_buy_price = 0

        self.series = {'dates':[], 'shares':[], 'cash':[], 'portfolio':[]}

        print("Portfolio initialized.")
        if self.ticker is not None:
            self.print_portfolio()

    def print_portfolio(self):

        print(f"Current date: {self.current_date}")
        print(f"Current cash: ${self.cash}.")
        print(f"Current shares of {self.ticker} owned: {self.shares}.")
        print(f"Current value of portfolio: ${self.shares*self.get_current_price()}")

    def update_series(self):

        try:
            self.portfolio_value = self.shares * self.get_current_price()
        except KeyError:
            self.portfolio_value = self.series['portfolio'][-1]

        self.series['dates'].append(self.current_date)
        self.series['shares'].append(self.shares)
        self.series['cash'].append(self.cash)
        self.series['portfolio'].append(self.portfolio_value)

        print("Series updated.")

    def next_day(self):

        self.update_series()

        date_plus_1 = self.current_date+datetime.timedelta(days=1)
        self.current_date = date_plus_1
        print(f"Updated date. Current date: {self.current_date}.")

    def get_current_price(self):

        return access.access(self.ticker, f"{self.current_date.year}-{str(self.current_date.month).zfill(2)}-{str(self.current_date.day).zfill(2)}")

    def buy_shares(self, num_shares):

        ## get current price ##
        current_price = self.get_current_price()
        self.initial_buy_price = current_price

        ## get cash required ##
        buy_cost = num_shares * current_price
        if buy_cost > self.cash:

            max_shares = np.floor(self.cash / current_price)

            print(f"Cost of buying shares (${buy_cost}) greater than available cash (${self.cash}). Buying {max_shares} shares instead.")

            num_shares = max_shares
            buy_cost = num_shares * current_price

        ## buy shares ##
        self.cash -= buy_cost
        self.shares += num_shares

        print("Shares bought.")
        self.print_portfolio()

    def sell_shares(self, num_shares):

        ## get current price ##
        current_price = self.get_current_price()

        ## get cash required ##
        sell_price = num_shares * current_price
        if num_shares > self.shares:

            print(f"Trying to buy more shares ({num_shares}) than are available ({self.shares}). Selling all shares.")

            sell_price = self.shares * current_price
            num_shares = self.shares

        ## sell shares ##
        self.cash += sell_price
        self.shares -= num_shares

        print("Shares sold.")
        self.print_portfolio()


    def plot_series(self, quantity):

        plt.plot(range(len(self.series['dates'])), self.series[quantity])
        plt.xlabel("Days")
        plt.ylabel(quantity)
        plt.title(self.start_date)
        plt.show()


def decide_to_sell(portfolio):

    max_val = max(portfolio.series['portfolio'])

    if portfolio.get_current_price() < 0.97*max_val:
        return 0.5

    elif portfolio.get_current_price() < 0.98*max_val:
        return 0.2    

    elif portfolio.get_current_price() < 0.99*max_val:
        return 0.1  


    else:
        return 0.0

#------------- test 100 day simulation -------------#

# STOCK = 'NEW'
# NewPortfolio = Portfolio(cash=START_MONEY, start_date=START_DATE_OBJ, ticker=STOCK)

# NewPortfolio.buy_shares(1e8)

# for day in range(DAYS):

#     NewPortfolio.next_day()

#     try:
#         print("Testing current price $", NewPortfolio.get_current_price())
#     except KeyError:
#         print("Stock market closed. Skipping today.")
#         NewPortfolio.next_day()
#         continue

#     NewPortfolio.sell_shares(decide_to_sell(NewPortfolio)*NewPortfolio.shares)

# NewPortfolio.next_day()


#------------- extended simulation -------------#

dates = []
cash = []

ITERATIONS = 100
for iteration in range(ITERATIONS):

    ## start portfolio
    NewPortfolio = Portfolio(cash=START_MONEY, start_date=START_DATE_OBJ)


    ## pick stock ##
    # stocks =  ml.get_recommended_symbols(f"{NewPortfolio.current_date.year}-{str(NewPortfolio.current_date.month).zfill(2)}-{str(NewPortfolio.current_date.day).zfill(2)}", tickers=p5.get_recommended_symbols(f"{NewPortfolio.current_date.year}-{str(NewPortfolio.current_date.month).zfill(2)}-{str(NewPortfolio.current_date.day).zfill(2)}"))
    stocks = p5.get_recommended_symbols(f"{NewPortfolio.current_date.year}-{str(NewPortfolio.current_date.month).zfill(2)}-{str(NewPortfolio.current_date.day).zfill(2)}")

    ticker = stocks[0]
    print ("[{0}][ticker: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), ticker))
    
    ## assign stock ##
    NewPortfolio.ticker = ticker

    ## buy shares ##
    NewPortfolio.buy_shares(1e8)

    ## iterate portfolio ##
    for day in range(DAYS):

        NewPortfolio.next_day()

        try:
            print("Testing current price $", NewPortfolio.get_current_price())
        except KeyError:
            print("Stock market closed. Skipping today.")
            NewPortfolio.next_day()
            continue

        NewPortfolio.sell_shares(decide_to_sell(NewPortfolio)*NewPortfolio.shares)

        if NewPortfolio.shares < 1:
            NewPortfolio.sell_shares(1e5)
            START_MONEY = NewPortfolio.cash
            START_DATE_OBJ = NewPortfolio.current_date
            break

    NewPortfolio.print_portfolio()
    # input()

    dates.append(NewPortfolio.current_date)
    cash.append(NewPortfolio.cash)



plt.plot(range(len(dates)), cash)
plt.xlabel("Days")
plt.ylabel("cash")
# plt.title(.start_date)
plt.show()