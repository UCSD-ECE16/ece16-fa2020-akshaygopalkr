from ECE16Lib.Communication import  Communication
import time

if __name__ == "__main__":
    comms = Communication("/dev/cu.AkshayBluetooth-ESP32SPP", 115200)
    comms.clear()
    try:
        for i in range(30):
            message = str(i+1) + " seconds"
            comms.send_message(message)
            time.sleep(1)
            received_message = comms.receive_message()
            if received_message != None:
                print(received_message)
    except KeyboardInterrupt:
        print("User stopped the program with CTRL+C input")
    finally:
        comms.close()