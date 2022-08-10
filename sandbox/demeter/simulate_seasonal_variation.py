import numpy as np
import datetime
import yfinance as yf


import matplotlib.pyplot as plt

seasons_dict = {
    'winter':['12-01','03-01',1], ## start date, end date, year change
    'spring':['03-01','05-30', 0],
    'summer':['06-01','09-30', 0],
    'fall':['10-01','12-05', 0]
}

seasons = ['spring', 'summer', 'fall', 'winter']

seasons_tickers = {
    'winter':'LNG',
    'spring':'FSI',
    'summer':'CHGG',
    'fall':'LII'
}

#------------- simulation parameters -------------#
START_MONEY = 4000 ## dollars
START_DATE = '2005-03-01'
START_DATE_OBJ = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')


CURRENT_EQUITY = START_MONEY

equity = [CURRENT_EQUITY]
dates = [START_DATE_OBJ]


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


class Portfolio(object):

    def __init__(self, cash=0, start_date=START_DATE_OBJ, ticker=None):

        self.cash = cash
        self.shares = 0
        self.ticker = ticker
        self.start_date = start_date
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

    def next_day(self, update=True):

        if update:
            self.update_series()

        date_plus_1 = self.current_date+datetime.timedelta(days=1)
        self.current_date = date_plus_1
        print(f"Updated date. Current date: {self.current_date}.")

    def get_current_price(self):

        data = yf.download(self.ticker, start=self.current_date, end=self.current_date+datetime.timedelta(days=10))
        closing_data = data.Close
        return closing_data[0]

        # return access.access(self.ticker, f"{self.current_date.year}-{str(self.current_date.month).zfill(2)}-{str(self.current_date.day).zfill(2)}")

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





#------------- simulation -------------#
YEAR = 2016
YEARS = 2
dates = []
cash_t = []

for y in range(YEARS):

    for season in seasons:

        start_date = f'{str(YEAR+y)}-'+seasons_dict[season][0]
        end_date = f'{YEAR+y+seasons_dict[season][2]}-'+seasons_dict[season][1]

        ## create simulation ##
        NewPortfolio = Portfolio(cash=CURRENT_EQUITY, start_date=datetime.datetime.strptime(start_date, "%Y-%m-%d"))

        
        ## buy stocks at BEGINNING of season ##
        NewPortfolio.ticker = seasons_tickers[season]
        if YEAR + y < 2014 and season == 'summer': NewPortfolio.ticker = 'CINF'
        NewPortfolio.buy_shares(1e8)
        NewPortfolio.update_series()

        ## skip to end of season ##
        while NewPortfolio.current_date < datetime.datetime.strptime(end_date, "%Y-%m-%d"):
            NewPortfolio.next_day(update=False)

        ## sell shares ##
        NewPortfolio.update_series()
        NewPortfolio.sell_shares(1e8)
        NewPortfolio.next_day()


        ## update equity ##
        CURRENT_EQUITY = NewPortfolio.cash
        dates.append(NewPortfolio.current_date)
        cash_t.append(NewPortfolio.cash)

        NewPortfolio.print_portfolio()

    # CURRENT_EQUITY += 3500

NewPortfolio.sell_shares(1e8)
NewPortfolio.print_portfolio()

plt.plot(dates, cash_t)
plt.xlabel("Date")
plt.ylabel("Cash in account")
# plt.yscale('log')
plt.show()