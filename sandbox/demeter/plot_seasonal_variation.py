#------------- imports -------------#
import sys
import datetime
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt 

#------------- grab plotting parameters -------------#
if len(sys.argv) == 1:
    STOCK = 'HD'
    SEASON = 'spring'

else:
    STOCK = sys.argv[1]
    SEASON = sys.argv[2]

YEARS = [2010, 2020]

#------------- define seasons -------------#
seasons_dict = {
    'winter':['12-01','03-01',1], ## start date, end date, year change
    'spring':['03-01','05-30', 0],
    'summer':['06-01','09-30', 0],
    'fall':['10-01','12-05', 0],
}


def get_data_range(ticker, start_date, end_date):

    ## convert data into proper range ##
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    data = yf.download(ticker, start_date, end_date) 

    ## extract closing data ##
    closing_data = data.Close

    return closing_data

def convert_season_to_dates(season, year):

    start_date = f'{str(year)}-'+seasons_dict[season][0]
    end_date = f'{year+seasons_dict[season][2]}-'+seasons_dict[season][1]

    return start_date, end_date

offset = 0.1
deltas = []
percents = []
for year in range(YEARS[0], YEARS[1]+1):

    data = get_data_range(STOCK, *convert_season_to_dates(SEASON, year))
    prices = np.array([d for d in data if not np.isnan(d)])

    ## normalize ##
    norm_prices = (prices-np.min(prices))/np.max(prices-np.min(prices))
    plt.plot(norm_prices+offset, label=f'Year: {year}; $\Delta$=\${round(prices[-1]-prices[0], 4)}')
    deltas.append(round(prices[-1]-prices[0], 4))
    percents.append((prices[-1]-prices[0])/prices[0])
    offset += 1


plt.title(f"TICKER: {STOCK}; SEASON: {SEASON}; YEARS: {YEARS[0]}-{YEARS[1]}; $\mu_\Delta=$\${round(np.median(deltas), 4)}; PC DIFF: {100*round(np.median(percents), 4)}")
plt.legend()
plt.show()