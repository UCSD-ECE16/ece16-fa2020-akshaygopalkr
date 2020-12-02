from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
from time import time
from time import sleep
import ECE16Lib.DSP as filt
import numpy as np

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
    print(thresh_low, thresh_high)
    return thresh_low, thresh_high


"""
Collects 10 seconds of data that will be used to calibrate 
sensors 
@:return    samples of the x, y, and z acceleration
"""
def collect_samples():
    num_samples = 500  # 10 seconds of data @ 50Hz
    times = CircularList([], num_samples)
    ax = CircularList([], num_samples)
    ay = CircularList([], num_samples)
    az = CircularList([], num_samples)
    comms = Communication("/dev/cu.ag-ESP32SPP", 115200)
    try:
        comms.clear()  # just in case any junk is in the pipes
        # wait for user to start walking before starting to collect data
        input("Walk for 10 seconds to calibrate the pedometer. Press [ENTER] to begin.\n")
        sleep(3)
        comms.send_message("wearable")  # begin sending data

        sample = 0
        while sample < num_samples:
            message = comms.receive_message()
            if (message != None):
                try:
                    (m1, m2, m3, m4) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
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


"""
Gets user data for 10 seconds and then processes this 
data to find good upper and lower thresholds for 
step detection
@:return the lower and upper threshold 
"""
def calibrate_thresholds():
    data = collect_samples()
    ax = data[:, 1]
    ay = data[:, 2]
    az = data[:, 3]
    ped_calibration = Pedometer(500, 50, [])
    ped_calibration.add(ax, ay, az)
    _, step_peaks, filtr = ped_calibration.process()
    return detect_thresholds(filtr, step_peaks)


if __name__ == "__main__":
    fs = 50  # sampling rate
    num_samples = 250  # 5 seconds of data @ 50Hz
    process_time = 1  # compute the step count every second
    threshold_time = 5
    num_steps = 0
    ped = Pedometer(num_samples, fs, [])
    comms = Communication("/dev/cu.ag-ESP32SPP", 115200)
    low_thresh, high_thresh = calibrate_thresholds()
    print(low_thresh, high_thresh)
    ped.set_thresholds(low_thresh, high_thresh)
    comms.clear()  # just in case any junk is in the pipes
    sleep(3)
    comms.send_message("wearable")  # begin sending data
    print("Ready!")
    # Live data
    try:
        previous_time = time()
        while True:
            message = comms.receive_message()
            if message != None:
                try:
                    (m1, m2, m3, m4) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
                    continue

                # Collect data in the pedometer
                ped.add(int(m2), int(m3), int(m4))

                # if enough time has elapsed, process the data and plot it
                current_time = time()
                if current_time - previous_time > process_time:
                    previous_time = current_time

                    steps, peaks, filtered = ped.process()
                    print("Step count: {:d}".format(steps))
                    comms.send_message("Step count: " + str(steps))
                    plt.cla()
                    plt.plot(filtered)
                    plt.plot(low_thresh, "b--")
                    # plt.plot(high_thresh, "b--")
                    # plt.title("Step Count: %d" % steps)
                    # plt.show(block=False)
                    # plt.pause(0.001)

    except(Exception, KeyboardInterrupt) as e:
        print(e)  # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
