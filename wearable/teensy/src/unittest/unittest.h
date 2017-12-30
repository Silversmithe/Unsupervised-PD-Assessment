/*
  ------------------------------------------------------------------------------
  unittest.cpp

  Alexander S. Adranly
  December 29th, 2017
  ------------------------------------------------------------------------------
  Defining the tests of different levels of functionality
  ------------------------------------------------------------------------------
  UNIT TEST CODES
  MAIN:     0x00 --> not a unit test, runs main code
  EMG_0:    0x01 --> testing one emg for rectified signal on console, SERIAL
  EMG_1:    0x02 --> testing emg for raw signal, SERIAL
  IMU_0:    0x03 --> testing one imu, all signals, SERIAL
  IMU_1:    0x04 --> testing two imu on one bus, SERIAL

*/
#include "stdint.h"

#ifndef UNITTEST_H
#define UNITTEST_H

/* TEST DRIVER */
bool unittest_runner(uint8_t mode_type); // runs all unit tests
/* UNIT TESTS */
// EMG
bool emg_0 (); // testing one emg for rectified signal on console, SERIAL
bool emg_1 (); // testing emg for raw signal, SERIAL
// IMU
bool imu_0 (); // testing one imu, all signals, SERIAL
bool imu_1 (); // testing two imu, on one bus, SERIAL

#endif
