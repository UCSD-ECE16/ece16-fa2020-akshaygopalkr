
unsigned int counter = 0; //keeps tracks of the seconds on the timer

bool timer_is_on = false; //boolean of whether the timer is on
const int BUTTON_PIN = 14; //The PIN # of the button

bool prev_state = LOW; //the previous state of the Button

//variables to keep track of times some actions occurred
unsigned long last_time_printed = 0;
unsigned long last_time_incremented = 0;
unsigned long now = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

//prints out the current time on the counter variable
void print_timer()
{
    Serial.print("Time: ");
    Serial.println(counter);
}

/** Checks whether the counter needs to be incremented or 
 *  if the time needs to be printed
 */
void check_times()
{
  /**
   * If it's been 1 second since counter was last incremented,
   * increment timer now. 
   */
  if(now-last_time_incremented >= 1000)
  {
    counter++;
    last_time_incremented = now;
  } 

  /**
   * If it's been 100 milliseconds since the timer was last printed,
   * print the timer now 
   */
  if(now - last_time_printed >= 100)
  {
    print_timer();
    last_time_printed = now; 
  }
}

void loop() {
 // put your main code here, to run repeatedly:
  bool curr_state = digitalRead(BUTTON_PIN);

  //if the button has been pressed
  if(prev_state == HIGH && curr_state == LOW)
  {
    timer_is_on = !timer_is_on; //flips the state of the timer
    unsigned long temp = now; 
    now = millis(); //get the time the button was just pressed 
    if(timer_is_on)
    { 
      /*This makes sure after we start the time again that 
       * the last time counter was printed or incremented is consistent
       * with before we stopped the timer
       */
      last_time_incremented = now - (temp - last_time_incremented);
      last_time_printed = now - (temp - last_time_printed);
    }
  }

  /*
   * If the timer is on get the current time and check
   * whether the time needs to be printed or incremented
   */
  if(timer_is_on)
  {
    now = millis();
    check_times();
  }
  prev_state = curr_state; //set the previous state to current state
}
