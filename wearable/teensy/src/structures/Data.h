/*------------------------------------------------------------------------------
  file:         Data.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  This struct contains the all the information gathered and
                produced by the wearable device and other processing algorithms
  ----------------------------------------------------------------------------*/
#include "stdint.h"

#ifndef MED_DATA_H
#define MED_DATA_H

/* INFORMATION STORED IN BUFFER */
struct Data {
  /* worst case data
    32 + 13*4*32 + 32 = 1,728 bits

    100 Hz --> 172,800 bits per second

    200 Hz --> 345,600 bits per second (unsustainable with Zigbee!)

    if Mxyz and Temp are removed per sensor:
    200Hz -> 243,200 bits per second
  */

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
