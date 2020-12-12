bool prev_state = LOW; //the previous state of the button
const int BUTTON_PIN = 14; //PIN # for the Button 

void setupButton()
{
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

boolean buttonPressed()
{
  boolean pressed = false;
  bool curr_state = digitalRead(BUTTON_PIN);
  if(prev_state == HIGH && curr_state == LOW)
    pressed = true;
  prev_state = curr_state;
  return pressed;
}
