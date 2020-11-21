from ECE16Lib.Communication import Communication
from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.CircularList import  CircularList
from matplotlib import pyplot as plt
from time import time
from time import sleep
import numpy as np

if __name__ == "__main__":
    fs = 50                         # sampling rate
    num_samples = 500               # 10 seconds of data @ 50Hz
    process_time = 1                # compute the heart beat every second
    MAX_HEART_RATE  = 200
    hr = HRMonitor(num_samples, 50)
    comms = Communication("/dev/cu.ag-ESP32SPP", 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data
    print("Ready!")
    hr_plot = CircularList([], num_samples)
    t = CircularList([], num_samples)
    # Live data
    try:
        previous_time = time()
        while(True):
            message = comms.receive_message()
            if (message != None):
                try:
                    (m1, _, _, _, m2) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
                    continue
                # Collect data in the pedometer
                hr.add(int(m1)/1e3, int(m2))
                t.add(int(m1)/1e3)
                t_plot = np.array(t)
                # if enough time has elapsed, process the data and plot it
                current_time = time()
                if (current_time - previous_time > process_time):
                    previous_time = current_time
                    try:
                        heart_rate, peaks, filtered = hr.process()
                    except:
                        continue
                    print("Heart Rate: " + str(heart_rate))
                    plt.cla()
                    plt.plot(t_plot, filtered)
                    plt.plot(t_plot[peaks], filtered[peaks], 'rx')
                    plt.plot(t_plot, [0.6]*len(filtered), 'b--')
                    # If the heart is too large, then it should be displayed as an inaccurate reading
                    if(heart_rate > MAX_HEART_RATE):
                        plt.title("Inaccurate Reading")
                        comms.send_message("Inaccurate Reading")
                    # Otherwise display the Heart Rate on the Plot and send to the LED display
                    else:
                        plt.title("Heart Rate: %d" % heart_rate)
                        comms.send_message("HR: " + str(int(heart_rate)) + " bpm")
                    plt.show(block=False)
                    plt.pause(0.001)
    except(Exception, KeyboardInterrupt) as e:
      print(e)  # Exiting the program due to exception
    finally:
      print("Closing connection.")
      comms.send_message("sleep")  # stop sending data
      comms.close()


