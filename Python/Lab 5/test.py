from ECE16Lib.Communication import Communication
import serial
ser = serial
try:
    ser = serial.Serial("/dev/cu.ag-ESP32SPP", 115200)


except ser.serialutil.SerialException:
    print("port is in use")
    ser = serial.Serial()
    ser.close()