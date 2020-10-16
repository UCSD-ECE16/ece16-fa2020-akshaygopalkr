
const int X_PIN = A0;
const int Y_PIN = A1;
const int Z_PIN = A2;


void setupAccelSensor()
{
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
}

void readAccelSensor()
{
  ax = analogRead(A0);
  ay = analogRead(A1);
  az = analogRead(A2);
}
