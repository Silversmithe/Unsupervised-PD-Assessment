/*
  multiDeviceBus.cpp

  Alexander Sami Adranly
*/

#include "Arduino.h"
#include "stdint.h"
#include "MyoEMG/MyoEMG.h"

#define LED 13
#define RAW_PIN 13
#define RECT_PIN 12

// EMG Object Test
EMG forearm(RECT_PIN, RAW_PIN);
int raw_value, rect_value;

void setup() {
  // serial to display data
  Serial.begin(115200);
  while(!Serial) {}

}

void loop() {
  // read the sensor
  raw_value = forearm.getRaw();
  rect_value = forearm.getRect();

  // display the sensor value
  Serial.printf("%d\t%d\n", raw_value, rect_value);

  delay(200);
}
