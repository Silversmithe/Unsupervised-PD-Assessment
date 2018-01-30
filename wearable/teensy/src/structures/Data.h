/*
  MedData.h

  Alexander S. Adranly

  This struct contains the basic storage of all information necessary to gather
  diagnostics

  NOTES:
  January 8th, 2018
  Angular Velocity is important for analysis
  - include angular velocity in the PAYLOAD packet ( can keep pos still if fits)


*/
#include "stdint.h"

#ifndef MED_DATA_H
#define MED_DATA_H

/* INFORMATION STORED IN BUFFER */
struct Data {
  /* ------------------ EMG -----------------------*/
  int16_t emg[2]; // Raw Rect
  /*
    ------------------ IMU -----------------------
    In the array, data is organized as follows:
    [Axyz Gxyz Mxyz T]
  */
  float hand[10];
  float hand_pos[3];

  float thumb[10];
  float thumb_pos[3];

  float point[10];
  float point_pos[3];

  float ring[10];
  float ring_pos[3];

  /* TIMING */
  uint32_t dt; // distance between interrupts
};

/* INFORMATION SENT OVER RADIO */
struct Payload {
  /*
    UPDATE: floats are 4 bytes = 4*8 = 32 bits
    272 bits of information
    This would result in 27.2 kbits/s
  */
  /* Electromyography of Forearm */
  int16_t dEMG[2];
  /* Dorsum of Hand Position and Acceleration */
  int16_t dHACCEL[3];
  int16_t dHPOS[3];
  /* Thumb Finger Position and Angular Velocity */
  int16_t dTPOS[3];
  int16_t dTRADS[3];
  /* Pointer Finger Position */
  int16_t dPPOS[3];
  int16_t dPRADS[3];
  /* Ring Finger Position */
  int16_t dRPOS[3];
  int16_t dRRADS[3];
  /* Message Code TELEMETRY */
};

typedef struct Data Data;
typedef struct Payload Payload;

#endif
