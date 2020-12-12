/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;


unsigned long last_buzzed = millis();
bool buzz = false;

bool pause_game = false;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupButton();
  setupPhotoSensor();
  setupMotor();
  sending = false;

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
}

/*
 * The main processing loop
 */
void loop() {
  // Parse command coming from Python (either "stop" or "start")
  String command = receiveMessage();
  if(command == "stop") {
    sending = false;
    writeDisplay("Waiting...", 0, true);
  }
  else if(command == "start") {
    sending = true;
    resetZeroValues();
    pause_game = false;
    writeDisplay("Playing!", 0, true);
  }
  // If the buzz command is sent start buzzing the motor 
  else if(command == "buzz")
  {
    buzz = true;
    activateMotor(255);
    last_buzzed = millis();
  }
  else if(command == "LOW BATTERY")
  {
    sending = false;
    writeDisplay("Recharge battery...", 0, true);
  }
  // If the command shows the top three scores, write them to the LED Display
  else if(command.substring(0,3) == "Top")
  {
    writeDisplayCSV(command, 3);
  }
  // Send the orientation of the board
  if(sending && !pause_game && sampleSensors()) {
    sendMessage(String(getOrientation()));
  }

  // If it's been one second since the buzz message has been sent deactivate the motor 
  if(buzz && millis() - last_buzzed > 1000)
  {
    deactivateMotor();
    buzz = false;
  }

  if(buttonPressed() && sending)
  {
    pause_game = !pause_game;
    if(pause_game)
    {
      sendMessage("10");
      writeDisplay("Paused.", 0, true);
    }
    else
    {
      sendMessage("11");
      writeDisplay("Playing!", 0, true);
    }
  }
}
