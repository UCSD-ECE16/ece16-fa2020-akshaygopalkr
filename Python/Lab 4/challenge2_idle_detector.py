from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from time import time
import numpy as np

"""
Computes the average value for an axis
@:param acceleration_list: The acceleration over 5 seconds in either x,y,z direction
@:return: A scalar which is the average from the acceleration list 
"""
def average_value(ax,ay,az):
    return np.average(np.array(ax)), np.average(np.array(ay)), np.average(np.array(az))

"""
Determines whether the device is inactive or not 
@:param average_x: The average x-acceleration
@:param average_y: The average y-acceleration
@:param average_z: The average z-acceleration
@:return: a boolean representing whether the device is inactive or not 
"""
def is_inactive(average_x, average_y, average_z):
    return average_x <= ax_idle_threshold and average_y <= ay_idle_threshold and average_z <= az_idle_threshold

# Bluetooth port: /dev/cu.AkshayBluetooth-ESP32SPP
# Serial port: /dev/cu.usbserial-1410
comms = Communication("/dev/cu.AkshayBluetooth-ESP32SPP", 115200)
comms.clear()  # just in case any junk is in the pipes
comms.send_message("wearable")  # begin sending data
num_samples = 250  # we want the data to store 5 seconds of data
refresh_time = 0.1  # update the plot every 0.1s (10 FPS)

# lists to keep track of the acceleration and
times = CircularList([], num_samples)
ax = CircularList([], num_samples)
ay = CircularList([], num_samples)
az = CircularList([], num_samples)

# the thresholds that determine when the device is idle or noot
ax_idle_threshold = 2080
ay_idle_threshold = 2085
az_idle_threshold = 2625

last_idlecheck_time = 0 # variable to keep track of last time for idle check
idle_state = False
last_active_time = 0  # variable to keep track of last time person was active for 1 second



# sample data from the accelerometer
try:
    previous_time = 0
    while (True):
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
            current_time = time()
            # every 5 seconds, check to see if the person has been inactive
            if current_time - last_idlecheck_time >= 5:
                average_x, average_y, average_z = average_value(ax,ay,az)
                print(average_x, ",", average_y, ",", average_z)
                last_idlecheck_time = current_time
                # if they have been inactive then buzz the motor
                if is_inactive(average_x, average_y, average_z):
                    idle_state = True
                    comms.send_message("Buzz motor")
                else:
                    idle_state = False
            # If the person has been inactive but has become active for 1 second
            if idle_state and current_time - last_active_time >= 1:
                last_active_time = current_time
                # get the average values for the last 1 second
                average_x, average_y, average_z = average_value(ax[200:],ay[200:],az[200:])
                if not is_inactive(average_x, average_y, average_z):
                    print("Active accelerations: ", average_x, average_y, average_z)
                    last_idlecheck_time = current_time # this ensures that the person must be inactive for 5 seconds after their activity
                    comms.send_message("Keep it up!")
except(Exception, KeyboardInterrupt) as e:
    print(e)  # Exiting the program due to exception
finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()


