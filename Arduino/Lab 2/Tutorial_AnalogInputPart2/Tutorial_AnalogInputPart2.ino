
int ax = 0;
int ay = 0;
int az = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  setupAccelSensor();
}

void loop() {
  // put your main code here, to run repeatedly:
  // Send to Serial Plotter. Notice only the last print has a newline.
  readAccelSensor();
  Serial.print(ax);
  Serial.print(",");
  Serial.print(ay);
  Serial.print(",");
  Serial.println(az);
}
