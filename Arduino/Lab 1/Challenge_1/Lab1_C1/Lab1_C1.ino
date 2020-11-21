const int LED_PIN = 14;


void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN, OUTPUT);
}

void blink_with_frequency(int freq)
{
  double delay_time = 1000.0/(2*freq);
  blink_with_delays(delay_time, delay_time);
}

void blink_with_delays(int delay_one, int delay_two)
{
  digitalWrite(LED_PIN, HIGH);
  delay(delay_one);
  digitalWrite(LED_PIN, LOW);
  delay(delay_two);
}

void loop() 
{
  // put your main code here, to run repeatedly:
  //blink_with_frequency(1);
  //blink_with_frequency(10);
  //blink_with_frequency(50);
  //blink_with_delays(1000, 100);
  //blink_with_delays(200, 50);
  blink_with_delays(20,10);
 
}
