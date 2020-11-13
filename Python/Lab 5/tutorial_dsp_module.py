import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt
import numpy as np

fs = 50      # sampling rate
t_low = 3   # lower peak threshold
t_high = 12 # upper peak threshold

def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Load the data as a 500x4 ndarray
data = load_data("./data/offline_data.csv")
t = data[:,0]
t = (t - t[0])/1e3
ax = data[:,1]
ay = data[:,2]
az = data[:,3]

l1 = filt.l1_norm(ax, ay, az)                      # Compute the L1-Norm
print(len(l1))
ma = filt.moving_average(l1, 20)                   # Compute Moving Average
dt = filt.detrend(ma)                              # Detrend the Signal

freqs, power = filt.psd(l1, len(l1), 50)           # Power Spectral Density

bl, al = filt.create_filter(3, 1, "lowpass", fs)   # Low-pass Filter Design
lp = filt.filter(bl, al, dt)                       # Low-pass Filter Signal

grad = filt.gradient(lp)  # Compute the gradient
grad_avg = filt.moving_average(grad,20) # Compute the moving average of the gradient

count, peaks = filt.count_peaks(grad_avg, t_low, t_high) # Find & Count the Peaks

# Plot the results
plt.plot(t, grad_avg)
plt.title("Detected Peaks = %d" % count)
plt.plot(t[peaks], grad_avg[peaks], 'rx')
plt.plot(t, [t_low]*len(grad_avg), "b--")
plt.plot(t, [t_high]*len(grad_avg), "b--")
plt.show()

plt.plot(freqs, power)
plt.title("Power Spectrum Density")
plt.show()