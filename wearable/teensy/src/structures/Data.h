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

/* INFORMATION STORED IN BUFFER */
struct Data {
  /* 4B + 4 *(2*6) = 52B*/
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

typedef struct Data Data;

#endif
