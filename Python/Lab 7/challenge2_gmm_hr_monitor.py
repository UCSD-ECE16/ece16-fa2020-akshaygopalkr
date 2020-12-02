import glob
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt
from ECE16Lib.Communication import Communication
from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
from time import sleep
import numpy as np



if __name__ == "__main__":
    fs = 50  # sampling rate
    num_samples = 500  # 10 seconds of data @ 50Hz
    process_time = 1  # compute the heart beat every second
    MAX_HEART_RATE = 200 # the maximum heart rate possible

    initial_period = num_samples/fs # set initial period in seconds

    hr = HRMonitor(num_samples, fs)
    hr.train()

    input("Ready to start monitoring? Press [ENTER] to begin.\n")
    comms = Communication("/dev/cu.ag-ESP32SPP", 115200)
    comms.clear()  # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data

    # Used for plotting data
    t = CircularList([], num_samples)
    peaks = CircularList([], num_samples)

    # Live data
    try:
        previous_time = time()
        while True:
            message = comms.receive_message()
            if message != None:
                try:
                    (m1, _, _, _, m2) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
                    continue
                # Collect data in the pedometer
                hr.add(int(m1) / 1e3, int(m2))
                t.add(int(m1) / 1e3)
                t_arr = np.array(t)

                # if enough time has elapsed, process the data and plot it
                current_time = time()
                if current_time - previous_time > process_time:
                    previous_time = current_time
                    try:
                        # with the processed data make a prediction using GMM model
                        hr_est, est_peaks, filtered = hr.predict()
                        peaks.add(list(est_peaks))
                    except:
                        continue
                    # If enough time has passed for clean data
                    if initial_period <=0:
                        # If the heart is too large, then it should be displayed as an inaccurate reading
                        if hr_est > MAX_HEART_RATE:
                            plt.title("Inaccurate Reading")
                            comms.send_message("Inaccurate Reading")
                        # Otherwise display the Heart Rate on the Plot and send to the LED display
                        else:
                            comms.send_message("HR: " + str(int(hr_est)) + " bpm")
                            print("HR: " + str(int(hr_est)) + "bpm")
                            plt.title("Estimated Heart Rate: " + str(int(hr_est)) + " bpm")
                        plt.cla()
                        plt.plot(t_arr, filtered)
                        plt.plot(t_arr, peaks, 'rx')
                        plt.show(block = False)
                        plt.pause(0.001)
                    else:
                        print("Not enough data to compute... " + str(initial_period) + " seconds left...")
                        comms.send_message(str(initial_period))
                        initial_period-=1
    except(Exception, KeyboardInterrupt) as e:
        print(e)  # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
