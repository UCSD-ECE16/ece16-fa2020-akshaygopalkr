const int BUTTON_PIN = 14;
float time_when_pressed = 0; //the time the button was last pressed 
bool prev_state = HIGH; //the previous state of the button 
bool pressed = false; //detects whether the button is currently being pressed

//set up the Button
void setupButton()
{
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

/**
 * if the button has been pressed (gone from HIGH to LOW),
 * return true
 */
bool just_pressed(bool curr_state)
{
  return prev_state == HIGH && curr_state == LOW;
}

/**
 * if the button has been pressed (gone from LOW to HIGH),
 * return true
 */
bool just_released(bool curr_state)
{
  return prev_state == LOW && curr_state == HIGH;
}

//checks whether the button has been pressed long enough to be pressed 
bool check_reset()
{
  bool curr_state = digitalRead(BUTTON_PIN);
  //start the timer for the button once i pressed it 
  if(just_pressed(curr_state))
  {
    time_when_pressed = millis();
    pressed = true;
  }
  //if the button has been released then it is no longer pressed
  if(just_released(curr_state))
    pressed = false;
  //if it's been 2 seconds and the button has been pressed
  prev_state = curr_state;
  if(pressed && millis() - time_when_pressed >= 2000)
  {
    time_when_pressed = millis(); // update the time when pressed to account for any overlap
    return true;
  }
  return false;
}
