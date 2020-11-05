from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from time import time
import numpy as np
from matplotlib import pyplot as plt
from time import sleep

class Processing():
    __num_samples = 250  # 2 seconds of data @ 50Hz
    __refresh_time = 0.5  # update the plot every 0.1s (10 FPS)

    # Thresholds for idle detection
    __ax_idle_threshold = 1935
    __ay_idle_threshold = 1918
    __az_idle_threshold = 2430

    """
    Initializes the processing object and sets the field variables 
    @:param transformation_method: the type of transformation that will be plotted and computed 
    @:param port_name: The Serial port name used for Serial communication 
    """
    def __init__(self, transformation_method, port_name):
        self.comms = Communication(port_name, 115200)

        __transform_dict = {"average acceleration": self.__average_value, "sample difference": self.__sample_difference,
                            "L2 norm": self.__l2_norm_calculation, "L1 norm": self.__l1_norm_calculation,
                            "Maximum acceleration:": self.__max_acceleration}

        # This will keep track of the transformation method to be called
        self.__transformation_method = __transform_dict[transformation_method]
        self.transform_x = CircularList([], self.__num_samples)
        self.transform_y = CircularList([], self.__num_samples)
        self.transform_z = CircularList([], self.__num_samples)

        # These will contain the acceleration values read from the accelerometer
        self.times = CircularList([], self.__num_samples)
        self.ax = CircularList([], self.__num_samples)
        self.ay = CircularList([], self.__num_samples)
        self.az = CircularList([], self.__num_samples)

        # Set up the plotting
        fig = plt.figure()
        self.ax1 = fig.add_subplot(311)
        self.ax2 = fig.add_subplot(312)
        self.ax3 = fig.add_subplot(313)
        self.graph_type = transformation_method

        # times to keep track of when
        self.__last_idlecheck_time = 0
        self.__idle_state = False
        self.__last_active_time = 0

    """
    Updates the plot, displaying the acceeleration values as well as the 
    transformation values
    """
    def __plot(self):
        # Clears the plots and resets them
        self.ax1.cla()
        self.ax2.cla()
        self.ax3.cla()

        # Sets the title of the plot
        self.ax1.set_title("X acceleration (Red) and " + self.graph_type + " (Blue)")
        self.ax2.set_title("Y acceleration (Red) and " + self.graph_type + " (Blue)")
        self.ax3.set_title("X acceleration (Red) and " + self.graph_type + " (Blue)")

        # Plots the acceleration values along with the transformation
        self.ax1.plot(self.transform_x, 'b', self.ax, 'r')
        self.ax2.plot(self.transform_y, 'b', self.ay, 'r')
        self.ax3.plot(self.transform_z, 'b', self.az, 'r')
        plt.show(block = False)
        plt.pause(0.0001)

    """
    Determines whether the device is inactive or not 
    @:param average_x: The average x-acceleration
    @:param average_y: The average y-acceleration
    @:param average_z: The average z-acceleration
    @:return: a boolean representing whether the device is inactive or not 
    """
    def __is_inactive(self, average_x, average_y, average_z):
        return average_x <= self.__ax_idle_threshold and average_y <= self.__ay_idle_threshold and average_z <= self.__az_idle_threshold


    """
    Computes the average value for an axis
    @:param acceleration_list: The acceleration over 5 seconds in either x,y,z direction
    @:return: A scalar which is the average from the acceleration list 
    """
    def __average_value(self, acceleration_list):
        return np.average(np.array(acceleration_list))

    """
    Computes the difference between each adjacent indexes
    @:param acceleration_list: The acceleration over 5 seconds in either x,y,z direction
    @:return: a numpy array containing the differences between each point
    """
    def __sample_difference(self, acceleration_list):
        np.diff(np.array(acceleration_list))
        return np.diff(np.array(acceleration_list))

    """
    Computes the euclidean distance for the acceleration list
    @:param x_acceleration: one sample of the x-acceleration
    @:param y_acceleration: one sample of the y-acceleration
    @:param z_acceleration: one sample of the z-acceleration
    @:return: A scalar which is the square root of the sum of each number in the 
    """
    def __l2_norm_calculation(self, x_acceleration, y_acceleration, z_acceleration):
        return np.linalg.norm(np.array([x_acceleration, y_acceleration, z_acceleration]))

    """
    Computes the L1 norm for the acceleration lsit
    @:param x_acceleration: one sample of the x-acceleration
    @:param y_acceleration: one sample of the y-acceleration
    @:param z_acceleration: one sample of the z-acceleration
    @:return: The sum of the absolute value of each acceleration value 
    """
    def __l1_norm_calculation(self, x_acceleration, y_acceleration, z_acceleration):
        return np.linalg.norm(np.array([x_acceleration, y_acceleration, z_acceleration]), ord=1)

    """
    Finds the max acceleration in one of the accelerations 
    @:param: acceleration_list: The acceleration over 5 seconds in either x,y,z direction
    @:return: The maximum value in the acceleration list 
    """
    def __max_acceleration(self, acceleration_list):
        return int(np.max(np.array(acceleration_list)))

    """
    Records the acceleration and times from the accelerometer 
    @:param time: the time from the Serial monitor
    @:param x_acceleration: the x-acceleration
    @:param y_acceleration: the y-acceleration
    @:param z_acceleration: the z-acceleration
    """
    def __record_acceleration(self,time, x_acceleration ,y_acceleration, z_acceleration):
        # add the new values to the circular lists
        self.times.add(int(time))
        self.ax.add(int(x_acceleration))
        self.ay.add(int(y_acceleration))
        self.az.add(int(z_acceleration))

    """
    Records the transformation value based on what transformation type the 
    instance uses 
    @:param x_acceleration: one sample of the x-acceleration
    @:param y_acceleration: one sample of the y-acceleration
    @:param z_acceleration: one sample of the z-acceleration
    """
    def __record_transformation(self, x_acceleration, y_acceleration, z_acceleration):
        # These if statements are used because some of these methods have different parameters and return types
        if self.__transformation_method == self.__l1_norm_calculation or self.__transformation_method == self.__l2_norm_calculation:
            norm_number = self.__transformation_method()
            self.transform_x.add(norm_number)
            self.transform_y.add(norm_number)
            self.transform_z.add(norm_number)
        # sets each transformation method to the sample difference array
        elif self.__transformation_method == self.__sample_difference:
            self.transform_x = self.__transformation_method(self.ax)
            self.transform_y = self.__transformation_method(self.ay)
            self.transform_z = self.__transformation_method(self.az)
        # This will either call average_value or maximum_acceleration
        else:
            self.transform_x.add(self.__transformation_method(self.ax))
            self.transform_y.add(self.__transformation_method(self.ay))
            self.transform_z.add(self.__transformation_method(self.az))


    """
    Checks if the device has been idle for 5 seconds or if it's been active for 1 
    second. This will either cause the motor to buzz or another message displaying that the person has
    been active.
    @:param current_time: The current time the program is at 
    """
    def __check_idle(self, current_time):
        # If it's been 5 seconds since the last time the person has been inactive
        if current_time - self.__last_idlecheck_time >= 5:
            # get the average acceleration over 5 seconds
            average_x = self.__average_value(self.ax)
            average_y = self.__average_value(self.ay)
            average_z = self.__average_value(self.az)
            print(average_x, ",", average_y, ",", average_z)
            self.__last_idlecheck_time = current_time
            # if the device has been idle for 5 seconds, buzz the motor
            if self.__is_inactive(average_x, average_y, average_z):
                self.__idle_state = True
                self.comms.send_message("Buzz motor")
            else:
                self.__idle_state = False
        # If the person has been inactive but has become active for 1 second
        if self.__idle_state and current_time - self.__last_active_time >= 1:
            self.__last_active_time = current_time
            # get the average values for the last 1 second
            average_x = self.__average_value(self.ax[200:])
            average_y = self.__average_value(self.ay[200:])
            average_z = self.__average_value(self.az[200:])
            if not self.__is_inactive(average_x, average_y, average_z):
                print("Active accelerations: ", average_x, average_y, average_z)
                self.__last_idlecheck_time = current_time  # this ensures that the person must be inactive for 5 seconds after their activity
                self.comms.send_message("Keep it up!")

    """
    Runs all the processing for the Serial communication, including plotting the 
    acceleration values and checking whether the device has been inactive or not. 
    """
    def run(self):
        self.comms.clear()  # just in case any junk is in the pipes
        self.comms.send_message("wearable")  # begin sending data
        try:
            previous_time = 0
            while (True):
                message = self.comms.receive_message()
                if (message != None):
                    try:
                        (m1, m2, m3, m4) = message.split(',')
                    except ValueError:  # if corrupted data, skip the sample
                        continue
                    # Record the acceleration and transformation
                    self.__record_acceleration(m1,m2,m3,m4)
                    self.__record_transformation(m2,m3,m4)
                    current_time = time()
                    if current_time - previous_time > self.__refresh_time:
                        previous_time = current_time
                        self.__plot()
                    self.__check_idle(current_time)

        except(Exception, KeyboardInterrupt) as e:
            print(e)  # Exiting the program due to exception
        finally:
            print("Closing Connection")
            self.comms.send_message("sleep")  # stop sending data
            self.comms.close()
            sleep(1)

processing_unit = Processing("average acceleration", "/dev/cu.AkshayBluetooth-ESP32SPP")
processing_unit.run()

