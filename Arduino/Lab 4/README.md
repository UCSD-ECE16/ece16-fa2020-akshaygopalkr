# Arduino Code for Lab 4 

## Summary 
> This Arduino code reuses a lot of the code I previously wrote 
> in other labs. The main purpose of this Arduino code is to communicate with the 
> Python code, sending the acceleration values for the Python code 
> to analyze as well as receive messages from the Python code to print messages 
> or buzz the motor. I used a lot of the tabs I used in previous labs like Communication,
> Motor, Display, Accelerometer, and Sampling. 

## Tutorial Plotting Wearable 
    else if(command == "Buzz motor")
    {
        activateMotor(255);
        delay(1000);
        deactivateMotor();
        writeDisplay("You're inactive!", 0, true);
    }
    else if(command == "Keep it up!")
    {
        writeDisplay(command.c_str(), 0, true);
    }
    if(sending && sampleSensors()) {
        String response = String(sampleTime) + ",";
        response += String(ax) + "," + String(ay) + "," + String(az);
        sendMessage(response);    
    }
> This is an example of how I sent and received messages in Arduino. 
> I would sample the accelerometer readings and then combine them into one String and then 
> send this String. Then, the Python code would receive this message and perform operations 
> like plotting or idle detection. Otherwise, the Arduino code would receive messages 
> from the Python Code. Based on the message, the Arduino would turn something on in the circuit or display 
> a message onto the LED. 
