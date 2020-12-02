
import glob
from ECE16Lib.Communication import Communication
from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
from time import sleep
import numpy as np
from ECE16Lib.Pedometer import Pedometer
from pyowm import OWM
from datetime import date
from datetime import datetime


"""
Finds the proper thresholds in filtered data instead 
of using hardcoded thresholds 
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

"""
Collects 10 seconds of data that will be used to calibrate 
sensors 
@:return    samples of the x, y, and z acceleration
"""
def collect_samples(comms):
  num_samples = 500 # 10 seconds of data @ 50Hz
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)
  try:
    comms.clear() # just in case any junk is in the pipes
    # wait for user to start walking before starting to collect data
    input("Walk for 10 seconds to calibrate the pedometer. Press [ENTER] to begin.\n")
    comms.send_message("wearable") # begin sending data

    sample = 0
    while sample < num_samples:
      message = comms.receive_message()
      if message != None:
        try:
          (m1, m2, m3, m4, _) = message.split(',')
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

  return data

"""
Gets user data for 10 seconds and then processes this 
data to find good upper and lower thresholds for 
step detection
@:return the lower and upper threshold 
"""
def calibrate_thresholds(comms):
    ped_data = collect_samples(comms)
    ax = ped_data[:, 1]
    ay = ped_data[:, 2]
    az = ped_data[:, 3]
    ped_calibration = Pedometer(500, 50, [])
    ped_calibration.add(ax, ay, az)
    _, peaks, filtered = ped_calibration.process()
    return detect_thresholds(filtered, peaks)

"""
Gets the weather from San Diego using the OWM library
@:return : a string which displays the weather in °F. 
"""
def get_weather(owm):
    weather = owm.weather_at_place('San Diego,CA,US').weather  # Get the current weather using the OWM library
    return "Temp (F): " + str(weather.temperature('fahrenheit')['temp'])

"""
Creates the String message including the heart rate, steps, and 
weather/time 
@:param hr_est: The estimated heart rate
@:param steps: The estimated step count
@:param show_weather: boolean to tell weather to display weather or time 
@:param initial_period: whether or not to wait to display the heart rate because of 
                        early inaccuracies 
"""
def create_message(hr_est, steps, weather, initial_period):

    if initial_period <=0:
        # Strings that will display the heart rate and weather/time
        if hr_est > MAX_HEART_RATE:
            hr_str = "Bad HR reading"
        else:
            hr_str = "HR: " + str(int(hr_est)) + " bpm"
    else:
        hr_str =  str(initial_period) + " s left"

    # Displays the number of steps on the LED
    step_str = "Steps: " + str(int(steps))


    time_str = str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + ":" + str(
            datetime.now().time().second)

    return hr_str + "," + step_str + "," + weather + "," + time_str


if __name__ == "__main__":
    fs = 50 # the sampling frequency
    num_samples = 500 # 10 seconds of data @ 50Hz
    process_time = 1  # compute the heart beat and step count every second
    MAX_HEART_RATE = 200
    loop_counter = 0

    comms = Communication("/dev/cu.ag-ESP32SPP", 115200)  # used to communicate with Serial
    comms.clear()  # just in case any junk is in the pipes

    # Train the GMM model for the HR monitor
    hr = HRMonitor(num_samples, fs)
    hr.train()
    initial_period = 10

    # Calibrate the thresholds for the pedometer
    ped = Pedometer(num_samples, fs, [])
    low_thresh, high_thresh = calibrate_thresholds(comms)
    ped.set_thresholds(low_thresh, high_thresh)
    print(low_thresh, high_thresh)

    # Set up Bluetooth connection and API key for pyowm
    owm = OWM('0b8f49521da5313875dc27259de862cd').weather_manager()
    show_weather = False
    weather = ""

    input("Press [ENTER] when ready to use! \n")
    comms.send_message("wearable")  # begin sending data
    comms.send_message("buzz")
    # Live data
    try:
        previous_time = time()
        while True:
            message = comms.receive_message()
            if message != None:
                # if the button is pressed reset the step count
                if message.rstrip() == "reset":
                    ped.reset()
                    print("resetting step count")
                    continue
                try:
                    (m1, m2, m3, m4, m5) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
                    continue

                ped.add(int(m2), int(m3), int(m4))
                hr.add(int(m1)/1e3, int(m5))

                # if 1 second has elapsed, process the data and plot it
                current_time = time()
                if current_time - previous_time > process_time:
                    previous_time = current_time
                    try:
                        # process the pedometer data
                        steps, ped_peaks, ped_filtered = ped.process()
                        # with the processed data make a prediction using GMM model
                        hr_est, hr_peaks, hr_filtered = hr.process()
                    except:
                        continue

                    # everytime the person has taken 10 steps buzz the motor
                    if steps % 10 == 0 and steps != 0:
                        comms.send_message("buzz")

                    # update the weather every 10 seconds
                    if loop_counter % 10 == 0:
                        weather = get_weather(owm)
                            
                    comms_message = create_message(hr_est, steps, weather, initial_period)
                    print(comms_message)
                    comms.send_message(comms_message)
                    loop_counter += 1
                    initial_period -=1
    except(Exception, KeyboardInterrupt) as e:
        print(e)  # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()

