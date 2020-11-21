# Arduino Code for Lab 6

## Summary
> For the Arduino Code in this Lab, we were introduced to a new device that we had to 
> sample: a Photosensor. This device uses I2C communication, so we could communicate with the 
> LED and photosensor using I2C. and still have a functioning device. The majority of the Arduino 
> code was centered on configuring this new device, and also integrating with our wearable device code 
> in order to get live samples from the photosensor to calculate the heart rate
> of someone. 

---

## Tutorial 1:  Photoplethysmography

#### Questions
> 1. With I2C Communication, we are allowed to communicate with multiple sensors. Each sensor will share the same clock 
> and have a unique address that allows the MCU to identify which device it should send or receive 
> data too.
> 2. With this while(1) command, the program will stay inside of this if loop and none 
> of the other code will be executed. If we try and reconnect or change anything in our circuit, nothing will change, as the program will still 
> be inside of the if loop. Therefore, we will need to reconfigure what is wrong and then reupload the code 
> to check if the sensor is now connected. 
> 3. IF we had a a led brightness of 25 mA, then the ledBrightness variable should 
> be 255/2 = 127.5. For Red + IR LEDs, then ledMode should be set to 2. To sample at 200 Hz, 
> the variable sampleRate should be set to 200 Hz. And for an adcRange of 8192, adcRange should be set 
> to 8192. 
> 4. The units of the pulse width are in nanoseconds. If there is a bigger pulse width, 
> then the measurement would be more intense. With Pulse Width Modulation, more intense measurements 
> have a longer pulse width. 
> 5. To have an ADC range of 16384, we would need to have 14 bits. To calculate this, I 
> did the log(16384) with a base of 2.
> 6. Peak Wavelength for Red LED: 670 nm
>    Peak Wavelength for Green LED: 545 nm
>    Peak wavelength for IR LED: 900 nm
> 7. To read the green value, I would need to set the ledMode = 3. 
> Then, to read the green signal I would call getGreen() instead of getIR(). 

---

## TutorialPPG2
> Once we had the PPG readings set up in the previous tutorial, we could 
> now could combine these readings with also sampling analog accelerometer values 
> from the accelerometer. To do this, we modified the sampleSensors() method, which now 
> now called methods to read the photosensor and accelerometer. 

    readAccelSensor();     // values stored in "ax", "ay", and "az"
    readPhotoSensor(); //value stored in "ppg"
---

## Challenge 2: Online HR Monitor
> For the online HR monitor, there were two critical components the 
> Arduino code had to accomplish. First, we needed our Arduino code to sample from the Photosensor 
> and send these values to the Python code for analysis. Then, the Arduino code 
> should receive the heart rate the Python code computes and display it on the LED. Everything else 
> was similar to the wearable device code we previously used, using the Communication, Display, 
> and Sampling Tabs to carry out sampling values from the hardware and displaying messages on the LED.

    // This will write the heart rate to the LED Display
    else if(command != "")
    {
        writeDisplay(command.c_str(), 0, true);
    }
    
    // Send the ppg data and time to the Python Code
    if(sending && sampleSensors()) 
    {
        String response = String(sampleTime) + ",";
        response += String(ax) + "," + String(ay) + "," + String(az);
        response += "," + String(ppg);
        sendMessage(response);
    }
    
    