int sampleTime = 0; // Time of last sample (in Sampling tab)
// Acceleration values recorded from the readAccelSensor() function
int ax = 0;         
int ay = 0;
int az = 0;
bool sending = false;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  //setupMotor();
}

void loop() {
  String command = receiveMessage();
  if(command == "sleep")
    sending = false;
  else if(command == "wearable")
    sending = true;
  else if(command == "Buzz motor")
  {
    activateMotor(255);
    delay(1000);
    deactivateMotor();
    writeDisplay("You're inactive!", 0, true);
  }
  else if(command == "Keep it up!")
  {
    writeDisplay(command.c_str(), 0, true);
  }
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }
}
