# Python Code for Lab 3


## Summary
> In this lab, we were introduced to Python and its various benefits 
> and applications it can be applied to. First, we learned the basics 
> of Python and learned about strings, methods, data types, and data 
> structures. Then, we applied Python to Serial Communication, learning how 
> we could combine Python communication and Arduino to communicate with the
> ESP32. In our labs, we used Python to send messages to the Serial port that 
> could then be displayed on our LED. 

---
## Python Basics Tutorial
    numbers = [10, 114, 567, 8, 9] # list of integers
    print(numbers[0:3]) # prints [10,20,30]: slice from 0 to 3 (exclusive)
    print(numbers[:3]) # prints [10,20,30]: slice from 0 to 3 (exclusive)
    print(numbers[4:7]) # prints [50,60,70]: slice from 4 to the end of the list
    print(numbers[:]) # prints [10,20,30,40,50,60,70], slice of the whole list
> This tutorial had various examples of coding nuances
> or important features of Python. For example, this snippet code
> shows one Python's most helpful tools: slicing. This allows us to 
> take a portion of any data type. 
    
    
---

## Pyserial Tutorial
     def send_message(ser, message):
        if message[-1] != "\n":  # we add a newline character so we know we've received a completed message
            message = message + "\n"
        ser.write(message.encode('utf-8'))
     
    def receive_message(ser, num_bytes=50):
        if ser.in_waiting > 0:
            return ser.readline(num_bytes).decode('utf-8')
        else:
            return None
> These were functions that we created to send and receive messages
> using Python code to the Serial Port. To send messages, I had to encode 
> my string into a type utf-8. For receiving messages, I had to decode 
> the type utf-8 back into a String. 
 ---
 
## Challenge 1: Pig Latin
    if msg_arr[i][0] in vowels:
        msg_arr[i] += "yay"
    # General case for consonants 
    msg_arr[i] = msg_arr[i][first_vwl_idx:] + msg_arr[i][0:first_vwl_idx] + "ay"
> To translate from english to pig latin, there were two general cases. If the word
> started with a vowel, I would just add "yay" to the end of the string. Otherwise,
> then I would have to find the first vowel and shift everything before the first vowel
> to the end of the string. Then, I would add "ay" to the end to convert it to pig latin. There were 
> special edge cases like words that started with "y" or "qu" that I had to account for also.

    if msg_arr[i][-3:] == 'yay':  # if the word starts with a vowel, just return the word without "yay"
        msg_arr[i] = msg_arr[i][:-3]
    while not dictionary.check(temp.lower()):
        # This creates a word with the letters before "ay" or "ey" and the letters before that
        temp = msg_arr[i][letters_before:-2] + msg_arr[i][0:letters_before]
        letters_before -= 1 #subtract letters_before so we can try to put a different combination of letters before

> To translate back to English, I had to general cases. If the message started with a vowel, I just removed the 
> "yay" at the end of the message. Otherwise, I had to use the python enchant library which 
> could check if my translated words were English.

---

## Challenge 2: Weather Watch

    weather = owm.weather_at_place('San Diego,CA,US').weather # Get the current weather using the OWM library
    weather_str = "Temp: " + str(weather.temperature('fahrenheit')['temp'])
    date_str =  "," + "Date: " + str(date.today())
    time_str = "," + str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + ":" + str(datetime.now().time().second)

> Python libraries helped me access the current weather, data, and time. 
> I updated these every 1 second and then used Bluetooth communication to 
> display these on the LED display. 