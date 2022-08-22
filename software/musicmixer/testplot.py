from scipy import signal
from scipy.fftpack import fft
import matplotlib.pyplot as plt

w = signal.hamming(51)
plt.plot(w)
plt.show()
