/*------------------------------------------------------------------------------
  file:         main.cpp (Wearable Version 2: SECOND SKIN)

  author:       Alexander S. Adranly
  ------------------------------------------------------------------------------
  description:  Main Application for gathering and reporting information of both
  sensors in one. This is the prototype for the main application.
  Wearable device gathers information about the muscles of the arm and its
  fingers to perform diagnostics of parkinson's disease.
  ----------------------------------------------------------------------------*/
#include "main.h"
#include <Arduino.h>              // Arduino Library
#include "stdint.h"               // Integer Library
#include "TimerOne.h"             // Timer Libaray

/* VARIABLES */
static IOBuffer BUFFER(BUFFER_SIZE);
static Data* temp_data;
static uint32_t current_time, instant_time, delta_time;

/* STATE */
State __current_state;

/* DEVICE INITIALIZATION */
bool __enabled[4] = {
  THUMB_SELECT,
  POINT_SELECT,
  HAND_SELECT,
  RING_SELECT
};

EMG forearm(RECT_PIN, RAW_PIN);
MPU9250 __imus[4] = {
  MPU9250(Wire1, IMU_ADDR_HI),   // hand
  MPU9250(Wire, IMU_ADDR_LO),   // thumb finger
  MPU9250(Wire, IMU_ADDR_HI),   // pointer finger
  MPU9250(Wire1, IMU_ADDR_LO)   // ring finger
};

/* SETUP */
void setup(void) {
  bool hardware_success = false;
  bool network_success = false;
  __current_state = INIT;   // Initialization state

  /* HARDWARE INITIALIZATION PROCEDURE */
  // 1. can you initialize all hardware?
  // STATE <- YES: INIT, NO: KILL
  pinMode(BUILTIN_LED, OUTPUT);   // BUILTIN_LED -> 13 D
  hardware_success |= init_com();            // setup HWSERIAL & XBEE
  hardware_success |= imu_setup(false);      // setup IMU
  if(!hardware_success){
    __current_state = KILL;
    kill();
  }

  /* NETWORK INITIALIZATION PROCEDURE */
  // 1. Can you contact the server?
  //    STATE <- YES: ONLINE, NO: OFFLINE
  // 2. How strong is the connection?
  //    STATE <- > 50%: ONLINE, < 50%: OFFLINE
  if(XBEE_SELECT){ network_success = isAnyoneThere(); }

  __current_state = (network_success)? ONLINE : OFFLINE;
  if(__current_state == ONLINE)
    log("current state: ONLINE");
  else
    log("current state: OFFLINE");

  /* delay before running */
  delay(5000);
  /* START TRAP TIMER */
  Timer1.initialize(FULL_SAMPLE_RATE); // DEMO_RATE FULL_SAMPLE_RATE DOUBLE_SAMPLE_RATE
  Timer1.attachInterrupt(sensor_isr);
  // current_time = micros();            // initialize timer
}

/*
 *  function:     loop
 *
 *  description:  main consumer thread, responsible for picking packets out
 *                of the buffer and sending it over the radio or the serial
 *                monitor.
 */
void loop(void) {

  // eventually do BURST logging
  // wait to log after a set of points have been collected
  if(!BUFFER.is_empty()){
      // remove a Data item from buffer
      temp_data = BUFFER.remove_front();
      /* DATA PROCESSING */
      // Load Position data into Data structures using Mahony Filter
      // orient(data, HAND_SELECT, THUMB_SELECT, POINT_SELECT, RING_SELECT);
      /* DATA TRANSFER */
      if(SERIAL_SELECT){write_console(temp_data);}

      if(__current_state == ONLINE){ /* ONLINE */
        write_radio(temp_data);
      } else { /* OFFLINE */
        log_payload(temp_data);
      }
  }
  delay(CONSUMER_RATE);
}

/*
 *  function:     kill
 *
 *  description:  put the device in an infinite state of waiting and notify
 *                the user that the device should be rebooted or debugged
 */
void kill(void){
  close_log();
  kill_light();
  while(1){ delay(10000); }
}

/*
 *  function:     imu_setup
 *
 *  param:        (bool) trace: turn on debugger tracer
 *
 *  description:  hardware initialization of the inertial measurement
 *                units. should return some status of the operations.
 *                Returns true if the initialization was 100% successful.
 */
bool imu_setup(bool trace){
  int status[4];
  bool out = false;
  if(trace && !SERIAL_SELECT) { return false; }

  for(int i=0; i<4; i++){
    if(__enabled[i]){
      status[i] = __imus[i].begin();
      out = out | !(status[i] < 0);
      if(trace && status[i] < 0){
        Serial.print("(");
        Serial.print(i);
        Serial.print("): hardware error, CODE: ");
        Serial.println(status[i]);
      }
    }
  }
  return out;
}

/*
 *  function:     sensor_isr
 *
 *  description:  method that runs after each interrupt from the main thread.
 *                this function is responsible for gathering all the information
 *                from the sensors and store it in a packet, which gets pushed
 *                onto the buffer.
 */
void sensor_isr(void){
  // update the time
  instant_time = micros();
  delta_time = instant_time - current_time;
  current_time = instant_time;

  // new information set for buffer
  Data packet = {
    {0,0},                    // EMG DATA
    {0,0,0,0,0,0,0,0,0,0},    // HAND
    {0,0,0},                  // HPOSITION
    {0,0,0,0,0,0,0,0,0,0},    // THUMB
    {0,0,0},                  // TPOSITION
    {0,0,0,0,0,0,0,0,0,0},    // POINT
    {0,0,0},                  // PPOSITION
    {0,0,0,0,0,0,0,0,0,0},    // RING
    {0,0,0},                  // RPOSITION
    delta_time                // dt
  };

  float* __data_pointer = packet.hand;  // use this to jump around

  /* READ/STORE SENSOR INFORMATION */
  if(EMG_SELECT){
    packet.emg[0] = forearm.getRaw();
    packet.emg[1] = forearm.getRect();
  }
  for(int i=0; i<4; i++){ // IMUS
    if(__enabled[i]){
      __data_pointer[0] = __imus[i].getAccelX_mss();
      __data_pointer[1] = __imus[i].getAccelY_mss();
      __data_pointer[2] = __imus[i].getAccelZ_mss();
      __data_pointer[3] = __imus[i].getGyroX_rads();
      __data_pointer[4] = __imus[i].getGyroY_rads();
      __data_pointer[5] = __imus[i].getGyroZ_rads();
      __data_pointer[6] = __imus[i].getMagX_uT();
      __data_pointer[7] = __imus[i].getMagY_uT();
      __data_pointer[8] = __imus[i].getMagZ_uT();
      __data_pointer[9] = __imus[i].getTemperature_C();
      __data_pointer = __data_pointer + 13; // start at position array
    } else {
      __data_pointer = __data_pointer + 13; // skip this part in the pointer
    }
  }

  // store packet in buffer
  BUFFER.push_back(packet);
}
