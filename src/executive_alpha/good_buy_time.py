#------------- imports -------------#
import yfinance as yf
import numpy as np
import pandas as pd
import datetime
from scipy import interpolate
from scipy.stats import chisquare
from tqdm import tqdm
import asyncio
import scipy.optimize
import time
from scipy.misc import derivative

from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

import bybit_buy_sell as bbs


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
mpl.rcParams['figure.facecolor'] = '1.0'
plt.rcParams.update({'font.size': 14})


def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset, 0])

    def sinfunc(t, A, w, p, c, d):  return A * np.sin(w*t + p) + c*t + d
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c, d = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c*t + d
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

def fit_sin_fixed_f(tt, yy, w):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 0., guess_offset, 0])

    def sinfunc(t, A, p, c, d):  return A * np.sin(w*t + p) + c*t + d
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, p, c, d = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c*t + d
    return {"amp": A, "omega": w , "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}


def reject_outliers(data, m = 2.):
    data = np.array(data)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m]

async def check_buy_time(ticker):

    TICKER = ticker + "-USD"
    print(f"Trying {TICKER}")

    ## check if you have the right coin ##
    stock = yf.Ticker(TICKER)
    current_price = stock.info['regularMarketPrice']

    bybit_price = await bbs.get_price(ticker)

    if abs(current_price-bybit_price)/bybit_price > 0.01:

        TICKER = ticker + '1-USD'
        print(f"Trying {TICKER}")
        ## check if you have the right coin ##
        stock = yf.Ticker(TICKER)
        current_price = stock.info['regularMarketPrice']

        bybit_price = await bbs.get_price(ticker)

        if abs(current_price-bybit_price)/bybit_price > 0.01:

            TICKER = ticker + '2-USD'
            print(f"Trying {TICKER}")
            ## check if you have the right coin ##
            stock = yf.Ticker(TICKER)
            current_price = stock.info['regularMarketPrice']

            bybit_price = await bbs.get_price(ticker)

            if abs(current_price-bybit_price)/bybit_price > 0.01:


                TICKER = ticker + '3-USD'
                print(f"Trying {TICKER}")
                ## check if you have the right coin ##
                stock = yf.Ticker(TICKER)
                current_price = stock.info['regularMarketPrice']

                bybit_price = await bbs.get_price(ticker)

                if abs(current_price-bybit_price)/bybit_price > 0.01:

                    print("Couldn't find the right coin.")
                    return -1





    plt.clf(); plt.cla()

    #------------- download data from last few hours -------------#
    data = yf.download(TICKER, period='2d', interval='1m')


    est_freqs = []
    for SAMPLE_PERIOD in tqdm(np.linspace(0.25, 24, 150)):
        sample_index = list(data.index)
        sample_close = list(data.Close)
        SAMPLE_DATA_LEN = len(sample_index)
        if SAMPLE_DATA_LEN != len(sample_close):
            bcolors.failure("Sample index and sample data length not equal.")


        ## splice data ##

        sample_period_fraction = float(SAMPLE_PERIOD+0.5)/(2.*24.)
        sample_period_index = int(SAMPLE_DATA_LEN - SAMPLE_DATA_LEN*sample_period_fraction)
        sample_index = sample_index[sample_period_index:]
        sample_close = sample_close[sample_period_index:]


        fit_x = np.linspace(-SAMPLE_PERIOD, 0, len(sample_index))

        #------------- identify periodicity in data -------------#
        try:
            res = fit_sin(fit_x, sample_close)
        except RuntimeError:
            continue
        except IndexError:
            continue

        est_freqs.append(1./res['omega'])
        for i in range(int(abs(24-int(SAMPLE_PERIOD)))):
            est_freqs.append(1./res['omega'])

    est_freqs = reject_outliers(est_freqs)
    # print ("[{0}][len(est_freqs): {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), len(est_freqs)))

    # print ("[{0}][np.median(est_freqs): {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), np.median(est_freqs)))
    # print ("[{0}][np.std(est_freqs): {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), np.std(est_freqs)))

    # plt.hist(est_freqs)
    # plt.show()

    SAMPLE_PERIOD =  0.3*np.median(est_freqs)
    sample_index = list(data.index)
    sample_close = list(data.Close)
    SAMPLE_DATA_LEN = len(sample_index)
    if SAMPLE_DATA_LEN != len(sample_close):
        bcolors.failure("Sample index and sample data length not equal.")

    # print ("[{0}][SAMPLE_DATA_LEN: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), SAMPLE_DATA_LEN))

    ## splice data ##

    sample_period_fraction = float(SAMPLE_PERIOD+0.5)/(1.*24.)
    sample_period_index = int(SAMPLE_DATA_LEN - SAMPLE_DATA_LEN*sample_period_fraction)
    # print ("[{0}][sample_period_index: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), type(sample_period_index)))
    sample_index = sample_index[sample_period_index:]
    sample_close = sample_close[sample_period_index:]

    print(min(sample_index))
    print(max(sample_index))

    fit_x = np.linspace(-SAMPLE_PERIOD, 0, len(sample_index))
    try:
        res = fit_sin_fixed_f(fit_x, sample_close, np.median(est_freqs))
        plt.plot(fit_x, res['fitfunc'](fit_x))
        first_derivative = abs(derivative(res['fitfunc'], 0, dx=1e-6, n=1))
        first_derivatives = [abs(derivative(res['fitfunc'], l, dx=1e-6, n=1)) for l in np.linspace(-SAMPLE_PERIOD, 0, 100)]
        second_derivative = derivative(res['fitfunc'], 0, dx=1e-6, n=2)
    except RuntimeError:
        print("Threw runtime error.")
        second_derivative = None

    fit = np.polyfit(fit_x, sample_close, 2)
    f = np.poly1d(fit)


    plt.plot(fit_x, sample_close)
    plt.plot(fit_x, f(fit_x))

    zero_point = -fit[1]/(2*fit[0])
    plt.axvline(zero_point)

    BUY = False

    if second_derivative is None: 
        second_derivative = fit[0]

    if abs(zero_point)/abs(SAMPLE_PERIOD) < 0.4 and second_derivative > 0:
        print("Go go go!")
        BUY = True


    plt.title(f"Buy {TICKER}: {str(BUY)}")

    plt.savefig("buy_terminal.png")


    return BUY

    # print(first_derivative)
    # print(second_derivative)


async def main():

    while 1:
        print(await check_buy_time('ENS'))
        time.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())