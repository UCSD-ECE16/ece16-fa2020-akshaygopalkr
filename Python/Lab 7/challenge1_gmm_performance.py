# Import for searching a directory
import glob

# The usual suspects
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt

# The GMM Import
from sklearn.mixture import GaussianMixture as GMM
from sklearn.metrics import r2_score

# Import for Gaussian PDF
from scipy.stats import norm

# Retrieve a list of the names of the subjects
def get_subjects(directory):
  filepaths = glob.glob(directory + "/*")
  return [filepath.split("/")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable
def get_data(directory, subject, trial, fs):
  search_key = "%s/%s/%s_%02d_*.csv" % (directory, subject, subject, trial)
  filepath = glob.glob(search_key)[0]
  t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
  t = (t-t[0])/1e3
  hr = get_hr(filepath, len(ppg), fs)

  fs_est = estimate_fs(t)
  if(fs_est < fs-1 or fs_est > fs):
    print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est,filepath))

  return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count
def get_hr(filepath, num_samples, fs):
  count = int(filepath.split("_")[-1].split(".")[0])
  seconds = num_samples / fs
  return count / seconds * 60 # 60s in a minute

# Estimate the sampling rate from the time vector
def estimate_fs(times):
  return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)
def process(x):
  x = filt.detrend(x, 25)
  x = filt.moving_average(x, 5)
  x = filt.gradient(x)
  return filt.normalize(x)

# Plot each component of the GMM as a separate Gaussian
def plot_gaussian(weight, mu, var):
  weight = float(weight)
  mu = float(mu)
  var = float(var)

  x = np.linspace(0, 1)
  y = weight * norm.pdf(x, mu, np.sqrt(var))
  plt.plot(x, y)

# Estimate the heart rate given GMM output labels
def estimate_hr(labels, num_samples, fs):
  peaks = np.diff(labels, prepend=0) == 1
  count = sum(peaks)
  seconds = num_samples / fs
  hr = count / seconds * 60 # 60s in a minute
  return hr, peaks

"""
Computes the rms square error
@:param hr: the actual heart rates from the data
@:param hr_est: the estimated heart rate from the GMM model
@:return the rms error 
"""
def compute_rms_error(hr, hr_est):
    np_hr = np.array(hr)
    np_hr_est = np.array(hr_est)
    sum_avg_diff = np.sum(np.square(np_hr_est-np_hr))/len(np_hr)
    return np.sqrt(sum_avg_diff)

""" 
Computes the R2 score of the GMM model
@param hr: the actual heart rate values 
@param hr_est: the estimated heart rate values
"""
def compute_r2_score(hr, hr_est):
  return r2_score(hr, hr_est)

"""
Computes the accuracy of the GMM model 
@param hr: the actual heart rate values 
@param hr_est: the estimated heart rate values
"""
def compute_accuracy(hr, hr_est):
  correct_pred = [hr[i] for i in range(0, len(hr)) if hr[i] == hr_est[i]]
  return len(correct_pred)/len(hr)


# Run the GMM with Leave-One-Subject-Out-Validation
if __name__ == "__main__":
  fs = 50
  directory = "/Users/akshaygopalkrishnan/Desktop/ECE 16/Python/Lab 7/data/data"
  subjects = get_subjects(directory)
  print(subjects)
  actual_hr_vals = []
  est_hr_vals = []
  # Leave-One-Subject-Out-Validation
  # 1) Exclude subject
  # 2) Load all other data, process, concatenate
  # 3) Train the GMM
  # 4) Compute the histogram and compare with GMM
  # 5) Test the GMM on excluded subject
  for exclude in subjects:
    print("Training - excluding subject: %s" % exclude)
    train_data = np.array([])
    for subject in subjects:
      for trial in range(1,11):
        t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)

        if subject != exclude:
          train_data = np.append(train_data, process(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    gmm = GMM(n_components=2).fit(train_data)

    # Compare the histogram with the GMM to make sure it is a good fit
    # plt.hist(train_data, 100, density=True)
    # plot_gaussian(gmm.weights_[0], gmm.means_[0], gmm.covariances_[0])
    # plot_gaussian(gmm.weights_[1], gmm.means_[1], gmm.covariances_[1])
    # plt.show()

    for trial in range(1,11):
      t, ppg, hr, fs_est = get_data(directory, exclude, trial, fs)
      test_data = process(ppg)
      labels = gmm.predict(test_data.reshape(-1,1))

      hr_est, peaks = estimate_hr(labels, len(ppg), fs)

      # print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (exclude,trial,hr,hr_est))
      actual_hr_vals.append(hr)
      est_hr_vals.append(hr_est)


  rms_error = compute_rms_error(actual_hr_vals, est_hr_vals)
  print("Root mean square error: " + str(rms_error))
  print("R2 score: " + str(compute_r2_score(actual_hr_vals, est_hr_vals)))
  print("Model accuracy: " + str(compute_accuracy(actual_hr_vals, est_hr_vals)))
  # used to plot a perfect algorithm, where the estimated heart
  est_equal_actual = []
  for i in range(30, 160):
    est_equal_actual.append(i)
  plt.scatter(est_hr_vals, actual_hr_vals)
  plt.plot(est_equal_actual, est_equal_actual, 'r', label = "Estimated HR = Actual HR")
  plt.title("Estimated vs. Actual heart rate")
  plt.xlabel('Estimated Heart Rate (bpm)')
  plt.ylabel('Actual Heart Rate (bpm)')
  plt.legend(loc = "upper left")
  plt.show()