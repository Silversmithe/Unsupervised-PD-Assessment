/*
--------------------------------------------------------------------------------
MyoEMG structued programming:

Alexander S. Adranly (aadranly@scu.edu)
--------------------------------------------------------------------------------
*/

#ifndef MYOEMG_H
#define MYOEMG_H

#include "Arduino.h"
#include "stdint.h"

class EMG {
public:
  EMG(uint8_t prect, uint8_t praw=0);           // EMG constructor
  int16_t getRaw();                             // get the raw signal
  int16_t getRect();                            // get the rectified signal

private:
  uint8_t raw_pin;                              // define raw pin
  uint8_t rect_pin;                             // define rectified pin
};

#endif
