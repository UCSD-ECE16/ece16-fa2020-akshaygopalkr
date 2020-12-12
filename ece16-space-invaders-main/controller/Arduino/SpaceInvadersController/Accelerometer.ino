// ----------------------------------------------------------------------------------------------------
// =========== Accelerometer Sensor ============ 
// ----------------------------------------------------------------------------------------------------

/*
 * Configure the analog input pins to the accelerometer's 3 axes
 */
const int X_PIN = A4;
const int Y_PIN = A3;
const int Z_PIN = A2;

const int sensitivity = 100; 

const bool wired = 1; //boolean that shows whether the device is plugged in or not 


/*
 * Set the "zero" states when each axis is neutral
 * NOTE: Customize this for your accelerometer sensor!
 */
const int X_ZERO_WIRED = 1850; // zero values when wired
const int Y_ZERO_WIRED = 1830; // zero values when wired  
const int Z_ZERO_WIRED = 2350; //2350 for wired

int X_ZERO = 1750;
int Y_ZERO = 1750;
int Z_ZERO = 2250;




unsigned long last_decreased = 0;



/*
 * Configure the analog pins to be treated as inputs by the MCU
 */
void setupAccelSensor() {
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
}

/*
 * Read a sample from the accelerometer's 3 axes
 */
void readAccelSensor() {
  ax = analogRead(X_PIN); 
  ay = analogRead(Y_PIN);
  az = analogRead(Z_PIN);
}

/*
 * Resets the bluetooth zero values 
 */
void resetZeroValues()
{
 X_ZERO = 1750;
 Y_ZERO = 1750;
 Z_ZERO = 2250; 
}

/*
 * Updates the zero values 
 */
void updateZeroValues()
{
  unsigned long now = millis();
  // Don't start decreasing the zero values until the device is ready
  if(now - last_decreased >= 250)
  {
    X_ZERO -= 1;
    Y_ZERO -= 1;
    Z_ZERO -= 1;
    last_decreased = now;
  }
}

/*
 * Get the orientation of the accelerometer
 * Returns orientation as an integer:
 * -1 == LOW BATTERY
 * 0 == flat
 * 1 == up
 * 2 == down
 * 3 == left
 * 4 == right
 * 5 = left & firing
 * 6 = right & firing
 */
int getOrientation() {
  int orientation = 0;

  int x = 0;
  int y = 0;
  int z = 0;

  if(wired)
  {
    x = ax - X_ZERO_WIRED;
    y = ay - Y_ZERO_WIRED;
    z = az - Z_ZERO_WIRED;
  }
  
  else
  {
    x = ax - X_ZERO;
    y = ay - Y_ZERO;
    z = az - Z_ZERO;
    updateZeroValues();
  }

  // If the battery is discharging and the zero value is below this threshold, the battery needs to be
  // recharged 
  if(!wired && X_ZERO <= 1575)
    orientation = -1;
  /**
   * If ax and ay are both over sensitivity rate and the maginitude of the x and y acceleration 
   * are greater than the z acceleration, the device should be moving and firing.
   */
  else if(abs(x) > sensitivity && abs(y) > sensitivity && abs(x) > abs(z) && abs(y) > abs(z))
  {
    // If the device is to the left and pointed down, it should be moving left and firing
    if(x<0 && y > 0)
      orientation = 5;
    // If the device is to the right and pointed down, it should be moving right and firing
    else if(x> 0 && y>0)
      orientation = 6;
    // If the device is facing up and to the left, it will move left and not fire as well
    else if(x<0)
      orientation = 3;
    // If the device is facing up and to the right, it will move right and not fire as well
    else
      orientation = 4;
  }
  // If ax has biggest magnitude, it's either left or right
  else if(abs(x) >= abs(y) && abs(x) >= abs(z)) {
    // If the x acceleration is less than the negative sensitivity value, 
    if(x < -1*sensitivity) // left
      orientation = 3;
    else if(x > sensitivity) // right
      orientation = 4;
    else 
      orientation = 0;
  }
  // If ay has biggest magnitude, it's either up or down
  else if(abs(y) >= abs(x) && abs(y) >= abs(z)) {
    if(y < -1*sensitivity) 
      orientation = 1;
    else if(y > sensitivity)
      orientation = 2;
    else 
      orientation = 0;
  }
  // If az biggest magnitude, it's flat (or upside-down)
  else if(abs(z) > abs(x) && abs(z) >= abs(y)) {
    orientation = 0; // flat
  }

  return orientation;
}
