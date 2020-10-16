const int accelX = A0;

void setup() {
  Serial.begin(9600);
  pinMode(accelX, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  int accel_val = analogRead(accelX);
  Serial.println(accel_val);
}
