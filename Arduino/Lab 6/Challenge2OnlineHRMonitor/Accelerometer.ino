

const int Z_PIN = A2;
const int Y_PIN = A3;
const int X_PIN = A4;

//set up the accelermoter 
void setupAccelSensor()
{
  pinMode(Z_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(X_PIN, INPUT);
}

//Read the z acceleration from the accelermoter
void readAccelSensor()
{
  az = analogRead(Z_PIN);
  ax = analogRead(X_PIN);
  ay = analogRead(Y_PIN);
}
