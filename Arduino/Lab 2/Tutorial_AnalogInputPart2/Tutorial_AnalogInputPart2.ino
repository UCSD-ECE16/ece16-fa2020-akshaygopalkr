
int ax = 0;
int ay = 0;
int az = 0;

int last_ax = 0;
int last_ay = 0;
int last_az = 0;

int X_ZERO = 1750;
int Y_ZERO = 1750;
int Z_ZERO = 2250;

unsigned long last_decreased = 0;

unsigned long last_printed = 0;

boolean ready = false;

void setup() {
  // put your setup code here, to run once:
  setupCommunication();
  setupAccelSensor();
}

void updateZeroValues()
{
  unsigned long now = millis();
  // Don't start decreasing the zero values until the device is ready
  if(now - last_decreased >= 250)
  {
    X_ZERO -= 1;
    Y_ZERO -= 1;
    Z_ZERO -= 1;
    last_decreased = now;
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  // Send to Serial Plotter. Notice only the last print has a newline.
  String command = receiveMessage();
  if(command  == "start")
    ready = true;
  if(ready)
  {
    if(millis() - last_printed >= 5000)
    {
      readAccelSensor();
      String message = String(last_ax - ax) + "," + String(last_ay - ay) + "," + String(last_az - az);
      last_ax = ax;
      last_ay = ay;
      last_az = az;
      sendMessage(message);
      last_printed = millis();;
    }
  }
}
