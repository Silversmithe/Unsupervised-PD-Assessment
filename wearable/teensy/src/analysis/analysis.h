/*------------------------------------------------------------------------------
  file:         analysis.h

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description: the analysis file contains any algorithms that will be used
               to further process the information being recieved by the
               wearable device. possible transformations of the raw data
               set may include:

               - processing for intelligent power consumption
               - data filtering to extract data
               - device health
   ---------------------------------------------------------------------------*/
#include "quaternionFilters.h"
#include "../structures/Data.h"

#ifndef ANALYSIS_H
#define ANALYSIS_H

// functions to convert orientation data
float to_pitch();   // quaternion -> pitch
float to_yaw();     // quaternion -> yaw
float to_roll();    // quaternion -> roll

// convert sensor data to orientation data
void orient(Data* item, bool hand, bool thumb, bool point, bool ring);

#endif
