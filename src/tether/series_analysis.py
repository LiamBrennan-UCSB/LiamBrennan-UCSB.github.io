import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def estimate_periodicity(series, show=True):

    f, Pxx_den = signal.periodogram(series, len(series))

    max_f = f[np.argsort(Pxx_den)[-1]]

    if show:
        plt.semilogy(f, Pxx_den)
        plt.axvline(max_f)

        plt.show()

    return max_f / 1.6




if __name__ == '__main__':
    x = np.linspace(0, 10, 1000)
    y = np.sin(77.383*x)

    print(estimate_periodicity(y))


