"""
====================================
Filename:         proof_of_concept.py 
Author:              Joseph Farah 
Description:       Making prediction based on past behavior.
====================================
Notes
     
"""
 
#------------- imports -------------#
import yfinance as yf
import numpy as np
import pandas as pd
import datetime
from scipy import interpolate
from scipy.stats import chisquare
import time

from matplotlib.backends.backend_pdf import PdfPages

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


#------------- classes -------------#
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



#------------- script settings -------------#
TICKER          = 'BAT-USD'
SAMPLE_PERIOD   = 2 ## hours
COMPARE_PERIOD  = '1mo'
INTERVAL        = '5m'

## check settings ##
if SAMPLE_PERIOD > 24:
    bcolors.failure("Sample period must be less than one day. Setting SAMPLE_PERIOD -> 24 (hours).")

pdf = PdfPages(f'{TICKER}_pattern_analysis.pdf')

#------------- download historical data -------------#
plt.clf(); plt.cla()
data = yf.download(TICKER, period=COMPARE_PERIOD, interval='5m')

history_index, history_close = list(data.index), list(data.Close)

## plot historical data ##
plt.plot(history_index, history_close)
plt.xlabel("Datetime")
plt.ylabel("Value of coin (USD)")
plt.title(f"{TICKER}, period: {COMPARE_PERIOD}, HISTORY")
# plt.show()
pdf.savefig()



#------------- download sample data -------------#
plt.clf(); plt.cla()
data = yf.download(TICKER, period='5d', interval='5m')

sample_index = list(data.index)
sample_close = list(data.Close)
SAMPLE_DATA_LEN = len(sample_index)
if SAMPLE_DATA_LEN != len(sample_close):
    bcolors.failure("Sample index and sample data length not equal.")

