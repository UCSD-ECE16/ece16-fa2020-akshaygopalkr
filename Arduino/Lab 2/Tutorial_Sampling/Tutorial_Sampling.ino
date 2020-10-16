int sampleTime = 0; // Time of last sample (in Sampling tab)
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; 
int ay = 0;
int az = 0;

void setup () {
  setupAccelSensor();
  setupDisplay();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Note: we only print values when we have a new sample!!!
  if( sampleSensors() ) 
  {
    Serial.print(ax);
    Serial.print(",");
    Serial.print(ay);
    Serial.print(",");
    Serial.println(az);
   }

}
