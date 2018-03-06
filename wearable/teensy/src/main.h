/*------------------------------------------------------------------------------
  file:         main.cpp (Wearable Version 1: IRON FIST)

  author:       Alexander Sami Adranly
  ------------------------------------------------------------------------------
  description:  Main Application for gathering and reporting information of both
  sensors in one. This is the prototype for the main application.
  Wearable device gathers information about the muscles of the arm and its
  fingers to perform diagnostics of parkinson's disease.

  In the H file, useful definitions will be made. The device can also be
  configured here to run or not run different sensors depending on what is
  necessary. This is particularly useful for unittesting the system.
  ----------------------------------------------------------------------------*/

#include "myoEMG/MyoEMG.h"                // EMG library
#include "mpu9250/MPU9250.h"              // IMU library
#include "analysis/analysis.h"            // analysis functions
#include "structures/IOBuffer.h"          // IOBuffer
#include "structures/Data.h"              // Data Struct
#include "com/com.h"                      // Communications Functions

#ifndef MAIN_H
#define MAIN_H

/* PROGRAM INFO */
#define VERSION 1

/* DEVICE SELECTORS */
#define EMG_SELECT    false      // Turn on/off Forearm EMG readings
#define HAND_SELECT   true      // Turn on/off dorsum hand IMU readings
#define THUMB_SELECT  true      // Turn on/off Thumb IMU readings
#define POINT_SELECT  true      // Turn on/off Pointer IMU readings
#define RING_SELECT   true      // Turn on/off Ring IMU readings

/* COMMUNICATION DEFINITION */
#define BUFFER_SIZE    200      // amount of packets that can be
#define CONSUMER_RATE  10       // miliseconds

/* EMG DEFINITION */
#define RAW_PIN   12            // Teensy pin to read RAW signal
#define RECT_PIN  13            // Teensy pin to read RECT signal

/* IMU DEFINITION */
#define IMU_ADDR_LO 0x68        // Low address for IMU
#define IMU_ADDR_HI 0x69        // High address for IMU

/* SAMPLING INFORMATION */
#define DOUBLE_SAMPLE_RATE 5000     // microseconds, 200Hz
#define FULL_SAMPLE_RATE   10000    // microseconds, 100 Hz
#define DEMO_RATE          1000000  // microseconds

/* COMMUNICATION SELECTORS */
const int SRC_XBEE_ADDRESS = 0x0001;   // MY address (for reference)
const int DEST_XBEE_ADDRESS = 0x0002;  // Destination address (for use)
const bool SERIAL_SELECT = false;       // Serial communication toggle
const bool XBEE_SELECT = true;         // Xbee (Radio) communication toggle
const unsigned TIMEOUT = 5000;              // error timeout

/* PINS */
const unsigned BUILTIN_LED = 13;     // builtin led for signaling
const unsigned EMG_RAW_PIN = 12;     // analog pin for emg sampling
const unsigned EMG_RECT_PIN = 13;    // analog pin for emg rectified sampling

/* FUNCTION PROTOTYPES */
void imu_setup();                  // initialize all imus accordingly
void sensor_isr();                 // called whenever the device samples

#endif
