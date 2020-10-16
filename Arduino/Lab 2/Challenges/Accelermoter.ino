

const int Z_PIN = A0;

//set up the accelermoter 
void setupAccelSensor()
{
  pinMode(Z_PIN, INPUT);
}

//Read the z acceleration from the accelermoter
void readAccelSensor()
{
  az = analogRead(Z_PIN);
}
