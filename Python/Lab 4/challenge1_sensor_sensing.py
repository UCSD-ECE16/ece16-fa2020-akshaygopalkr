from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np

"""
Computes the average value for an axis
@:param acceleration_list: The acceleration over 5 seconds in either x,y,z direction
@:return: A scalar which is the average from the acceleration list 
"""


def average_value(acceleration_list):
    return np.average(np.array(acceleration_list))


"""
Computes the difference between each adjacent indexes
@:param acceleration_list: The acceleration over 5 seconds in either x,y,z direction
@:return: a numpy array containing the differences between each point
"""


def sample_difference(acceleration_list):
    np.diff(np.array(acceleration_list))
    return np.diff(np.array(acceleration_list))


"""
Computes the euclidean distance for the acceleration list
@:param acceleration_list: The acceleration over 5 seconds in either x,y,z direction
@:return: A scalar which is the square root of the sum of each number in the 
"""


def l2_norm_calculation(ax,ay,az):
    return np.linalg.norm(np.array([ax,ay,az]))


"""
Computes the L1 norm for the acceleration lsit
@:param acceleration_list:The acceleration over 5 seconds in either x,y,z direction
@:return: The sum of the absolute value of each acceleration value 
"""


def l1_norm_calculation(ax,ay,az):
    return np.linalg.norm(np.array([ax,ay,az]), ord=1)


"""
Finds the max acceleration in one of the accelerations 
"""


def max_acceleration(acceleration_list):
    return int(np.max(np.array(acceleration_list)))


def plot_three_subplots():
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax1.set_title("X-acceleration (Red) and Max acceleration (Blue)")
    ax2.set_title("Y-acceleration (Red) and Max acceleration (Blue)")
    ax3.set_title("Z-acceleration (Red) and Max acceleration (Blue)")
    ax1.plot(transform_x, 'b', ax, 'r')
    ax2.plot(transform_y, 'b', ay, 'r')
    ax3.plot(transform_z, 'b', az, 'r')

def plot_two_subplots():
    ax1.cla()
    ax2.cla()
    ax1.set_title("X (Red), Y (Blue), and Z(Green) Acceleration")
    ax2.set_title("X (Red), Y(Blue), and Z(Green) Sample Difference")
    ax1.plot(ax, 'r', ay, 'b', az, 'g')
    ax2.plot(transform_x, 'r', transform_y, 'b', transform_z, 'g')

def plot_norm(euclidean_distance):
    ax1.cla()
    ax2.cla()
    ax1.set_title("X (Red), Y (Blue) and Z (Green) Acceleration")
    ax2.set_title("Euclidean Distance")
    ax1.plot(ax, 'r', ay, 'b', az, 'g')
    ax2.plot(euclidean_distance)

if __name__ == "__main__":
    num_samples = 100  # 2 seconds of data @ 50Hz
    refresh_time = 0.1  # update the plot every 0.1s (10 FPS)

    # This is a predefined dictionary I will use to decide what transformation method to call
    transform_dict = {0: average_value, 1: sample_difference, 2: l2_norm_calculation
        , 3: l1_norm_calculation, 4: max_acceleration}
    transform_method = transform_dict[0]
    times = CircularList([], num_samples)
    ax = CircularList([], num_samples)
    ay = CircularList([], num_samples)
    az = CircularList([], num_samples)

    # These will contain data for the transformation data
    transform_x = CircularList([], num_samples)
    transform_y = CircularList([], num_samples)
    transform_z = CircularList([], num_samples)

    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    comms = Communication("/dev/cu.AkshayBluetooth-ESP32SPP", 115200)
    comms.clear()  # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data
    try:
        previous_time = 0
        while (True):
            message = comms.receive_message()
            if (message != None):
                try:
                    (m1, m2, m3, m4) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
                    print("bad")
                    continue

                # add the new values to the circular lists
                times.add(int(m1))
                ax.add(int(m2))
                ay.add(int(m3))
                az.add(int(m4))

                if transform_method == l2_norm_calculation or transform_method == l1_norm_calculation:
                    transform_x.add(transform_method(int(m1),int(m2),int(m3)))
                elif transform_method != sample_difference :
                    transform_x.add(transform_method(ax))
                    transform_y.add(transform_method(ay))
                    transform_z.add(transform_method(az))
                else:
                    transform_x = sample_difference(ax)
                    transform_y = sample_difference(ay)
                    transform_z = sample_difference(az)
                # if enough time has elapsed, clear the axis, and plot az
                current_time = time()
                if (current_time - previous_time > refresh_time):
                    previous_time = current_time
                    if transform_method == l2_norm_calculation or transform_method == l1_norm_calculation:
                        plot_norm(transform_x)
                    elif transform_method == sample_difference:
                        plot_two_subplots()
                    else:
                        plot_three_subplots()
                    plt.show(block=False)
                    plt.pause(0.001)
    except(Exception, KeyboardInterrupt) as e:
        print(e)  # Exiting the program due to exception
    finally:
        comms.send_message("sleep")  # stop sending data
        comms.close()
