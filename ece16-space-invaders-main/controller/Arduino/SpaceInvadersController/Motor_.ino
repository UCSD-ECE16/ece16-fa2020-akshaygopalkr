const int pwmFrequency = 5000;
const int pwmChannel = 0;
const int pwmBitResolution = 8;

const int MOTOR_PIN = 18;

//sets up the motor with PWM
void setupMotor()
{
  ledcSetup(pwmChannel, pwmFrequency, pwmBitResolution);
  ledcAttachPin(MOTOR_PIN, pwmChannel);
}

//activates the motor with a certain PWM
void activateMotor(int motorPower)
{
  ledcWrite(pwmChannel, motorPower);
}

//turns the Motor off
void deactivateMotor()
{
  ledcWrite(pwmChannel, 0);
}
