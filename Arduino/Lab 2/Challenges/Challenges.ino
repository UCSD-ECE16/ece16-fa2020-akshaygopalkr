int sampleTime = 0; //the last time a sample was occurred 
int az = 0; //current z acceleration
int last_az = 0; //the last z acceleration
int numTaps = 0; //the number of taps on the acceleromoter 
float last_tapped = 0; //when the acceleromoter was last tapped

float last_countdown = 0; //the last time the button was counting down 
/**
 * State descriptions:
 * 0: Waiting for Triggers
 * 1: Countdown process
 * 2: Buzz Motor
 */
int state = 0; 

const int ACCEL_DIFF_ON_TAP = 85;

void setup() {
  //set up all the sensors and displays 
  setupAccelSensor();
  setupButton();
  setupDisplay();
  setupMotor();
  Serial.begin(115200);
  Serial.println(state);
}

//displays the amount of taps onto the LED monitor 
void displayTaps()
{
  String message = String(numTaps) + " taps";
  writeDisplay(message.c_str(), 0, true); //clear the Display and display the new value of taps
}

//function when circuit is at waiting for triggers state
void wait_for_trigger_state()
{
  float now = millis();
  //if it's been 4 seconds since last tap switch to countdown state
  if(now - last_tapped >= 4000 && numTaps != 0)
  {
    state = 1;
    last_countdown = now;
  }
  //if the button has been pressed for 2 seconds go to the buzz motor state 
  else if(check_reset())
  {
    numTaps = 0;
    displayTaps();
    state = 2;
  }
}

//method for when circuit is in countdown state 
void countdown_state()
{
  /**
   * check if it's been 1 second since numTaps has been decremented
   * and numTaps is not 0
   */
  float now = millis();
  if(now - last_countdown >= 1000 && numTaps !=0)
  {
    numTaps--;
    last_countdown = now;
    displayTaps();
  }
  //if the button has been pressed for 2 seconds go to the buzz motor state 
  else if(check_reset())
  {
    numTaps = 0;
    displayTaps();
    state = 2;
  }
  if(numTaps == 0) //otherwise if numTaps is equal to 0 go to the Buzz Motor state
    state = 2;
}

//method to represent when circuit is in buzz motor state 
void buzz_motor_state()
{
  activateMotor(255); //set the motor to the 100% PWM 
}

//check if there has been a tap detected
void check_for_tap()
{
  if(sampleSensors())
  {
    if(ifTapped())//if a tap is detected (z acceleration has gone down by more than 50 since last sample)
    {
      numTaps++; //increase numTaps 
      last_tapped = millis();
      displayTaps();
      //if a tap is detected from the buzz motor state turn off the motor
      if(state == 2)
        deactivateMotor();
      state = 0;
    }
    last_az = az; //save the last z acceleration 
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  //if a tap is detected 
  check_for_tap();
  //one of the state methods will be running depending on the state
  if(state == 0)
    wait_for_trigger_state();
  else if(state == 1)
    countdown_state();
  else if(state == 2)
    buzz_motor_state();
    
}

//function to tell whether accelerometer has been tapped or not
bool ifTapped()
{
  return last_az - az >= ACCEL_DIFF_ON_TAP; 
}
