# Lab 2

### Summary of Lab
> This lab introduced us to new communication styles that 
> can be used in Arduino. We learned I2C and Analog Communication,
> as well as how to sample from various sensors. Furthermore, 
> we also interacted with analog outputs using PWM, which allows
> us to specify a variety of outputs. Using all of these tools, 
> I had to make a gesture controlled watch that could detect taps
> on an acceleromoter.

---
### I2C Communication Tutorial
    
> Using I2C Communication, we can communicate with multiple devices 
> on one pin. We used I2C Communication to write to the LED display.
>
---
### Analog Input (Accelerometer) Tutorial
     const int accelX = A0;     
> We can use the analog pins to the acceleration in the x-direction
> from the accelerometer.

     int accel_val = analogRead(accelX);

> In this line of code, the x-acceleration signal is converted to 
> a voltage with a range of 0 to a reference voltage. Using an ADC, 
> a digital output is then produced which then can be processed by the CPU. 

---
### Sampling Tutorial
    bool sampleSensors() {
    timeEnd = micros();
    if(timeEnd - timeStart >= sampleDelay) {
        displaySampleRate(timeEnd);
        timeStart = timeEnd;
        // Read the sensors and store their outputs in global variables
         sampleTime = millis();
        readAccelSensor();
        return true;
    }
        return false;
    }
> This is an example of how you can sample with Arduino Code. To accomplish this,
> we used non-blocking timing code, so other operations can be performed as well
> while we check if we need to sample. In this code, we also defined sufficient sampling speeds
> that would not cause unwanted noise in our readings. 
---
### Analog Output (Buzzer Motor) Tutorial 
    void activateMotor(int motorPower)
    {
        ledcWrite(pwmChannel, motorPower);
    }

> Unlike digitalWrite(), with PWM we can provide a range of analog outputs. In this case,
> we used PWM to specify different motor strengths from 0-255. In this case, 0 would deactivate
> the motor and 255 would be 100% duty cycle. 
---

### Challenge 1: Gesture Detection
    
    bool ifTapped()
    {
        return last_az - az >= ACCEL_DIFF_ON_TAP; 
    }

> When the accelerometer is tapped, I noticed that there was a sudden decrease 
> in the z-acceleration. Therefore, to detect if the accelerometer has been tapped,
> I looked at the difference of the last z-acceleration and current z-acceleration. 
> If there is a difference greater than or equal to a difference I found through trial 
> and error, then I would know the accelerometer was tapped. 
---

### Challenge 2: Gesture Controlled Watch

    //Methods to represent each state
    void wait_for_trigger_state()
    void countdown_state()
    void buzz_motor_state()
    
    // Call each function based on the state the
    // circuit is in
    if(state == 0)
        wait_for_trigger_state();
    else if(state == 1)
        countdown_state();
    else if(state == 2)
        buzz_motor_state();
    
> For this problem, I used a state machine to solve this problem. I used three 
> different states, wait for trigger, countdown, and buzz motor, to represent each 
> situation the circuit is in. Based on the state it is currently in, I would then 
> call one of these functions which would then go through all the actions 
> of all those states and check if the state needs to be changed. 