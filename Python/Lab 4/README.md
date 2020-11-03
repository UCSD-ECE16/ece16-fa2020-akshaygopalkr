# Python Code for Lab 4

## Summary 
> In this lab, we were introduced to more advanced concepts in Python. First, 
> we learned about object oriented programming, which allows us to encapsulate data 
> and abstract various features of our programs. This allows for easier reuseability 
> of code through options like inheritance and lets users use class features without 
> needing to understand the processing and code behind the hood. Next, we learned about 
> Numpy, a Python library that allows us to operate on higher dimension arrays. Not only that, but 
> we can also use Numpy to compute complex mathematical transformations on our data. Finally, 
> we utilized Matplotlib for plotting data in Python. We can use this to use subplots to plot multiple 
> acceleration values as well perform live plotting to update our data instantaneously. We had to use 
> all these concepts and libraries throughout our challenges to make an idle detector as well as plotting 
> acceleration values 
---

## tutorial_oop_dog 
> This tutorial program provided an example of OOP through a Dog class. In this class, 
> there were private fields that could not be accessed outside the class 
> as well as public methods that instances of this class can call. Using the constructor, 
> we created instances of the Dog class and called various methods to observe the 
> instance's behavior. 
    
    scout = Dog("Scout", 2, "Belgian Malinois")
    skippy = Dog("Skippy", 5, "Golden Retriever")
    scout.define_buddy(skippy)
    scout.buddy.description()
---

## tutorial_numpy 
> This tutorial required us to create Numpy arrays using methods like 
> vstack, hstack, arange, or access features of Numpy arrays through features
> like np.shape. In this tutorial, I learned how Numpy can allow you to easily perform 
> operations on arrays and extract mathematical information about them. Not only that, but it allows 
> for people to use higher dimension array which is important in fields like machine 
> and deep learning. 
    
     # Example numpy commands 
     print(array1.shape)
     array6 = np.zeros((3, 4))   
     array5 = np.linspace(0, 100, 49, True)
     array3 = np.vstack((array3, array3, array3, array3))
---

## tutorial_plotting_basics 
> For this tutorial, we learned the basics of Matplotlib, using arrays 
> to create Python plots. I learned how to use subplots to plot multiple plots
> on one figure and labeling axis of plots.
    
      def part_three():
        a = np.array([[1, 2, 3, 4], [1, 4, 9, 16]])
        x = a[0, :]  # index from a to get [1,2,3,4]
        y = a[1, :]  # index from a to get [1,4,9,16]
        plt.title("First plot!")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.plot(x, x)
        plt.show()
---

## tutorial_plotting_wearable
> This file took what we learned from the first plotting tutorial and applied it 
> to plotting acceleration values from the accelerometer through Serial communication. 
> In this tutorial, we sampled data from the accelerometer at 50 Hz for 10 seconds. Once 
> the data was fully read, we plotted out each of the acceleration values 
> onto the figure. 

    # Read accelerometer data 
    m1, m2, m3, m4) = message.split(',')
    times[count] = int(m1)
    ax[count] = int(m2)
    ay[count] = int(m3)
    az[count] = int(m4)
    
    # Plotted out the acceleration in each direction
    plt.subplot(311)
    plt.plot(times, ax)
    plt.subplot(312)
    plt.plot(times, ay)
    plt.subplot(313)
    plt.plot(times, az)
    plt.show()
---

## tutorial_live_plotting 
> Now, this program takes data from the accelerometer but live plots 
> it onto our computer. To perform this, we had to decouple our plotting from 
> all of our other processes like sampling. Moreover, we utilized a circular list, 
> which behaves like a first-in first out buffer of data. We could then plot this 
> circular list to get the most recent samples of acceleration.

    # Example of how we decoupled plotting 
    current_time = time()
        if (current_time - previous_time > refresh_time):
            previous_time = current_time
            plt.cla()
            plt.plot(ax)
            plt.show(block=False)
            plt.pause(0.001)
---

## Challenge 1: Sensor Sensing
> In this challenge, we performed live plotting with sampling data from the accelerometer 
> and performed mathematical transformations on this data using Numpy. All of these transformations could easily be performed 
> by calling a method from the Numpy library. Some observations I had from these transformations 
> was that the average x,y, and z values are not zero even when the the accelerometer is not moving. These average values 
> were important for the next challenge so I could find thresholds that define when the device is idle or not. Moreover,
> there was a good amount of fluctuation in each sampling whether I was moving the accelerometer or keeping it 
> still. 

    # Example transformations 
    np.average(np.array(acceleration_list))
    np.diff(np.array(acceleration_list))
    np.linalg.norm(np.array([ax,ay,az]))
    np.linalg.norm(np.array([ax,ay,az]), ord=1)
    int(np.max(np.array(acceleration_list)))

## Challenge 2: Idle Detector 
> For this challenge, we again sampled data from the accelerometer and then used it 
> to determine or not whether the person was not moving. To approach this problem, I had to fine 
> well defined thresholds. When the average acceleration values over 5 seconds were below this threshold, then I would 
> know that the person has been inactive. I also used a state machine for this problem. In this case, there were only two 
> states: Being inactive or active. Each state resulted in different messages being sent to the microcontroller 

    # Checks if the device has been idle for 5 seconds
    if is_inactive(average_x, average_y, average_z):
        idle_state = True
        comms.send_message("Buzz motor")
    
    if not is_inactive(average_x, average_y, average_z):
        last_idlecheck_time = current_time # this ensures that the person must be inactive for 5 seconds after their activity
        comms.send_message("Keep it up!")

## Challenge 3: Processing Class
> This Python file contains a class which combines the tasks in Challenge 1 and 2 
> and abstracts all their operations. With this class, the user should be able to define 
> an instance of the class and then run a method which performs live plotting with a specified 
> transformation as well as detect whether or not the device is idle. 

    def __init__(self, transformation_method, port_name):

> For the constructor, I passed in the transformation method as well as the port name 
> that would be used for communication. I had many other fields that would 
> keep track of acceleration, transformation values, plotting variables, and variables 
> necessary for idle detection. 

    """
    Runs all the processing for the Serial communication, including plotting the 
    acceleration values and checking whether the device has been inactive or not. 
    """
    def run(self):

> This was the only public method I created, and this runs all the 
> processing necessary. In this method, I called various private methods, which were 
> used to compute transformations, plotting, or idle detection. This method uses 
> a try catch block which terminates once the user enter Control C. 
    
    



