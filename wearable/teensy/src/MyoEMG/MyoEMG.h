/*------------------------------------------------------------------------------
  file:         MyoEMG.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  A wrapper data structure to represent the EMG sensor attached
                to the wearable device. responsible for keeping track of which
                pins the device is attached to, which pin allows the device
                to read raw data, and which pin allows the device to read
                rectified data.
  ----------------------------------------------------------------------------*/
#include "Arduino.h"
#include "stdint.h"

#ifndef MYOEMG_H
#define MYOEMG_H

class EMG {
public:
  EMG(uint8_t prect, uint8_t praw);             // EMG constructor
  int16_t getRaw(void);                  // get the raw signal
  int16_t getRect(void);                 // get the rectified signal

private:
  uint8_t raw_pin;                              // define raw pin
  uint8_t rect_pin;                             // define rectified pin
};

#endif
