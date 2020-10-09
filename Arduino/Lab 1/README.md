# Lab 1
Akshay Gopalkrishnan A15832133

---
### Description of Lab
>This lab introduced us to microcontrollers, requiring us 
use to utilize digital and serial communication in order to 
>properly finish the challenges. Not only that, but I also learned
>how I can use Arduino code to interact with a circuit using the microcontroller. 
---
### Digital Communication Tutorial
    pinMode(LED_PIN, INPUT_PULLUP);
>In digital communication, input and outputs are ideally 0s and 1s. However,
>sometimes these values can be ambiguous, so Arduino provides us with a built in 
>pull up resistor to make the readings more defined.

    if (digitalRead(BUTTON_PIN) == LOW) {
        digitalWrite(LED_BUILTIN, HIGH);     
    }
    // if the button is not pushed down, turn the LED off
    else {
        digitalWrite(LED_BUILTIN, LOW); // turn the LED off
    }
> This is a code example of using Digital Read and Digital Write. Using digitalRead(), we 
>can read a digital input from a button, which can be used to determine whether or not we turn on or off 
>an LED. 
>
---
### Serial Communication Tutorial 
    Serial.begin(9600);
    Serial.print("Hello world\n");

> This is an example of a Serial write, which allows us to data from the MCU
> to the computer. 

    if(Serial.available() > 0)
        char incoming_data = Serial.read();
> With a Serial Read, we can send data from the Serial Monitor on the computer
> to the MCU. 
---
### Challenge #1: Blinking LEDs
    void blink_with_delays(int delay_one, int delay_two)
    {
        digitalWrite(LED_PIN, HIGH);
        delay(delay_one);
        digitalWrite(LED_PIN, LOW);
        delay(delay_two);
    }
>This function takes in two delay times, and uses them to turn the LED on and off for a certain period
>of time. 

    void blink_with_frequency(int freq)
    {
        double delay_time = 1000.0/(2*freq);
        blink_with_delays(delay_time, delay_time);
    }
>I used this method to make an LED blink with a certain frequency. To find the time 
>the LED would be on and off, I used the equation 1000.0/(2*frequency). I then 
>sent this number to the previous function blink_with_delays()
___
### Challenge #2: Stopwatch
> For this challenge, I had to program a stopwatch that could be started/stopped
> by a button. Here are some of the essential variables and decision making of my program:

    unsigned int counter = 0;
    unsigned long last_time_printed = 0;
    unsigned long last_time_incremented = 0;
    unsigned long now = 0;
    
>  The counter variable kept track of the time displayed on the stopwatch.
>  All the other variables were used to either keep track of when certain actions had last
>  occurred for the timer or the current time. 

    if(prev_state == HIGH && curr_state == LOW)
        //start or stop the timer 
        
> I stored the previous state of the button to determine when it was pushed, 
> which would then either start or stop the stopwatch. 

    if(timer_is_on)
    {
        now = millis();
        check_times();
    }

> Whenever the stopwatch was running, I would get the current time in millisecond. The 
> check_times() method determined whether it was time to print the current time
> or increment the counter variable. 
---
### Challenge 3: Timer
> This challenge required us to make a timer. Every time the user pushed the button,
> the time would increment by one second. Once the user did not push the button for three seconds, 
> then the timer would start going down to 0 and then stop. 

      if(prev_state == HIGH && curr_state == LOW)
      {
        timer++;
        button_last_pressed = now;
      }
> Every time the button was pressed, I incremented my timer variable and saved the last time the button as pressed.
       
    if(!count_down && now - button_last_pressed >= 3000)
        count_down = true;

> Once 3 seconds had passed since the button was last pressed, the timer 
> would start counting down. Every second, I would then decrement my timer
> variable till it reaches 0. Similar to Challenge #2,
> the timer prints the timer variable every 100 milliseconds. 
    
    
   

       

    
     