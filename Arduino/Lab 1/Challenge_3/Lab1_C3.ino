
int timer = 0; //keeps track of the timer 
bool prev_state = LOW; //the previous state of the button
const int BUTTON_PIN = 14; //PIN # for the Button 
bool count_down = false; //boolean to represent when the timer is counting down 

//Time variables to check when certain actions occured 
unsigned long button_last_pressed = millis();
unsigned long last_time_decremented = millis(); 
unsigned long last_time_printed = millis();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

//Prints out the timer variable to the Serial monitor
void print_timer(unsigned long now)
{
   Serial.print("Timer: ");
   Serial.println(timer);
}


//decrements the time by now 
void decrement_time(unsigned long now)
{
  //only decrease the time if it's > 0.
  if(timer>0)
  {
    timer--;
    last_time_decremented = now; 
  }
  //if timer is 0 we should stop counting down 
  else
     count_down = false;
}

void loop() {
  
  //get the state of the button and current time 
  bool curr_state = digitalRead(BUTTON_PIN);
  unsigned long now = millis();

  /** 
   *  If the button has been pressed add to the timer variable
   *  and save the time the button was pressed
   */
  if(prev_state == HIGH && curr_state == LOW)
  {
    timer++;
    button_last_pressed = now;
  }

  /** 
   *  If it's been 3 seconds since the button has last been pressed
   *  then the timer can start counting down
   */
  if(!count_down && now - button_last_pressed >= 3000)
    count_down = true;
   

  /** 
   *  If it's been 1 second since we last decremented 
   *  the timer variable, then decrement the time variable
   */
  if(count_down && now - last_time_decremented >=1000)
    decrement_time(now);
    
  /**
   * If it's been 100 milliseconds since we last printed
   * the time, then print the time 
   */
  if(now - last_time_printed == 100)
  {
    print_timer(now);
    last_time_printed = now;
  }
  
  prev_state = curr_state; //set the previous state to the current state 
}
