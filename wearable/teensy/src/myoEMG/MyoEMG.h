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

typedef struct myEMG {
  /* PINS */
  // Rectified, Integrated, Amplified Signal
  int8_t sig_pin;         // Regular Rectified Signal

  // Electrode Extension
  int8_t mmep_pin;        // Mid Muscle Electrode Pin
  int8_t emep_pin;        // End Muscle Electrode Pin
  int8_t rep_pin;         // Reference Electrode Pin

  // Raw data request
  int8_t raw_pin;         // Raw signal Pin

  /* SIGNAL */
  int16_t raw_sig;        // Raw Signal
  int16_t rect_sig;       // Rectified Signal (EMG Envelope)
} myEMG;

#endif
