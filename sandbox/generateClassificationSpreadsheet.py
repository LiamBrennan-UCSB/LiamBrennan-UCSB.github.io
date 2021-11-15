import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import datetime
# import threading


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

## load in ML algorithm ##
import sys
sys.path.insert(0, '../modules/apollo/src/core/')

import DataFormatterv1
import ClassificationNetv1


with open("all_symbols_under5.txt", "r") as sym_file:
    lines = sym_file.readlines()

symbols = [line.strip() for line in lines]
print(symbols)

t0 = time.time()

INTERVAL_DAYS = int(sys.argv[1])
PERCENT = float(sys.argv[2])
TODAY = datetime.datetime.now()
d = datetime.timedelta(days=2)
TODAY -= d
output = []

def classifySymbols(symbol_sublist):

    global output

    for symbol in symbol_sublist:

        d = datetime.timedelta(days=INTERVAL_DAYS)
        start_date = TODAY - d
        try:
            data = yf.download(symbol,datetime.date.strftime(start_date, "%Y-%m-%d"),datetime.date.strftime(TODAY, "%Y-%m-%d")) 
        except: 
            print("Something went wrong, so I'm waiting 3 seconds.")
            time.sleep(3)


        ## extract closing data ##
        closing_data = data.Close

        training_data = []
        for d_idx, c_d in enumerate(closing_data):

            try:
                data_vec = [closing_data[d] for d in range(d_idx, d_idx+5)]

                if (1+float(PERCENT)/100.)*closing_data[d_idx+4] < closing_data[d_idx+5]:
                    data_vec.append(1.)
                else:
                    data_vec.append(0.)
                training_data.append(data_vec)
            except IndexError:
                break


        a = np.asarray(training_data)
        print(len(a))
        np.savetxt("data_cache.csv", a, delimiter=",")#, fmt='%1.4f %1.4f %1.4f %1.4f %1.4f %i')

        try:
            dataset = DataFormatterv1.Format("./data_cache.csv")
        except pd.errors.EmptyDataError:
            print("Couldn't find stock. Ignoring.")
            continue

        try:
            rate, result, _ = ClassificationNetv1.Predict(dataset, 5, closing_data[-6:-1], return_model=True)
        except ValueError:
            print(f"stock {symbol} may be too young. ignoring.")
            continue

        if int(result) == 0: 
            direction = 'not go up at least'
            num_dir = 0
            look_no_look = 'IGNORE'
        if int(result) == 1: 
            direction = 'go up at least'
            num_dir = PERCENT
            look_no_look = 'LOOK'
        print(f"Tomorrow the {symbol} stock will {direction} {PERCENT}%, with {rate*100}% certainty.")

        output.append([symbol, num_dir, rate, look_no_look])


classifySymbols(symbols)


# symbols_sublists = chunks(symbols, int(np.floor(len(symbols)/5)))

# for s, sublist in enumerate(symbols_sublists):
#     print(len(sublist))
#     threading.Thread( classifySymbols(sublist) )


with open(f'five_dollar_stock_prediction_{datetime.date.strftime(TODAY, "%Y-%m-%d")}_{INTERVAL_DAYS}-{PERCENT}percent.csv', "w") as op:
    for line in output:
        op.write(f"{line[0]}:\t {line[1]},\t {line[2]}, {line[3]}\n")
# df = pd.Series(output)
# df.to_csv('five_dollar_stock_prediction_11-03-2021.csv')


print(f">>>This took {time.time()-t0} seconds to run.<<<") 
