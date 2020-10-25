
void setup() {
  setupCommunication();
  setupDisplay();
}

void loop() 
{
  String message = receiveMessage();
  if(message != "")
  {
    writeDisplay(message,0,true);
  }
}
