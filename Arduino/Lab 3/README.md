# Arduino Code for Lab 3

## Summary

> In this lab, I further improved my Arduino code an in particular 
> found new ways to communicate with the ESP32 using bluetooth. I reused some of the 
> code from Lab 2 that helped display messages on the LED, but I also added 
> new communication features that allowed me to gracefully switch from 
> Bluetooth to USB port communication.

---

## PySerial Tutorial

    #define USE_BT = 1
    #if USE_BT
        #include "BluetoothSerial.h"
        BluetoothSerial BTSerial;     // instantiate a BT object
        #define Ser BTSerial          // substitute Ser for SerialBT
    #else
        #define Ser Serial            // substitute Ser for Serial
    #endif
    
> Using precompiler directions, I could easily change when I wanted 
> communication types from Bluetooth to Serial port. With bluetooth, I could communicate 
> and perform actions wirelessly on my ESP32.

---

## Challenge 2: Weather Watch
    
    String weather_msg = message.substring(0, message.indexOf(',')); //first portion of the string
    String date_msg = message.substring(first_comma_idx+1, second_comma_idx); //second portion of the string
    String time_msg = message.substring(second_comma_idx+1, message.length()); //third portion of the string
    //writes each string to the LED
    writeDisplay(weather_msg.c_str(), 0, true);
    writeDisplay(date_msg.c_str(), 1, true);
    writeDisplay(time_msg.c_str(), 2, true);
    
> Whenever I sent a message from my Python code, I would first check if the Serial
> port received a message. Once it did, I had to split up the message into different 
> parts for the weather, time, and data. Then, I displayed each of these 
> on the LED. 