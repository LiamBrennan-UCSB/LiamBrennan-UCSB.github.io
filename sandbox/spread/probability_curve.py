import yfinance as yf
import numpy as np
import pandas as pd
import urllib
import time 
import matplotlib.pyplot as plt

## download data from last six months ##
data = yf.download('HIPO','2021-05-02','2021-11-02') 

## extract closing data ##
closing_data = data.Close

six_months_changes = []
six_weeks_changes = []
three_weeks_changes = []
one_week_changes = []

## grab timespans ##
six_months = closing_data
six_weeks = closing_data[-30:-1]
three_weeks = closing_data[-10:-1]
one_week = closing_data[-5:-1]

## roll and subtract ##
six_mo_deltas = six_months - np.roll(six_months, 1)
six_weeks_deltas = six_weeks - np.roll(six_weeks, 1)
three_weeks_deltas = three_weeks - np.roll(three_weeks, 1)
one_week_deltas = one_week - np.roll(one_week, 1)

## chop off first erraneous point ##
six_mo_deltas = six_mo_deltas[1:]
six_weeks_deltas = six_weeks_deltas[1:]
three_weeks_deltas = three_weeks_deltas[1:]
one_week_deltas = one_week_deltas[1:]

## get truths ##
six_mo_above_zero = six_mo_deltas > 0
six_weeks_above_zero = six_weeks_deltas > 0
three_weeks_above_zero = three_weeks_deltas > 0
one_week_above_zero = one_week_deltas > 0

## get probabilities ##
times = [-180, -42, -21, -7]
probs = [six_mo_above_zero.sum()/len(six_mo_above_zero), six_weeks_above_zero.sum()/len(six_weeks_above_zero), three_weeks_above_zero.sum()/len(three_weeks_above_zero), one_week_above_zero.sum()/len(one_week_above_zero)]


z = np.polyfit(times, probs, 1)
p = np.poly1d(z)

plt.plot(times, probs)
plt.plot(times, p(times))
plt.show()