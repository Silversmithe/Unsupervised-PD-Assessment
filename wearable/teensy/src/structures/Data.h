/*------------------------------------------------------------------------------
  file:         Data.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  This struct contains the all the information gathered and
                produced by the wearable device and other processing algorithms
  ----------------------------------------------------------------------------*/
#include "stdint.h"

#ifndef DATA_H
#define DATA_H

struct Data {
  /* ------------------ EMG -----------------------*/
  int16_t emg[2]; // [Raw Rect]
  /* ------------------ IMU -----------------------
    (float[10])[Axyz Gxyz Mxyz T]
    (float[3]) [xyz]
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
  float dt; // distance between interrupts
};

typedef struct Data Data;

#endif
