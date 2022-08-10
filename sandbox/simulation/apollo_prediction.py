import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import datetime
import access_offline_data as access

## load in ML algorithm ##
import sys
sys.path.insert(0, '../../modules/apollo/src/core/')

import DataFormatterv1
import ClassificationNetv1


TRAINING_RANGE = 180 ## days
EVALUATION_RANGE = 5 ## days


def recommend_stock(ticker, date):

    ## download data from last six months ##
    start_date = datetime.datetime.strptime(date, '%Y-%m-%d')-datetime.timedelta(days=180)
    start_date = f"{start_date.year}-{str(start_date.month).zfill(2)}-{str(start_date.day).zfill(2)}"

    print("DATES:", start_date, date)

    # date = datetime.datetime.strptime(date, '%Y-%m-%d')-datetime.timedelta(days=1)
    # date = f"{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"
    # print(start_date)
    # data = yf.download(ticker, start_date ,date) 

    # ## extract closing data ##
    # closing_data = data.Close

    print ("[{0}][start_date: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), start_date))
    print ("[{0}][date: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), date))

    closing_data = access.access_range(ticker, start_date, date, return_list=True)

    training_data = []
    for d_idx, c_d in enumerate(closing_data):

        try:
            data_vec = [closing_data[d] for d in range(d_idx, d_idx+EVALUATION_RANGE)]

            if 1.001*closing_data[d_idx+4] < closing_data[d_idx+EVALUATION_RANGE]:
                data_vec.append(1.)
            else:
                data_vec.append(0.)
            training_data.append(data_vec)
        except IndexError:
            break


    a = np.asarray(training_data)
    np.savetxt("./training.csv", a, delimiter=",")#, fmt='%1.4f %1.4f %1.4f %1.4f %1.4f %i')





    ## load in ML algorithm ##
    import sys
    sys.path.insert(0, '../modules/apollo/src/core/')

    import DataFormatterv1
    import ClassificationNetv1

    dataset = DataFormatterv1.Format("./training.csv")

    ## test ##
    ## 5.000000000000000000e+00,4.989999771118164062e+00,4.900000095367431641e+00,4.719999790191650391e+00,4.449999809265136719e+00,1.000000000000000000e+00
    # print (ClassificationNetv1.Predict(dataset, 5, [5.000000000000000000e+00,4.989999771118164062e+00,4.900000095367431641e+00,4.719999790191650391e+00,4.449999809265136719e+00]))

    return ClassificationNetv1.Predict(dataset, EVALUATION_RANGE, closing_data[-EVALUATION_RANGE-1:-1])



def get_recommended_symbols(date, tickers=None):

    with open("all_symbols_under5.txt", "r") as sym_f:
        lines = sym_f.readlines()
    symbols = [line.strip('\n') for line in lines]

    if tickers is not None: symbols = tickers

    rec_symbols = []
    deltas = []
    for symbol in symbols:
        print(symbol)

        try:
            if recommend_stock(symbol, date) == 1.:
                rec_symbols.append(symbol)
        except TypeError:
            print("Not using this symbol.")
            deltas.append(-1e10)
            continue

        except FileNotFoundError:
            print("Not using this symbol.")
            deltas.append(-1e10)
            continue

        except:
            continue

        
    # indices = np.array(deltas).argsort()[-10:][::-1]
    # print(np.array(deltas)[indices])
    # print("$"*10)
    # if np.sum(np.array(deltas)[indices]) < 0: return []
    # rec_symbols = [symbols[idx] for idx in indices if deltas[idx] > 0.7]
    # print ("[{0}][rec_symbols: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), rec_symbols))
    return rec_symbols



def main():

    print(recommend_stock('ASRT', '2022-01-04'))
    print(len(get_recommended_symbols('2022-01-04')))


if __name__ == '__main__':
    main()