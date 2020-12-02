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
/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupButton();
  setupCommunication();
  setupMotor();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  writeDisplay("Sleep", 0, true);

  
  activateMotor(255);
  delay(1000);
  deactivateMotor();
  
}

/*
 * The main processing loop
 */
void loop() {
  String command = receiveMessage();
  if(command == "sleep") 
  {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") 
  {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  // If the buzz command is sent start buzzing the motor 
  else if(command == "buzz")
  {
    buzz = true;
    activateMotor(255);
    last_buzzed = millis();
  }
  // Write the step count, heart rate, time, and weather to the LED
  else if(command != "")
  {
    writeDisplayCSV(command.c_str(), 3);
  }
  // Send the ppg data to the Python code 
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
    sendMessage(response);
  }
  // If the button is pressed send the reset message 
  if(buttonPressed())
  {
    sendMessage("reset");
  }
  // If it's been one second since the buzz message has been sent deactivate the motor 
  if(buzz && millis() - last_buzzed > 1000)
  {
    deactivateMotor();
    buzz = false;
  }
}
