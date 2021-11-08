import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 

## load in ML algorithm ##
import sys
sys.path.insert(0, '../modules/apollo/src/core/')

import DataFormatterv1
import ClassificationNetv1
import IterativeApproximation

STOCK = "AAPL"

#------------- predict next day value -------------#
## download data from last six months ##
data = yf.download('IO','2021-05-02','2021-11-02') 

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

predict = [1.789999961853027344e+00,1.789999961853027344e+00,1.730000019073486328e+00,1.629999995231628418e+00,1.529999971389770508e+00] ## expected value 1.720000028610229492e+00
(bounds, history) = IterativeApproximation.IterativeApproximation(dataset, predict, list_of_columns, start_v = np.mean(predict), second_v=1.5*np.mean(predict), num_iter=25, show_graph=False)