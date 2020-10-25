
void setup() {
  setupCommunication();
  setupDisplay();
}

void loop() 
{
  String message = receiveMessage();
  if(message != "")
  {
    challenge_3_display(message);
  }
}

//Writes the weather, time, and date on seperate lines of the LED display
void challenge_3_display(String message)
{
  int first_comma_idx = message.indexOf(',');
  int second_comma_idx = message.indexOf(',', first_comma_idx+1);
  String weather_msg = message.substring(0, message.indexOf(',')); //first portion of the string
  String date_msg = message.substring(first_comma_idx+1, second_comma_idx); //second portion of the string
  String time_msg = message.substring(second_comma_idx+1, message.length()); //third portion of the string
  //writes each string to the LED
  writeDisplay(weather_msg.c_str(), 0, true);
  writeDisplay(date_msg.c_str(), 1, true);
  writeDisplay(time_msg.c_str(), 2, true);
}