print ("[{0}][SAMPLE_DATA_LEN: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), SAMPLE_DATA_LEN))

## splice data ##
sample_period_fraction = float(SAMPLE_PERIOD)/(5.*24.)
sample_period_index = int(SAMPLE_DATA_LEN - SAMPLE_DATA_LEN*sample_period_fraction)
print ("[{0}][sample_period_index: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), type(sample_period_index)))
sample_index = sample_index[sample_period_index:]
sample_close = sample_close[sample_period_index:]

## plot historical data ##
plt.plot(sample_index, sample_close)
plt.xlabel("Datetime")
plt.ylabel("Value of coin (USD)")
plt.title(f"{TICKER}, period: last {SAMPLE_PERIOD} hours")
# plt.show()
pdf.savefig()



def interp(y, il=1000):        
    x = np.linspace(0, 1, len(y))
    f = interpolate.interp1d(x, y, kind='cubic')

    xnew = np.linspace(0, 1.0, il)
    return f(xnew)

def compare_sample_history(sample, history, show=False, return_interp=True):

    t0 = time.time()

    ## select interpolation length ##
    INTERP_LENGTH = 5*max([len(sample), len(history)])

    ## reinterpolate both sample and history ##
    sample = interp(sample, il=INTERP_LENGTH)
    history = interp(history, il=INTERP_LENGTH)

    min_hist = np.min(history)
    norm_hist = np.max(history-np.min(history))

    ## normalize both ##
    sample = (sample-np.min(sample))/np.max(sample-np.min(sample))+0.001
    history = (history-np.min(history))/np.max(history-np.min(history))+0.001

    ## calculate chi sq ##
    chisq = chisquare(history, f_exp=sample)[0]
    print ("[{0}][chisq: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), chisq))

    bcolors.success(f"Completed in {time.time()-t0} seconds.")

    if show:
        plt.plot(sample, c='blue', label='sample')
        plt.plot(history, c='red', label='history')
        plt.legend()
        plt.title(r"$\chi^2\approx$"+str(round(chisq, 3)))
        plt.show()

    if return_interp:
        return chisq, sample, history, min_hist, norm_hist 
    return chisq

def remaining(d):
    m = max(d.values())
    return {k:v for k,v in d.items() if v != m}


#------------- iterate over every subset -------------#
chisq_dict = {}
for idx in range(0, len(history_close)-len(sample_close)):

    ## splice history comp ##
    history_comp = history_close[idx:idx+len(sample_close)]

    ## check chisq ##
    chisq = compare_sample_history(sample_close, history_comp, show=False, return_interp=False)

    chisq_dict[idx] = chisq

    if len(chisq_dict.keys()) > 20:
        chisq_dict = remaining(chisq_dict)


print ("[{0}][chisq_dict: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), chisq_dict))


def plot_best_fits(bf_idx, future_time_frac=1.0, return_stats=True, show=True):

    plt.clf(); plt.cla()

    ## get chisq ##
    history_comp = history_close[idx:idx+len(sample_close)]
    chisq, in_sample, in_history, min_hist, norm_hist = compare_sample_history(sample_close, history_comp, show=False)

    ## plot fit ##
    plt.plot(in_sample, c='blue', label='sample')
    plt.plot(in_history, c='red', label='history')

    plt.axhline(in_history[-1], c='black', alpha=0.5, ls='--')
    plt.text(0.05, in_history[-1]*0.91, "Leave price", color='black')

    leave_price_actual = in_history[-1]*norm_hist + min_hist
    print ("[{0}][leave_price_actual: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), leave_price_actual))

    ## plot future behavior ##
    history_future = history_close[idx+int(future_time_frac*len(sample_close)):idx+2*int(future_time_frac*len(sample_close))]
    history_future = (history_future-min_hist)/norm_hist + 0.001\

    potential_price_actual = np.max(history_future)*norm_hist + min_hist
    print ("[{0}][potential_price_actual: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), potential_price_actual))

    plt.axhline(np.max(history_future), c='green', alpha=0.5, ls='--')
    plt.text(0.05, np.max(history_future)*1.005, "Potential price", color='green')

    twohour_price_actual = history_future[-1]*norm_hist + min_hist
    print ("[{0}][twohour_price_actual: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), twohour_price_actual))

    plt.axhline(history_future[-1], c='red', alpha=0.5, ls='--')
    plt.text(0.05, np.max(history_future)*1.005, "Potential price", color='red')

    plt.plot(np.linspace(len(in_history), len(in_history)+5*len(history_future), len(history_future)), history_future, c='red', ls='--', alpha=0.5, label='future')

    perc_diff = (potential_price_actual-leave_price_actual)/leave_price_actual
    perc_diff_worst = (twohour_price_actual-leave_price_actual)/leave_price_actual

    if show:
        plt.legend(frameon=False)
        plt.title(r"$\chi^2\approx$"+str(round(chisq, 3))+f", pdiff: {round(perc_diff, 5)}")
        pdf.savefig()
        # plt.show()

    if return_stats:
        return chisq, leave_price_actual, potential_price_actual, perc_diff, perc_diff_worst



#------------- plot best fits sections -------------#
plt.clf(); plt.cla()
good_chisqs, good_perc_diffs, good_perc_diff_worsts = [], [], []
for idx in list(chisq_dict.keys()):

    chisq, leave_price_actual, potential_price_actual, perc_diff, perc_diff_worst = plot_best_fits(idx, return_stats=True, show=True)

    good_chisqs.append(chisq)
    good_perc_diffs.append(perc_diff)
    good_perc_diff_worsts.append(perc_diff_worst)


#------------- plot maximum potential -------------#
estimate_returns = np.median(good_perc_diffs)

print ("[{0}][estimate_returns: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), estimate_returns))


plt.clf(); plt.cla()
plt.scatter(good_chisqs, good_perc_diffs)
plt.axhline(0, color='black', ls='--', alpha=0.3)
plt.xlabel("$\chi^2$")
plt.ylabel("Percent diff of potential price")
plt.title(f"Percent change distribution (estimate returns: {estimate_returns})")
# plt.show()
pdf.savefig()

#------------- plot histogram of good perc diff -------------#

plt.clf(); plt.cla()
plt.hist(good_perc_diffs, 10)
plt.axvline(np.median(good_perc_diffs), color='black', ls='--', alpha=0.3)
plt.axvline(np.median(good_perc_diffs)+np.std(good_perc_diffs), color='black', ls='--', alpha=0.3)
plt.axvline(np.median(good_perc_diffs)-np.std(good_perc_diffs), color='black', ls='--', alpha=0.3)
plt.xlabel("percent differences, potential")
pdf.savefig()

#------------- plot worst case -------------#
estimate_returns_worst = np.median(good_perc_diff_worsts)

print ("[{0}][estimate_returns_worst: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), estimate_returns_worst))


plt.clf(); plt.cla()
plt.scatter(good_chisqs, good_perc_diff_worsts)
plt.axhline(0, color='black', ls='--', alpha=0.3)
plt.xlabel("$\chi^2$")
plt.ylabel("Percent diff of worst case price")
plt.title(f"Percent change distribution (estimate worst returns: {estimate_returns_worst})")
# plt.show()
pdf.savefig()

#------------- plot histogram of worst case perc diff -------------#

plt.clf(); plt.cla()
plt.hist(good_perc_diff_worsts, 10)
plt.axvline(np.median(good_perc_diff_worsts), color='black', ls='--', alpha=0.3)
plt.axvline(np.median(good_perc_diff_worsts)+np.std(good_perc_diff_worsts), color='black', ls='--', alpha=0.3)
plt.axvline(np.median(good_perc_diff_worsts)-np.std(good_perc_diff_worsts), color='black', ls='--', alpha=0.3)
plt.xlabel("percent differences, worst case")
pdf.savefig()

pdf.close()
plt.clf(); plt.cla()