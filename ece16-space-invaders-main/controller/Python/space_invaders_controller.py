"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.Communication import Communication
from time import sleep
import socket, pygame
import numpy as np

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

class PygameController:
  comms = None
  filename = "./scores/topscores.csv"

  def __init__(self, serial_name, baud_rate):
    self.comms = Communication(serial_name, baud_rate)

  # Save data to file
  def save_data(self, filename, data):
    np.savetxt(filename, data, delimiter=",")

  # Load data from file
  def load_data(self, filename):
    return np.genfromtxt(filename, delimiter=",")

  """
  Receives a message from the server 
  @:return: the message sent from the server 
  """
  def receive_from_server(self):
    game_status = None
    # Receive game status
    try:
      game_status, _ = mySocket.recvfrom(1024)
      game_status = game_status.decode('utf-8')
    except:
      pass

    return game_status

  """
  Orders the top three scores with the score from 
  the last round
  @:param top_scores: the last top three scores
  @:param score: the score from the last round 
  @:return: the new top three scores 
  """
  def order_top_scores(self, top_scores, score):
    top_scores.append(score) # add the score from last round to the top scores
    top_scores.sort(reverse=True) # sort all the scores from greatest to least
    return top_scores[:len(top_scores)-1] # return the new top scores with the lowest score removed


  """
  Updates the top three scores of the user after their game is zero
  @:param score: The score the user got in their last game 
  @:return: message send to Arduino which contains the top three scores 
  """
  def update_top_scores(self, score):

    # Load the top three scores from the file and sort them
    # from greatest to least
    top_scores = list(self.load_data(self.filename))
    top_scores.sort(reverse=True)

    # Update the top three scores and save them to the file
    top_scores = self.order_top_scores(top_scores, score)
    self.save_data(self.filename, np.array(top_scores))

    # This is the message that will be sent to the MCU to be displayed on the LED
    message = "Top Scores:" + "," + "#1: " + str(int(top_scores[0])) + "," + "#2: " + str(int(top_scores[1]))
    message = message + "," + "#3: " + str(int(top_scores[2]))
    return message

  """
  Method that only terminates once the game is 
  ready to start 
  """
  def wait_until_start(self):
    # Wait until the user starts the game again
    while True:
      game_status = self.receive_from_server()
      if game_status == "START":
        print("Game started")
        self.comms.send_message("start")
        break
  """
  Checks the current game status, which is sent by the server 
  @:param game_status: a string which represents the game status 
  """
  def check_game_status(self, game_status):

    # If the game ends, we stall sending data until a new game starts
    if game_status is not None and "GAME OVER" in game_status:

      # make sure data sending is stopped by ending streaming once game is over
      self.comms.send_message("stop")
      self.comms.clear()

      print("GAME OVER...")

      score = game_status.split(",")[1] # Get the score from the last round
      message = self.update_top_scores(int(score)) # Update the top three scores
      print(message)
      self.comms.send_message(message) # send the top three score to the MCU

      self.wait_until_start()

    # If the player has been hit, buzz the motor
    elif game_status == "BUZZ":
      print("Player hit!")
      self.comms.send_message("buzz")

  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    self.comms.send_message("stop")
    self.comms.clear()

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    mySocket.send("CONTROLLER ON".encode('utf-8'))

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Waiting for game to start...")
    self.wait_until_start()

    print("Use <CTRL+C> to exit the program.\n")
    while True:
      message = self.comms.receive_message()
      if(message != None):
        command = None
        message = int(message)
        if message == -1:
          self.comms.send_message("LOW BATTERY")
          command = "QUIT"
        elif message == 0:
          command = "FLAT"
        elif message == 1:
          command = "UP"
        elif message == 2:
          command = "FIRE"
        elif message == 3:
          command = "LEFT"
        elif message == 4:
          command = "RIGHT"
        elif message == 5:
          command = "FIRE LEFT"
        elif message == 6:
          command = "FIRE RIGHT"
        elif message == 10:
          command = "PAUSE"
        elif message == 11:
          command = "PLAY"
        if command is not None:
          mySocket.send(command.encode("UTF-8"))
        print(command)

      # Check the current game status
      game_status = self.receive_from_server()

      self.check_game_status(game_status)




if __name__== "__main__":
  serial_name = "/dev/cu.ag-ESP32SPP"
  baud_rate = 115200
  controller = PygameController(serial_name, baud_rate)

  try:
    controller.run()
  except(Exception, KeyboardInterrupt) as e:
    print(e)
  finally:
    print("Exiting the program.")
    controller.comms.send_message("stop")
    controller.comms.close()
    mySocket.send("QUIT".encode("UTF-8"))
    mySocket.close()

  input("[Press ENTER to finish.]")
