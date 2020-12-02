from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np
import glob
from sklearn.mixture import GaussianMixture as GMM
"""
A class to enable a simple heart rate monitor
"""
class HRMonitor:
  """
  Encapsulated class attributes (with default values)
  """
  __hr = 0           # the current heart rate
  __time = None      # CircularList containing the time vector
  __ppg = None       # CircularList containing the raw signal
  __filtered = None  # CircularList containing filtered signal
  __num_samples = 0  # The length of data maintained
  __new_samples = 0  # How many new samples exist to process
  __fs = 0           # Sampling rate in Hz
  __thresh = 0.6     # Threshold from Tutorial 2
  __directory = "/Users/akshaygopalkrishnan/Desktop/ECE 16/Python/Lab 7/data/data"

  """
  Initialize the class instance
  """
  def __init__(self, num_samples, fs, times=[], data=[]):
    self.__hr = 0
    self.__num_samples = num_samples
    self.__fs = fs
    self.__time = CircularList(data, num_samples)
    self.__ppg = CircularList(data, num_samples)
    self.__filtered = CircularList([], num_samples)
    self.__gmm = GMM(n_components=2)

  """
  Add new samples to the data buffer
  Handles both integers and vectors!
  """
  def add(self, t, x):
    if isinstance(t, np.ndarray):
      t = t.tolist()
    if isinstance(x, np.ndarray):
      x = x.tolist()


    if isinstance(x, int):
      self.__new_samples += 1
    else:
      self.__new_samples += len(x)

    self.__time.add(t)
    self.__ppg.add(x)

  """
  Compute the average heart rate over the peaks
  """
  def compute_heart_rate(self, peaks):
    t = np.array(self.__time)
    if len(np.diff(t[peaks])) > 0:
      return 60 / np.mean(np.diff(t[peaks]))
    else:
      return 0

  """ 
  Removes outlier peaks from the filtered data
  @:param peaks: The location of each peak 
  @:return the peaks with outliers removed
  """
  def remove_outliers(self, peaks):
    if len(peaks) > 1:
      t = np.array(self.__time)

      # Calculate peak difference and average/standard deviation
      peak_diff = np.diff(t[peaks])
      avg_peak_diff = np.mean(peak_diff)
      std_peak_diff = np.std(peak_diff)

      for i in range(len(peak_diff)):
        # If the peak difference is less than 2 deviations from the average, remove the peak (outlier)
        if peak_diff[i] < (avg_peak_diff - (1 * std_peak_diff)):
          peaks.pop(i+1)


    return peaks


  # Filter the signal (as in the prior lab)
  def train_process(self, x):
    x = filt.detrend(x, 25)
    x = filt.moving_average(x, 5)
    x = filt.gradient(x)
    return filt.normalize(x)

  # Retrieve a list of the names of the subjects
  def get_subjects(self, directory):
    filepaths = glob.glob(directory + "/*")
    return [filepath.split("/")[-1] for filepath in filepaths]

  # Estimate the heart rate from the user-reported peak count
  def get_hr(self, filepath, num_samples, fs):
    count = int(filepath.split("_")[-1].split(".")[0])
    seconds = num_samples / fs
    return count / seconds * 60  # 60s in a minute

  # Estimate the sampling rate from the time vector
  def estimate_fs(self, times):
    return 1 / np.mean(np.diff(times))

  # Retrieve a data file, verifying its FS is reasonable
  def get_data(self, directory, subject, trial, fs):
    search_key = "%s/%s/%s_%02d_*.csv" % (directory, subject, subject, trial)
    filepath = glob.glob(search_key)[0]
    t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
    t = (t - t[0]) / 1e3
    hr = self.get_hr(filepath, len(ppg), fs)
    fs_est = self.estimate_fs(t)
    if (fs_est < fs - 1 or fs_est > fs):
      print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est, filepath))
    return t, ppg, hr, fs_est

  """
  Trains the GMM model on offline data 
  @:return: the trained GMM model 
  """
  def train(self):
    print("Training GMM model... ")
    subjects = self.get_subjects(self.__directory)
    train_data = np.array([])
    for subject in subjects:
      for trial in range(1,11):
        t, ppg, hr, fs_est = self.get_data(self.__directory, subject, trial, self.__fs)
        train_data = np.append(train_data, self.train_process(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    self.__gmm = GMM(n_components=2).fit(train_data)

  """
  Estimate the heart rate given GMM output labels
  """
  def estimate_hr(self, labels, num_samples, fs):
    peaks = np.diff(labels, prepend=0) == 1
    count = sum(peaks)
    seconds = num_samples / fs
    hr = count / seconds * 60  # 60s in a minute
    return hr, peaks

  """
  Uses the GMM model to estimate the heart rate 
  @:param filtered: the filtered data
  @:param fs: the sampling frequency
  @:return: the estimated heart rate and estimated time of each peak 
  """
  def predict(self):
    # Grab only the new samples into a NumPy array
    x = np.array(self.__ppg[-self.__new_samples:])
    filtered_arr = self.train_process(x)
    self.__filtered.add(filtered_arr.tolist())
    labels = self.__gmm.predict(np.array(self.__filtered).reshape(-1, 1))
    self.__new_samples = 0
    hr_est, est_peaks = self.estimate_hr(labels, len(self.__filtered), self.__fs)
    return hr_est, est_peaks, np.array(self.__filtered)


  """
  Process the new data to update step count
  """
  def process(self):
    # Grab only the new samples into a NumPy array
    x = np.array(self.__ppg[-self.__new_samples:])

    # Filter the signal (feel free to customize!)
    x = filt.detrend(x, 25)
    x = filt.moving_average(x, 5)
    x = filt.gradient(x)
    x = filt.normalize(x)

    # Store the filtered data
    self.__filtered.add(x.tolist())

    # Find the peaks in the filtered data
    _, peaks = filt.count_peaks(self.__filtered, self.__thresh, 1)

    peaks = self.remove_outliers(peaks)


    # Update the step count and reset the new sample count
    self.__hr = self.compute_heart_rate(peaks)
    self.__new_samples = 0

    # Return the heart rate, peak locations, and filtered data
    return self.__hr, peaks, np.array(self.__filtered)

  """
  Clear the data buffers and step count
  """
  def reset(self):
    self.__steps = 0
    self.__time.clear()
    self.__ppg.clear()
    self.__filtered = np.zeros(self.__num_samples)


