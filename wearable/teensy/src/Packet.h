/*
  ------------------------------------------------------------------------------
  packet.h

  Alexander S. Adranly
  December 31st, 2017
  ------------------------------------------------------------------------------
  Create a container to send the information to the computer
  Assuming that each sensor is gathered at once and at the same rate.
  Can provide different types of packets depending on what rates are being
  transferred
  ------------------------------------------------------------------------------
*/
#include "stdint.h"

#ifndef PACKET_H
#define PACKET_H

typedef struct PACKET {
  // IMU Fingers
  int16_t* thumb_gyro;    // IMU - THUMB
  int16_t* pointer_gyro;  // IMU - POINTER
  int16_t* ring_gyro;     // IMU - RING
  // IMU - Dorsum Hand
  int16_t* hand_gyro;
  int16_t* hand_accel;
  // EMG
  int16_t* emg_sig;       // raw, rect
} PACKET;

#endif
