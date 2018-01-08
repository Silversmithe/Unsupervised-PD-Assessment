/*
  MedData.h

  Alexander S. Adranly

  This struct contains the basic storage of all information necessary to gather
  diagnostics
*/
#include "stdint.h"

#ifndef MED_DATA_H
#define MED_DATA_H

/* INFORMATION STORED IN BUFFER */
struct MedData {
  /* EMG */
  uint16_t emg_raw, emg_rect;

  /* IMU */
  // HAND
  float Hand_Ax, Hand_Ay, Hand_Az; // mss
  float Hand_Gx, Hand_Gy, Hand_Gz; // rads/s
  float Hand_Mx, Hand_My, Hand_Mz;
  float Hand_T;

  // Thumb Finger
  float Thumb_Ax, Thumb_Ay, Thumb_Az; // mss
  float Thumb_Gx, Thumb_Gy, Thumb_Gz; // rads/s
  float Thumb_Mx, Thumb_My, Thumb_Mz;
  float Thumb_T;

  // Pointer Finger
  float Point_Ax, Point_Ay, Point_Az; // mss
  float Point_Gx, Point_Gy, Point_Gz; // rads/s
  float Point_Mx, Point_My, Point_Mz;
  float Point_T;

  // Ring Finger
  float Ring_Ax, Ring_Ay, Ring_Az; // mss
  float Ring_Gx, Ring_Gy, Ring_Gz; // rads/s
  float Ring_Mx, Ring_My, Ring_Mz;
  float Ring_T;

  /* TIMING */
  uint32_t dT;
};

/* INFORMATION SENT OVER RADIO */
struct Payload {
  /*
    272 bits of information
    This would result in 27.2 kbits/s
  */
  /* Electromyography of Forearm */
  uint16_t dEMG[2];
  /* Dorsum of Hand Position and Acceleration */
  uint16_t dHACCEL[3];
  uint16_t dHPOS[3];
  /* Thumb Finger Position */
  uint16_t dTPOS[3];
  /* Pointer Finger Position */
  uint16_t dPPOS[3];
  /* Ring Finger Position */
  uint16_t dRPOS[3];
};

typedef struct MedData MedData;
typedef struct Payload Payload;

#endif
