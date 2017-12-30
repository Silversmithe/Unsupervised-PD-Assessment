/*
  ------------------------------------------------------------------------------
  main.cpp

  Alexander S. Adranly
  December 29th, 2017
  ------------------------------------------------------------------------------
  Driver program, change main code to select unittests or running the main
  program
  ------------------------------------------------------------------------------
*/
#include "Arduino.h"
#include "stdint.h"
// #include "i2c/i2c_t3.h"       // Teensy wire library
#include "MPU9250/MPU9250.h"
#include "MyoEMG/MyoEMG.h"
#include "TimerOne.h"         // timer & interrupt library

/* GLOBAL VARIALBES */
#define DEBUG           true  // defines debug state
#define BAUD_RATE       9600  // baud rate of the serial connection
#define IMU_ADDR_LO     0x68  // lower imu address on bus
#define IMU_ADDR_HI     0x69  // higher imu address on bus
#define EMG_RAW_PIN     13    // pin on teensy for raw emg (ANALOG)
#define EMG_REC_PIN     12    // pin on teensy for rectified emg (ANALOG)

/* MODE SELECTION */
#define MODE 0x00             // defines code to run (codes in unittest.h)
#if MODE != 0x00
  #include "unittest/unittest.h"
#endif
#if MODE == 0x00
  // IMU Devices
  MPU9250 POINT(Wire, IMU_ADDR_LO);              // pointer finger
  MPU9250 THUMB(Wire, IMU_ADDR_HI);              // thumb finger
  MPU9250 RING(Wire1, IMU_ADDR_LO);              // ring finger
  MPU9250 DORSAL(Wire1, IMU_ADDR_HI);            // back of palm
  // EMG Sensor
  EMG FOREARM(EMG_REC_PIN, EMG_RAW_PIN);         // EMG signal
#endif

/* FUNCTION PROTOTYPES */
bool die();   // graceful death of program

/* MAIN FUNCTIONS */
void setup() {
    /* ADJUST BASED ON MODE */
    if(MODE != 0x00){
        // unittest_runner(MODE);   // hand off to unit tester
    } else {
      /* MAIN SETUP */
      /* INITIALIZE SERIAL MONITOR */
      Serial.begin(BAUD_RATE);

      /* INITIALIZE IMU */
    } // endif
}

void loop() {
  if(MODE == 0x00){
    /* MAIN LOOP */

  } // endif
}
