from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time

if __name__ == "__main__":
  num_samples =  100              # 2 seconds of data @ 50Hz
  refresh_time = 0.1              # update the plot every 0.1s (10 FPS)

  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)

  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  comms = Communication("/dev/cu.usbserial-1410", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data
  fig = plt.figure()
  ax1 = fig.add_subplot(311)
  ax2 = fig.add_subplot(312)
  ax3 = fig.add_subplot(313)
  try:
    previous_time = 0
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue


        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))


        # if enough time has elapsed, clear the axis, and plot az
        current_time = time()
        if (current_time - previous_time > refresh_time):
            previous_time = current_time
            ax1.cla()
            ax2.cla()
            ax3.cla()
            ax1.plot(ax)
            ax2.plot(ay)
            ax3.plot(az)
            plt.show(block=False)
            plt.pause(0.001)
  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()
