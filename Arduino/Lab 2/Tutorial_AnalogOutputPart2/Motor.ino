const int pwmFrequency = 5000;
const int pwmChannel = 0;
const int pwmBitResolution = 8;

const int MOTOR_PIN = 18;

void setupMotor()
{
  ledcSetup(pwmChannel, pwmFrequency, pwmBitResolution);
  ledcAttachPin(MOTOR_PIN, pwmChannel);
}

void activateMotor(int motorPower)
{
  ledcWrite(pwmChannel, motorPower);
}

void deactivateMotor()
{
  ledcWrite(pwmChannel, 0);
}
