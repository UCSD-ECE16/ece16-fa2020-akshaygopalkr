# Lab 5
 

## Summary 
> In this lab, our ultimate goal was to make a pedometer that could 
> accurately count how many steps we were taking. To achieve this, we had to 
> learn key concepts like file io and digital signal processing. In particular, DSP
> was critical to this lab, as it allowed us to filter out noise from our data 
> and provide us with cleaner signals that we could easily analyze with python.
> There were many different filtering techniques we used like detrending, moving averages, 
> and low pass filters. In the challenges, we built our own filtering techniques that 
> could more accurately count steps than a baseline filtering algorithm. 

---

## File IO Tutorial
> To access offline data or save online data into a file, we needed to use 
> Python file IO. In this case, we sampled acceleration values in the x,y,z 
> direction and saved them to a file for future use or testing. 


    # Save data to file
    def save_data(filename, data):
        np.savetxt(filename, data, delimiter=",")

    # Load data from file
    def load_data(filename):
        return np.genfromtxt(filename, delimiter=",")


---

## Filtering Tutorial 
> This tutorial first introduced us to how we can make our own 
> filtering functions like detrending and moving averages. Then, we 
> implemented these functions along with the methods provided by scipy, a filtering
> library in Python.  

    """ 
    Our own method that computes a moving average for a certain 
    window "win"
    """
    def moving_average(x, win):
        ma = np.zeros(x.size)
        for i in np.arange(0,len(x)):
            if(i < win): # use mean until filter is "on"
                ma[i] = np.mean(x[:i+1])
            else:
                ma[i] = ma[i-1] + (x[i] - x[i-win])/win
        return ma
        
    """
    An example of a method that uses the scipy class
    """
    def create_filter(order, cutoff, btype, fs):
        b, a = sig.butter(order, cutoff, btype=btype, fs=fs)
        return b, a


---

## Tutorial DSP Module 
> This tutorial required us to make a DSP class, which contained some of them methods 
> we made in the previous tutorial but wraps them into a class. Then, in the 
> tutorial_dsp module file, we used some of these methods together in tandem 
> to perform some baseline filtering on a signal, which allowed us to better 
> see the amount of steps from offline data we took. 

    # Some example method calls using the DSP class 
    l1 = filt.l1_norm(ax, ay, az)      # Compute the L1-Norm
    ma = filt.moving_average(l1, 20)   # Compute Moving Average
    dt = filt.detrend(ma)              # Detrend the Signal


---

## Tutorial Pedometer Offline/Online 
> To build a pedometer, we first added to our ECE 16 library, implementing 
> a new Pedometer class. This class samples data from the accelerometer and 
> performs a baseline filter on the signal. This filtering is not perfect, and 
> something we would improve on in future challenges. Using this class, we both tested 
> it on offline and online data.


    ma = filt.moving_average(x, 20)  # Compute Moving Average
    dt = filt.detrend(ma)  # Detrend the Signal
    lp = filt.filter(self.__b, self.__a, dt)  # Low-pass Filter Signal
    grad = filt.gradient(lp)  # Compute the gradient
    x = filt.moving_average(grad, 20)  # Compute the moving average of the gradient

---

## Challenge 1: Step Counter
> One of the problems that I noticed in different samples of different 
> filtered data was that the thresholds would be different for each time. In our original situation,
> we hardcoded these thresholds, which did not make them very adaptable and always representable of the 
> data. Therefore, I thought a good idea would be the use a smart threshold that could 
> adapt based on the peak values in the filtered data. Once we processed our signal, we found 
> all the values of each peak and took their average. We would use this and 
> the standard deviation of all the peak values to find a better lower threshold and 
> upper threshold for peak and step detection. 
>
    # How we found the new thresholds 
    def detect_thresholds(filtered, peaks):
        peak_avg = np.average(np.array(filtered[peaks]))
        peak_std = np.std(np.array(filtered[peaks]))
        thresh_low = peak_avg - (2.5 * peak_std)
        thresh_high = peak_avg + (2.5 * peak_std)
        return thresh_low, thresh_high
--- 

## Challenge 2: Online Pedometer 
> For the live data, to learn the users lower and upper thresholds 
> for step detection we included a calibration step. This would ask the user to 
> walk for 10 seconds in order collect samples. Then, we would filter this data and perform the 
> same operation in challenge 1 to find better upper and thresholds that better fit the user. Once we 
> defined these thresholds, we could now perform live step detection and updating using 
> the calibrated thresholds. 
    
    # Method that would collect calibration data and then 
    # define lower and upperthresholds using the filtered data 
    def calibrate_thresholds():
        data = collect_samples()
        ax = data[:, 1]
        ay = data[:, 2]
        az = data[:, 3]
        ped = Pedometer(500, 50, [])
        ped.add(ax, ay, az)
        _, peaks, filtered = ped.process()
        return detect_thresholds(filtered, peaks)

---

