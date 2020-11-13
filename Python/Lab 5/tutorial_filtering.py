import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig


def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Compute the L1 norm for vectors ax, ay, az (L1=|ax|+|ay|+|az|)
def l1_norm(ax, ay, az):
  return abs(ax) + abs(ay) + abs(az)

# Compute the Moving Average Efficiently
def moving_average(x, win):
  ma = np.zeros(x.size)
  for i in np.arange(0,len(x)):
    if(i < win): # use mean until filter is "on"
      ma[i] = np.mean(x[:i+1])
    else:
      ma[i] = ma[i-1] + (x[i] - x[i-win])/win
  return ma

# Detrend the Signal
def detrend(x, win=50):
  return x - moving_average(x, win)

# Count the Number of Peaks
def count_peaks(x, thresh_low, thresh_high):
  peaks, _ = sig.find_peaks(x)
  count = 0
  locations = []
  for peak in peaks:
    if x[peak] >= thresh_low and x[peak] <= thresh_high:
      count += 1
      locations.append(peak)
  return count, locations


# Load the data as a 500x4 ndarray
data = load_data("./data/8steps_10s_50hz.csv")
t = data[:,0]
t = (t - t[0])/1e3
ax = data[:,1]
ay = data[:,2]
az = data[:,3]
l1 = l1_norm(ax, ay, az)
ma = moving_average(l1, 20)
dt = detrend(ma)

# Power Spectral Density
fs = 50 # sampling rate

# nfft = # of samples taken, fs = sampling frequency
freqs, power = sig.welch(az, nfft=len(az), fs=fs)

# Low-pass Filter Design
bl, al = sig.butter(3, 1, btype="lowpass", fs=fs)

# Once you have made a filter, you can apply it to a signal with lfilter()

# When we apply this, in our filtered signal we get a filter delay, which is cause
# when we don't have previous samples to filter the signal. A flat portion is known as
# the filter transient, which can create discontinuities
lp = sig.lfilter(bl, al, dt)

# Low-pass Filter the Signal Better
lp2 = sig.filtfilt(bl, al, dt)

thresh_low = 25
thresh_high = 100
count, peaks = count_peaks(lp2, thresh_low, thresh_high)

print(peaks)
plt.plot(t, lp2)
plt.title("Detected Peaks = %d" % count)
plt.plot(t[peaks], lp2[peaks], 'rx')
plt.plot(t, [thresh_low]*len(lp2), "b--")
plt.plot(t, [thresh_high]*len(lp2), "b--")
plt.show()


