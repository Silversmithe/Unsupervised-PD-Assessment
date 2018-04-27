/*------------------------------------------------------------------------------
  file:         Data.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  This struct contains the all the information gathered and
                produced by the wearable device and other processing algorithms

                (16*2) + (4*9)*4 = 176
  ----------------------------------------------------------------------------*/
#include "stdint.h"

#ifndef DATA_H
#define DATA_H

struct Data {
  /* ------------------ EMG -----------------------*/
  int16_t emg[2]; // [Raw Rect]
  /* ------------------ IMU -----------------------
    (float[10])[Axyz Gxyz Mxyz T]
  */
  float hand[9];
  float thumb[9];
  float point[9];
  float ring[9];
};

typedef struct Data Data;

#endif
