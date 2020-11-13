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
}

void loop() {
  String command = receiveMessage();
  if(command == "sleep")
    sending = false;
  else if(command == "wearable")
    sending = true;
  else if(command != "")
  {
    writeDisplay(command.c_str(), 0, true);
  }
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }
}
