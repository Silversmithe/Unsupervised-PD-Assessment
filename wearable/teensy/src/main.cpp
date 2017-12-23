/* LED Blink, Teensyduino Tutorial #1
   http://www.pjrc.com/teensy/tutorial.html

   This example code is in the public domain.
*/

// Teensy 2.0 has the LED on pin 11
// Teensy++ 2.0 has the LED on pin 6
// Teensy 3.x / Teensy LC have the LED on pin 13
#include "Arduino.h"
#include "stdint.h"


// the setup() method runs once, when the sketch starts

void setup() {
  // initialize the digital pin as an output.
  Serial.begin(9600);
  while(!Serial);
  delay(1000);
  Serial.println("Read EMG");
}

// the loop() methor runs over and over again,
// as long as the board has power

void loop() {
  // read the emg value and display it onto the monitor
  int value = analogRead(13);
  Serial.println(value);
  delay(100);
}
