from ECE16Lib.Communication import Communication
from ECE16Lib.Pedometer import Pedometer
import ECE16Lib.DSP as filt
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from ECE16Lib.CircularList import CircularList


# Save data to file
def save_data(filename, data):
  np.savetxt(filename, data, delimiter=",")

def load_data(filename):
  return np.genfromtxt(filename, delimiter=",")

# Collect num_samples from the MCU
def collect_samples():

  num_samples = 500 # 10 seconds of data @ 50Hz
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  comms = Communication("/dev/cu.AkshayBluetooth-ESP32SPP", 115200)
  try:
    comms.clear() # just in case any junk is in the pipes
    # wait for user to start walking before starting to collect data
    input("Ready to collect data? Press [ENTER] to begin.\n")
    sleep(3)
    comms.send_message("wearable") # begin sending data

    sample = 0
    while(sample < num_samples):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError: # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))
        sample += 1
        print("Collected {:d} samples".format(sample))

    # a single ndarray for all samples for easy file I/O
    data = np.column_stack([times, ax, ay, az])

  except(Exception, KeyboardInterrupt) as e:
      print(e)  # exiting the program due to exception
  finally:
      comms.send_message("sleep")  # stop sending data
      comms.close()

  return data

# Collects live data and then saves it into a file
def collect_and_save_data(filename):
    # Get data from the MCU and save to file
    data = collect_samples()
    save_data(filename, data)

    # Load the data from file
    data = load_data(filename)
    return data

"""
Defines the upper and lower thresholds on the signal and recounts 
the number of peaks based on the new thresholds
@:param filtered: the filtered data
@:param thresh_low: the lower threshold for detecting steps
@:param thresh_high: the upper threshold for detecting steps 
@:return the number of steps based on these thresholds 
"""
def find_peaks(filtered, thresh_low, thresh_high):
    return filt.count_peaks(filtered, thresh_low, thresh_high)

"""
Finds the proper thresholds in filtered data instead 
of using hardcoded 
@param filtered: the filtered data
@param peaks: the location of each peak in the filtered data 
@return:      the new upper and lower thresholds for step detection
"""
def detect_thresholds(filtered, peaks):
    peak_avg = np.average(np.array(filtered[peaks]))
    peak_std = np.std(np.array(filtered[peaks]))
    thresh_low = peak_avg - (2.5 * peak_std)
    thresh_high = peak_avg + (2.5 * peak_std)
    return thresh_low, thresh_high

# Load the data as a 500x4 ndarray
data = load_data("./data/offline_data.csv")

t = data[:,0]
t = (t-t[0])/1e3
ax = data[:,1]
ay = data[:,2]
az = data[:,3]


# Test the Pedometer with offline data
ped = Pedometer(500, 50, [])
ped.add(ax, ay, az)
_, peaks, filtered = ped.process()

low_thresh, high_thresh = detect_thresholds(filtered, peaks)
num_peaks, peak_locations = find_peaks(filtered, low_thresh, high_thresh)

print(low_thresh, high_thresh)
# Plot the results
plt.subplot(211)
plt.plot(t,filtered)
plt.title("Hard Coded Thresholds")
plt.plot(t, [4]*len(filtered), "b--")
plt.plot(t, [7]*len(filtered), "b--")
plt.subplot(212)
plt.plot(t, filtered)
plt.title("Detected Peaks with Smart Thresholds = %d" % num_peaks)
plt.plot(t[peak_locations], filtered[peak_locations], 'rx')
plt.plot(t, [low_thresh]*len(filtered), "b--")
plt.plot(t, [high_thresh]*len(filtered), "b--")
plt.show()
