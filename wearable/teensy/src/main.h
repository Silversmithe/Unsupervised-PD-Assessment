/*
--------------------------------------------------------------------------------
  main.cpp (Wearable Version 1: IRON FIST)

  Main Application for gathering and reporting information of both sensors in
  one. This is the prototype for the main application.
  Wearable device gathers information about the muscles of the arm and its
  fingers to perform diagnostics of parkinson's disease.

  Alexander Sami Adranly
--------------------------------------------------------------------------------
In the H file, useful definitions will be made. The device can also be
configured here to run or not run different sensors depending on what is
necessary. This is particularly useful for unittesting the system.
--------------------------------------------------------------------------------
*/

#include "MyoEMG/MyoEMG.h"             // EMG library
#include "MPU9250/MPU9250.h"           // IMU library
#include "analysis/quaternionFilters.h" // quad filters
#include "structures/IOBuffer.h"       // IOBuffer
#include "structures/Data.h"        // Medical Data Packet

#ifndef MAIN_H
#define MAIN_H

/* PROGRAM INFO */
#define VERSION 1

/* COMMUNICATION SELECTORS */
#define SERIAL_SELECT        true      // Turn on/off Serial communication
#define XBEE_SELECT          false     // Turn on/off Xbee (Radio) communication
#define IS_CONSUMED SERIAL_SELECT || XBEE_SELECT // is the data being consumed

/* DEVICE SELECTORS */
#define EMG_SELECT    true      // Turn on/off Forearm EMG readings
#define HAND_SELECT   true      // Turn on/off dorsum hand IMU readings
#define THUMB_SELECT  true      // Turn on/off Thumb IMU readings
#define POINT_SELECT  true      // Turn on/off Pointer IMU readings
#define RING_SELECT   true     // Turn on/off Ring IMU readings

/* COMMUNICATION DEFINITION */
#define BAUD_RATE 115200        // rate information is transferred serially
#define BUFFER_SIZE 100         // amount of packets that can be

/* EMG DEFINITION */
#define RAW_PIN   12            // Teensy pin to read RAW signal
#define RECT_PIN  13            // Teensy pin to read RECT signal

/* IMU DEFINITION */
#define IMU_ADDR_LO 0x68        // Low address for IMU
#define IMU_ADDR_HI 0x69        // High address for IMU

/* PINS */
#define BUILTIN_LED 13          // builtin led for signaling

/* SAMPLING INFORMATION */
#define DOUBLE_SAMPLE_RATE 5000   // microseconds, 200Hz
#define FULL_SAMPLE_RATE   10000  // microseconds, 100 Hz
#define DEMO_RATE          1000000 // microseconds

/* CHECKING CONFIGURATION */
#if SERIAL_SELECT == true && XBEE_SELECT == true
#error "Serial and Xbee communication should not both be turned on!"
#endif

/* FUNCTION PROTOTYPES */
// Sensor
void imu_setup();                  // initialize all imus accordingly
void sensor_isr();                 // called whenever the device samples
void get_orientation(Data* item);  // convert sensor data to orientation data

// Errors
void com_search_light();             // if device is searching for communcation

// Serial
void serial_print_data(Data* src); // print the meddata to the serial

// Communication
bool transfer_payload(Payload* payload); // transfer payload over COM connection

#endif
