
const int X_PIN = A0;
const int Y_PIN = A1;
const int Z_PIN = A2;

//Sets up the accelerator pins for all directions
void setupAccelSensor()
{
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
}

//reads the acceleration in each direction from the accelermoter =
void readAccelSensor()
{
  ax = analogRead(A0);
  ay = analogRead(A1);
  az = analogRead(A2);
}
