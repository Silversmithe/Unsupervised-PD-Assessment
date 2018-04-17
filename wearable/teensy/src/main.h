/*------------------------------------------------------------------------------
  file:         main.cpp (Wearable Version 2: SECOND SKIN)

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
#include "structures/IOBuffer.h"          // IOBuffer
#include "structures/Data.h"              // Data Struct
#include "com/com.h"                      // Communications Functions
#include "errors.h"                        // error values

#ifndef MAIN_H
#define MAIN_H

/* PROGRAM INFO */
#define VERSION 1
const uint8_t DEVICE_ID = '1';    // ID for this specific wearable device

/* DEVICE SELECTORS */
#define EMG_SELECT    true     // Turn on/off Forearm EMG readings
#define HAND_SELECT   true      // Turn on/off dorsum hand IMU readings
#define THUMB_SELECT  true      // Turn on/off Thumb IMU readings
#define POINT_SELECT  true      // Turn on/off Pointer IMU readings
#define RING_SELECT   true      // Turn on/off Ring IMU readings

/* COMMUNICATION DEFINITION */
const int SERVER_ADDR = 0xFE2F;
const int WEAR_ADDR = 0xFE31;

#define BUFFER_SIZE    500
#define BUFFER_STALL   200
#define BUFFER_FLUSH   10       // how much the consumer is allowed to leave in buffer
#define CONSUMER_RATE  10       // miliseconds: amount of delay for consumer

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

/* COMMUNICATION CONSTANTS */
const bool SERIAL_SELECT = true;       // Serial communication toggle
const bool XBEE_SELECT = false;         // Xbee (Radio) communication toggle

/* PINS */
const unsigned BUILTIN_LED = 13;     // builtin led for signaling
const unsigned EMG_RAW_PIN = 12;     // analog pin for emg sampling
const unsigned EMG_RECT_PIN = 13;    // analog pin for emg rectified sampling
const unsigned XBEE_SLEEP_PIN = 2;   // digital pin to sleep/wake radio

/* FSM STATES */
enum State {
  INIT,
  ONLINE,
  OFFLINE,
  KILL
};

/* FUNCTION PROTOTYPES */
bool imu_setup(bool trace);                // initialize all imus accordingly
void sensor_isr(void);                     // called whenever the device samples
void kill(void);                           // load the bootloader state

#endif
