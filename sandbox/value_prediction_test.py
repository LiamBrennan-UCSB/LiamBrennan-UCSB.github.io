import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import sys

## load in ML algorithm ##
import sys
sys.path.insert(0, '../modules/apollo/src/core/')

import DataFormatterv1
import ClassificationNetv1
import IterativeApproximation

STOCK = sys.argv[1].upper()

#------------- predict next day value -------------#
## download data from last six months ##
data = yf.download(STOCK,'2015-05-02','2021-11-05') 

## extract closing data ##
closing_data = data.Close

training_data = []
for d_idx, c_d in enumerate(closing_data):

    try:
        data_vec = [closing_data[d] for d in range(d_idx, d_idx+6)]
        

        training_data.append(data_vec)
    except IndexError:
        break

## save data for read-in ##
a = np.asarray(training_data)
np.savetxt("test_iterative_aapl_training.csv", a, delimiter=",")

results = np.transpose(training_data)[-1]


## load in dataset ##
dataset = DataFormatterv1.Format("./test_iterative_aapl_training.csv", names=['a', 'b', 'c', 'd', 'e', 'f'])

list_of_columns = [
    list(dataset.a.tolist()),
    list(dataset.b.tolist()),
    list(dataset.c.tolist()),   
    list(dataset.d.tolist()),
    list(dataset.e.tolist()),
    list(dataset.f.tolist())
]

predict = training_data[-1][0:-1]
## expected value 5.530000209808349609e+00
(bounds, history) = IterativeApproximation.IterativeApproximation(dataset, predict, list_of_columns, start_v = np.mean(results), second_v=1.5*np.mean(results), num_iter=25, show_graph=False)