

const int BUTTON_PIN = 14;
const int LED_PIN = 13;
void setup() 
{
  // put your setup code here, to run once:
  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  
}

void loop() {
  // if the button is pushed down, turn on the LED
     if (digitalRead(BUTTON_PIN) == LOW) {
          digitalWrite(LED_PIN, HIGH);
     }
     // if the button isn't pushed down, turn the LED off
     else 
          digitalWrite(LED_PIN, LOW); // turn the LED off

}
