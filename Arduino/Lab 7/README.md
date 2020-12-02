# Arduino Code for Lab 7

## Summary
> In this lab, we had to use a lot of our previous Arduino code 
> from other labs to build a fully functional wearable. Not only that, 
> but we also utilized Arduino code for an online heart rate monitor, which 
> reused the same code from Lab 6. Some of the 
> key concepts like non-blocking code and sending and receiving messages 
> via bluetooth were used in this lab. 
---
## Challenge 2: GMM HR Monitor 
> This code was the same exact as the Arduino code from Lab 6 that 
> performed live heart rate monitoring. First, we sampled ppg values from the Photosensor 
> and sent these values to the Python code for analysis. Then, the Arduino code 
> should receive the heart rate the Python code computes and display it on the LED. Everything else 
> was similar to the wearable device code we previously used, using the Communication, Display, 
> and Sampling Tabs to carry out sampling values from the hardware and displaying messages on the LED.

    // This will write the heart rate to the LED Display, where 
    // command contains the heart rate measured 
    else if(command != "")
    {
        writeDisplay(command.c_str(), 0, true);
    }
    
    // Send the ppg data and time to the Python Code for analysis
    if(sending && sampleSensors()) 
    {
        String response = String(sampleTime) + ",";
        response += String(ax) + "," + String(ay) + "," + String(az);
        response += "," + String(ppg);
        sendMessage(response);
    }
---

## Challenge 3: Complete Wearable
> To see the detailed state diagram explanation for this challenge, look at the README.md for Lab 7 in the 
> Python folder. For the complete wearable, we again used a lot of the common code
> that we used in previous labs like the Accelerometer, Button, Communication, LED Display, Motor, 
> Photodetector, and Sampling. Moreover, we again performed the same sampling process for the Pedometer and Photodetector,
> collecting these values and then sending them to the Python code for analyzing. 
> However, there were some key features we had to add in order 
> to have a functional wearable:

#### Buzz Motor
> If a Python message was sent to buzz the motor, then we would activate 
> the motor and buzz it for one second. In our code, we implemented non-blocking while 
> the motor was buzzing to make sure we could still collect samples while the MCU was 
> in the buzz state. 

    // If the buzz command is sent start buzzing the motor 
    else if(command == "buzz")
    {
        buzz = true;
        activateMotor(255);
        last_buzzed = millis();
    }
    // If it's been one second since the buzz message has been sent deactivate the motor 
    if(buzz && millis() - last_buzzed > 1000)
    { 
        deactivateMotor();
        buzz = false;
    }
#### Checking if the Button was pressed 
> To check if the button was pressed, we would keep track of the previous state 
> of the button. If the state ever switched from LOW to HIGH, then it must mean that 
> the button has been pressed. When this occurred, this meant that the user wanted 
> to reset the step count. As a result, a message would be sent to the Python code 
> for the step count in the Pedometer class to be reset.  

---
