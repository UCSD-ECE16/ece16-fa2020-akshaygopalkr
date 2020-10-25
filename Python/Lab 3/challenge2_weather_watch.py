import pyowm
from pyowm import OWM
from datetime import date
from datetime import datetime
import serial  # the PySerial library
import time  # for timing purposes

# Sets up Serial communication
def setup(serial_name, baud_rate):
    ser = serial.Serial(serial_name, baudrate=baud_rate)
    return ser

# Closes the Serial port
def close(ser):
    ser.close()

# Sends a message to Serial
def send_message(ser, message):
    if message[-1] != "\n":  # we add a newline character so we know we've received a completed message
        message = message + "\n"
    ser.write(message.encode('utf-8')) # Need to encode String message to a type utf-8

"""
Receive a message from Serial and limit it to num bytes (default of 50)
"""
def receive_message(ser, num_bytes=50):
    if ser.in_waiting > 0:
        return ser.readline(num_bytes).decode('utf-8') # to receive a message you decode it back to a String
    else:
        return None

# Set up Bluetooth connection and API key for pyowm
owm = OWM('0b8f49521da5313875dc27259de862cd').weather_manager()
ser = setup("/dev/cu.AkshayBluetooth-ESP32SPP", 115200)
time.sleep(3) # I have a cheap dongle that delays board reset so I need to wait some time before sending the message

while True:
    time.sleep(1) # Update weather, data, and time every one second
    weather = owm.weather_at_place('San Diego,CA,US').weather # Get the current weather using the OWM library
    weather_str = "Temp: " + str(weather.temperature('fahrenheit')['temp'])
    date_str =  "," + "Date: " + str(date.today())
    # Shows the current time in a digital fashion
    time_str = "," + str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + ":" + str(datetime.now().time().second)
    msg = weather_str + date_str + time_str # combines weather, data, and time, strings together
    send_message(ser, msg + "\n") #sends the message to the Serial port








